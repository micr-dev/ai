#!/usr/bin/env python3
"""Condense agent session transcripts (JSONL) into readable digest slices for ios-reflect miners.

Keeps user messages, assistant text, tool-call heads, tool errors, and compaction summaries.
Drops tool output bodies, which are most of the bytes and little of the signal.

Usage: build-digests.py <session-dir-or-jsonl>... --out <dir> [--slice-bytes 450000]
Writes main-*.md for top-level sessions and sub-NN.md for subagent transcripts.
"""
import argparse
import glob
import json
import os


def text_of(message):
    content = message.get("content")
    if isinstance(content, str):
        return content
    parts = []
    for part in content or []:
        kind = part.get("type")
        if kind == "text":
            parts.append(part["text"])
        elif kind in ("toolCall", "tool_use"):
            args = json.dumps(part.get("arguments", part.get("input", {})))[:300]
            parts.append(f"[call {part.get('name')}] {args}")
    return "\n".join(parts)


def digest(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if entry.get("type") == "compaction":
            out.append("## COMPACTION SUMMARY\n" + str(entry.get("summary", ""))[:6000])
            continue
        message = entry.get("message")
        if not isinstance(message, dict):
            continue
        role = message.get("role")
        if role == "user":
            out.append("## USER\n" + text_of(message)[:8000])
        elif role == "assistant":
            text = text_of(message)
            if text.strip():
                out.append("## A\n" + text[:3000])
        elif role in ("toolResult", "tool") and message.get("isError"):
            out.append("## TOOL ERROR\n" + text_of(message)[:600])
    return "\n".join(out)


def write_slices(blocks, prefix, out_dir, limit):
    slices, size = [[]], 0
    for block in blocks:
        block = block[:limit]
        if size + len(block) > limit and slices[-1]:
            slices.append([])
            size = 0
        slices[-1].append(block)
        size += len(block)
    names = []
    for index, chunk in enumerate(slices):
        name = os.path.join(out_dir, f"{prefix}-{index:02d}.md")
        with open(name, "w", encoding="utf-8") as handle:
            handle.write("".join(chunk))
        names.append(name)
    return names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--out", required=True)
    parser.add_argument("--slice-bytes", type=int, default=450_000)
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    top, subs = [], []
    for item in args.inputs:
        if item.endswith(".jsonl"):
            top.append(item)
            continue
        top += sorted(glob.glob(os.path.join(item, "*.jsonl")))
        # Subagent transcripts live in per-session directories next to the top-level file.
        subs += sorted(glob.glob(os.path.join(item, "*", "**", "*.jsonl"), recursive=True))

    main_blocks = [f"\n\n# ===== SESSION {os.path.basename(p)}\n" + digest(p) for p in top]
    # Top-level sessions get split too: a long parent session easily exceeds one slice.
    main_text = "".join(main_blocks)
    main_chunks = [main_text[i : i + args.slice_bytes] for i in range(0, len(main_text), args.slice_bytes)]
    written = []
    for index, chunk in enumerate(main_chunks):
        name = os.path.join(args.out, f"main-{index:02d}.md")
        with open(name, "w", encoding="utf-8") as handle:
            handle.write(chunk)
        written.append(name)
    sub_blocks = [f"\n\n# ===== SUBAGENT {os.path.relpath(p, os.path.dirname(p.rstrip('/')))}\n" + digest(p) for p in subs]
    written += write_slices(sub_blocks, "sub", args.out, args.slice_bytes)
    print("\n".join(written))


if __name__ == "__main__":
    main()
