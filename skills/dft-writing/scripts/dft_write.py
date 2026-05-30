#!/usr/bin/env python3
"""Call the Rosmine DFT Writing Demo through Gradio's direct API."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
import uuid


BASE_URL = "https://dft.rosmine.ai"
PREDICT_URL = f"{BASE_URL}/gradio_api/run/predict"
FN_INDEX = {
    "good": 6,
    "fast": 7,
}
EXAMPLE_FN_INDEX = {
    1: 14,
    2: 15,
    3: 16,
}


def post_predict(payload: dict, timeout: int) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        PREDICT_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"DFT API HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"DFT API request failed: {error}") from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"DFT API returned invalid JSON: {error}") from error


def normalize_tokens(value: int) -> int:
    rounded = round(value / 100) * 100
    return max(100, min(1000, rounded))


def read_text(value: str | None, path: str | None) -> str:
    if value is not None and path is not None:
        raise SystemExit("Use either inline text or a file path, not both.")
    if path is None:
        return value or ""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def collect_warnings(data: list) -> list[str]:
    warnings = []
    for item in data[1:5]:
        if isinstance(item, dict):
            if item.get("visible") is False:
                continue
            value = str(item.get("value") or "")
            if value and "color:#b91c1c" in value:
                text = (
                    value.replace("<span style='color:#b91c1c'>", "")
                    .replace("</span>", "")
                    .strip()
                )
                if text:
                    warnings.append(text)
    return warnings


def print_json(value: dict) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def run_example(number: int, timeout: int, as_json: bool) -> None:
    session_id = f"dft-{uuid.uuid4().hex[:12]}"
    response = post_predict(
        {
            "data": [],
            "event_data": None,
            "fn_index": EXAMPLE_FN_INDEX[number],
            "session_hash": session_id,
        },
        timeout,
    )
    data = response.get("data") or []
    result = {
        "prompt": data[0] if len(data) > 0 else "",
        "outline": data[1] if len(data) > 1 else "",
        "style": data[2] if len(data) > 2 else "",
        "use_case": data[3] if len(data) > 3 else "",
        "tokens": data[4] if len(data) > 4 else None,
    }
    if as_json:
        print_json(result)
        return
    for key, value in result.items():
        print(f"{key}: {value}")


def run_generate(args: argparse.Namespace) -> None:
    prompt = read_text(args.prompt, args.prompt_file).strip()
    outline = read_text(args.outline, args.outline_file).strip()
    if not prompt:
        raise SystemExit("A prompt is required.")

    tokens = normalize_tokens(args.tokens)
    session_id = args.session_id or f"dft-{uuid.uuid4().hex[:12]}"
    started = time.monotonic()
    response = post_predict(
        {
            "data": [
                prompt,
                outline,
                args.style,
                args.use_case,
                tokens,
                args.allow_emdash,
                True,
                session_id,
            ],
            "event_data": None,
            "fn_index": FN_INDEX[args.mode],
            "session_hash": session_id,
        },
        args.timeout,
    )
    elapsed = time.monotonic() - started
    data = response.get("data") or []
    output = data[0] if data else ""
    result = {
        "mode": args.mode,
        "tokens": tokens,
        "elapsed_seconds": round(elapsed, 2),
        "output": output,
        "warnings": collect_warnings(data),
        "raw": response if args.include_raw else None,
    }
    if args.json:
        if not args.include_raw:
            result.pop("raw")
        print_json(result)
        return
    if result["warnings"]:
        print("\n".join(f"Warning: {warning}" for warning in result["warnings"]), file=sys.stderr)
    print(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=sorted(FN_INDEX), default="fast")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--outline", default="")
    parser.add_argument("--outline-file")
    parser.add_argument("--style", default="Clear, informative")
    parser.add_argument("--use-case", default="News Article")
    parser.add_argument("--tokens", type=int, default=600)
    parser.add_argument("--allow-emdash", action="store_true")
    parser.add_argument("--session-id")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--example", type=int, choices=sorted(EXAMPLE_FN_INDEX))
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.example is not None:
        run_example(args.example, args.timeout, args.json)
        return
    run_generate(args)


if __name__ == "__main__":
    main()
