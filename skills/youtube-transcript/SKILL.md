---
name: youtube-transcript
description: Fetch or create transcripts for YouTube videos. Use when the user wants captions, subtitles, transcript text, timestamps, or a summary that requires the video's spoken content. Prefer existing captions with yt-dlp, then transcribe audio locally with Whisper when captions are unavailable.
---

# YouTube Transcript

Produce a clean transcript file without paid services. Use existing captions when possible because they are faster and may be creator-corrected. Use local Whisper when the video has no usable captions.

## Output

- Save into the current project when it is relevant; otherwise use `~/Downloads`.
- Name the file `Channel_Title.txt`, replacing unsafe filename characters with `_`. Fall back to the video ID when metadata is unavailable.
- Report the saved path. Print the transcript only when it is short or the user asks.

Get a safe base name:

```bash
URL="VIDEO_URL"
OUT="$(pwd)" # Use ~/Downloads when the current directory is unrelated.
META=$(yt-dlp --print '%(channel,uploader,uploader_id)s|%(title)s' --skip-download "$URL")
NAME=$(printf '%s' "$META" | tr '| ' '__' | tr -cd '[:alnum:]_.-')
[ -n "$NAME" ] || NAME=$(yt-dlp --print id --skip-download "$URL")
```

## 1. Existing captions

List captions first when the language is unknown:

```bash
yt-dlp --list-subs --skip-download "$URL"
```

Choose a creator-provided caption track before an automatically generated track. Download one explicit language as JSON3:

```bash
WORK=$(mktemp -d)
yt-dlp --skip-download --write-subs --write-auto-subs \
  --sub-langs "en" --sub-format json3 \
  -o "$WORK/captions.%(ext)s" "$URL"
CAPTION_FILE=$(find "$WORK" -maxdepth 1 -type f -name 'captions.*.json3' -print -quit)
```

Replace `en` with the requested or source language. If `CAPTION_FILE` exists, flatten that exact file:

```bash
python3 - "$CAPTION_FILE" "$OUT/$NAME.txt" <<'PY'
import html
import json
import pathlib
import re
import sys

source = pathlib.Path(sys.argv[1])
target = pathlib.Path(sys.argv[2])
payload = json.loads(source.read_text(encoding="utf-8"))
parts = [
    "".join(segment.get("utf8", "") for segment in event.get("segs") or [])
    for event in payload.get("events", [])
]
transcript = re.sub(
    r"\s+",
    " ",
    html.unescape(" ".join(part.strip() for part in parts if part.strip())),
).strip()
if not transcript:
    raise SystemExit("caption track contained no transcript text")
target.write_text(transcript + "\n", encoding="utf-8")
print(target)
PY
rm -f "$CAPTION_FILE"
rmdir "$WORK"
```

## 2. Local Whisper fallback

If no usable captions exist, download audio and transcribe it locally. This is pre-authorized for this machine; do not ask again.

```bash
yt-dlp -f ba -x --audio-format mp3 -o "$WORK/audio.%(ext)s" "$URL"
whisper "$WORK/audio.mp3" --model turbo --output_format txt --output_dir "$WORK"
mv "$WORK/audio.txt" "$OUT/$NAME.txt"
rm -f "$WORK/audio.mp3"
rmdir "$WORK"
```

- Pass `--language <language>` when known.
- Use `--model small` if `turbo` exceeds available memory. Accuracy may decrease.
- For timestamps, request JSON output and preserve Whisper's segments instead of flattening to plain text.
- Local transcription can be slow and may download model weights on first use.

## 3. Optional DeepAPI fallback

Use DeepAPI only when local YouTube access is blocked and `DEEPAPI_API_KEY` is already configured. It is a paid prepaid-credit service. Do not ask the user to subscribe or top up unless they explicitly prefer the hosted fallback.

## Failure handling

- On HTTP 429 or bot detection, stop instead of retrying in a loop.
- If `yt-dlp` fails because YouTube changed its extractor, update it using its installed package method, retry once, then stop.
- Do not claim success until the transcript file exists, is non-empty, and begins with coherent text.
