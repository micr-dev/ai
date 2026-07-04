#!/usr/bin/env python3
"""Call the current Deft Writing API for DFT-generated prose."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request


BASE_URL = "https://deftwriting.com"
GENERATE_URL = f"{BASE_URL}/api/generate"
GENERATION_MODE = {
    "generate": "simple",
    "rewrite": "rewrite",
}


def post_generate(payload: dict, timeout: int) -> tuple[dict, list[dict]]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        GENERATE_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"DFT API HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"DFT API request failed: {error}") from error
    if "application/x-ndjson" in content_type:
        return parse_ndjson(raw)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SystemExit(f"DFT API returned invalid JSON: {error}") from error
    if is_error(parsed):
        raise SystemExit(format_api_error(parsed))
    return parsed, []


def read_text(value: str | None, path: str | None) -> str:
    if value is not None and path is not None:
        raise SystemExit("Use either inline text or a file path, not both.")
    if path is None:
        return value or ""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def parse_ndjson(raw: str) -> tuple[dict, list[dict]]:
    progress = []
    complete = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise SystemExit(f"DFT API returned invalid NDJSON: {error}") from error
        event_type = event.get("type")
        if event_type == "progress" and isinstance(event.get("progress"), dict):
            progress.append(event["progress"])
        elif event_type == "complete" and isinstance(event.get("data"), dict):
            complete = event["data"]
        elif event_type == "error":
            raise SystemExit(format_api_error(event))
    if complete is None:
        raise SystemExit("DFT API response ended without a complete event.")
    return complete, progress


def is_error(value: object) -> bool:
    return isinstance(value, dict) and (
        "error" in value or isinstance(value.get("detail"), str)
    )


def format_api_error(value: object) -> str:
    if not isinstance(value, dict):
        return "DFT API returned an unknown error."
    error = value.get("error") or "unknown"
    detail = value.get("detail")
    if isinstance(detail, str) and detail:
        return f"DFT API error {error}: {detail}"
    return f"DFT API error {error}"


def print_json(value: dict) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_prompt(
    prompt: str,
    outline: str,
    style: str,
    use_case: str,
    words: int | None,
    allow_emdash: bool,
) -> str:
    sections = [prompt]
    if outline:
        sections.append(f"Outline:\n{outline}")
    if style:
        sections.append(f"Style: {style}")
    if use_case:
        sections.append(f"Use case: {use_case}")
    if words is not None:
        sections.append(f"Target length: about {words} words.")
    if not allow_emdash:
        sections.append(
            "Avoid em dashes. Use commas, colons, parentheses, or hyphens instead."
        )
    return "\n\n".join(sections)


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text))


def run_generate(args: argparse.Namespace) -> None:
    prompt = read_text(args.prompt, args.prompt_file).strip()
    outline = read_text(args.outline, args.outline_file).strip()
    if not prompt:
        raise SystemExit("A prompt is required.")
    if args.words is not None and args.words < 1:
        raise SystemExit("--words must be a positive integer.")
    rewrite_instructions = read_text(
        args.rewrite_instructions, args.rewrite_instructions_file
    ).strip()
    if args.mode == "rewrite" and not rewrite_instructions:
        rewrite_instructions = "Improve the draft while preserving its intent and facts."

    compiled_prompt = build_prompt(
        prompt=prompt,
        outline=outline,
        style=args.style.strip(),
        use_case=args.use_case.strip(),
        words=args.words,
        allow_emdash=args.allow_emdash,
    )
    started = time.monotonic()
    response, progress = post_generate(
        {
            "prompt": compiled_prompt,
            "generationMode": GENERATION_MODE[args.mode],
            "rewriteInstructions": rewrite_instructions,
            "progress": True,
        },
        args.timeout,
    )
    elapsed = time.monotonic() - started
    output = str(response.get("text") or "")
    metrics = response.get("metrics") if isinstance(response.get("metrics"), dict) else {}
    result = {
        "mode": args.mode,
        "words_requested": args.words,
        "words_returned": metrics.get("wordCount") or count_words(output),
        "elapsed_seconds": round(elapsed, 2),
        "generation_id": response.get("generationId"),
        "output": output,
        "metrics": metrics,
        "progress": progress,
        "raw": response if args.include_raw else None,
    }
    if args.json:
        if not args.include_raw:
            result.pop("raw")
        print_json(result)
        return
    print(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=sorted(GENERATION_MODE), default="generate")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--outline", default="")
    parser.add_argument("--outline-file")
    parser.add_argument("--style", default="Clear, informative")
    parser.add_argument("--use-case", default="News Article")
    parser.add_argument("--words", type=int)
    parser.add_argument("--rewrite-instructions")
    parser.add_argument("--rewrite-instructions-file")
    parser.add_argument("--allow-emdash", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-raw", action="store_true")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_generate(args)


if __name__ == "__main__":
    main()
