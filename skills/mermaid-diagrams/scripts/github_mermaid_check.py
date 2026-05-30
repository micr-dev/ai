#!/usr/bin/env python3
"""Check Markdown Mermaid blocks for GitHub README compatibility.

Static mode catches common README mistakes without dependencies. Render mode
extracts each Mermaid block and runs Mermaid CLI when available.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


FENCE_RE = re.compile(r"(?P<fence>`{3,}|~{3,})(?P<lang>[^\n`]*)\n(?P<body>.*?)(?P=fence)", re.DOTALL)
KNOWN_STARTS = {
    "architecture-beta",
    "block-beta",
    "c4component",
    "c4container",
    "c4context",
    "c4deployment",
    "classdiagram",
    "erdiagram",
    "flowchart",
    "gantt",
    "gitgraph",
    "graph",
    "journey",
    "mindmap",
    "packet-beta",
    "pie",
    "quadrantchart",
    "radar-beta",
    "requirementdiagram",
    "sankey-beta",
    "sequencediagram",
    "statediagram",
    "statediagram-v2",
    "timeline",
    "xychart-beta",
}


@dataclass
class MermaidBlock:
    index: int
    line: int
    body: str


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_mermaid_blocks(markdown: str) -> tuple[list[MermaidBlock], list[str]]:
    blocks: list[MermaidBlock] = []
    warnings: list[str] = []

    for match in FENCE_RE.finditer(markdown):
        lang = match.group("lang").strip()
        normalized_lang = lang.split()[0].lower() if lang else ""
        line = line_number(markdown, match.start())

        if "mermaid" in lang.lower() and normalized_lang != "mermaid":
            warnings.append(
                f"line {line}: Mermaid fence language should be exactly 'mermaid', got {lang!r}"
            )

        if normalized_lang == "mermaid":
            blocks.append(MermaidBlock(len(blocks) + 1, line, match.group("body").strip()))

    return blocks, warnings


def first_code_line(body: str) -> str:
    lines = [line.strip() for line in body.splitlines()]
    cursor = 0

    if lines[:1] == ["---"]:
        cursor = 1
        while cursor < len(lines) and lines[cursor] != "---":
            cursor += 1
        cursor += 1

    while cursor < len(lines):
        line = lines[cursor]
        if line and not line.startswith("%%"):
            return line
        cursor += 1

    return ""


def static_warnings(block: MermaidBlock) -> list[str]:
    warnings: list[str] = []
    first = first_code_line(block.body)
    diagram_type = first.split()[0].lower() if first else ""

    if not first:
        warnings.append(f"block {block.index} line {block.line}: empty Mermaid block")
        return warnings

    if diagram_type not in KNOWN_STARTS and first != "info":
        warnings.append(
            f"block {block.index} line {block.line}: first diagram line {first!r} is not a known Mermaid declaration"
        )

    if diagram_type in {"flowchart", "graph"}:
        risky_end_label = re.search(r"[\[({]\s*end\s*[\])}]", block.body)
        if risky_end_label:
            warnings.append(
                f"block {block.index} line {block.line}: contains an unquoted lowercase 'end' label; quote it or capitalize it"
            )

    for number, line in enumerate(block.body.splitlines(), start=block.line + 1):
        stripped = line.strip()
        if stripped.startswith("%%") and ("{" in stripped or "}" in stripped):
            warnings.append(
                f"block {block.index} line {number}: avoid braces in Mermaid comments; they can look like directives"
            )

    if "click " in block.body or "callback" in block.body:
        warnings.append(
            f"block {block.index} line {block.line}: interactive click/callback behavior is not README-safe"
        )

    if re.search(r"<script|<style|<link", block.body, re.IGNORECASE):
        warnings.append(
            f"block {block.index} line {block.line}: raw HTML/CSS/JS is not safe to depend on in GitHub Mermaid"
        )

    if any(token in diagram_type for token in ("beta",)) or diagram_type.startswith("c4"):
        warnings.append(
            f"block {block.index} line {block.line}: {diagram_type} may require a newer or experimental Mermaid renderer"
        )

    return warnings


def mermaid_command() -> list[str]:
    local = shutil.which("mmdc")
    if local:
        return [local]
    if shutil.which("npx"):
        return ["npx", "-y", "@mermaid-js/mermaid-cli"]
    return []


def browser_config(temp_dir: Path) -> list[str]:
    for browser_name in ("chromium-browser", "chromium", "google-chrome", "google-chrome-stable"):
        executable = shutil.which(browser_name)
        if executable:
            config_path = temp_dir / "puppeteer-config.json"
            config_path.write_text(
                json.dumps(
                    {
                        "executablePath": executable,
                        "args": [
                            "--no-sandbox",
                            "--disable-setuid-sandbox",
                            "--allow-file-access-from-files",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            return ["-p", str(config_path)]
    return []


def render_blocks(blocks: list[MermaidBlock]) -> list[str]:
    command = mermaid_command()
    if not command:
        return ["render requested but neither mmdc nor npx is available"]

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="mermaid-check-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        browser_args = browser_config(temp_dir)
        for block in blocks:
            source = temp_dir / f"block-{block.index}.mmd"
            output = temp_dir / f"block-{block.index}.svg"
            source.write_text(block.body + "\n", encoding="utf-8")
            run = subprocess.run(
                [*command, "-i", str(source), "-o", str(output), *browser_args],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if run.returncode != 0:
                message = (run.stderr or run.stdout).strip()
                failures.append(
                    f"block {block.index} line {block.line}: Mermaid CLI render failed: {message}"
                )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path, help="Markdown file to check")
    parser.add_argument("--render", action="store_true", help="render blocks with Mermaid CLI")
    args = parser.parse_args()

    markdown = args.markdown.read_text(encoding="utf-8")
    blocks, warnings = extract_mermaid_blocks(markdown)

    for block in blocks:
        warnings.extend(static_warnings(block))

    if args.render and blocks:
        warnings.extend(render_blocks(blocks))

    if not blocks:
        print(f"{args.markdown}: no Mermaid blocks found")
        return 0

    if warnings:
        print(f"{args.markdown}: checked {len(blocks)} Mermaid block(s), found issues:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print(f"{args.markdown}: checked {len(blocks)} Mermaid block(s), no issues found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
