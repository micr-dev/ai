# Images, video and transcripts

## Discover media

- Text-to-image: Kagi `search 'subject' --images --limit 5 --format json`, Firecrawl `search 'subject' --sources images --limit 5 --json`, or [Octen](octen.md) image search.
- Reference-image search: Octen accepts exactly one reference image instead of text; the installed MCP adapter has a documented incompatibility, so use the verified HTTP contract in that reference.
- Video/segment search: Octen video search accepts a text query and can return matched timestamps. Preserve the source page and segment boundaries.
- UI inspiration with style tokens/snippets belongs to the separate `octen-design` skill.

A thumbnail or search hit does not establish licensing, provenance or the video's spoken content. Inspect the source and retrieve captions before quoting speech.

## YouTube captions first

Choose creator-provided captions before generated captions. Stop on bot detection or HTTP 429; changing clients or proxies is not a continuation strategy after a block.

```bash
yt-dlp --list-subs --skip-download "$URL"
WORK=$(mktemp -d)
yt-dlp --skip-download --write-subs --write-auto-subs \
  --sub-langs en --sub-format json3 -o "$WORK/captions.%(ext)s" "$URL"
```

Choose the requested/source language and inspect the actual downloaded filename. Save into the relevant project, or `~/Downloads` when no project applies. Use `Channel_Title.txt` with unsafe characters replaced by `_`; use the video ID if metadata is unavailable. Do not overwrite an existing transcript without checking it.

Flatten the chosen JSON3 file only when plain text is requested. Keep the original timing data when citations need timestamps:

```bash
python3 - "$CAPTION_FILE" "$OUTPUT_FILE" <<'PY'
import html
import json
from pathlib import Path
import re
import sys
payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
parts = [
    ''.join(segment.get('utf8', '') for segment in event.get('segs') or [])
    for event in payload.get('events', [])
]
transcript = re.sub(r'\s+', ' ', html.unescape(' '.join(
    part.strip() for part in parts if part.strip()
))).strip()
if not transcript:
    raise SystemExit('Caption track contains no transcript text')
Path(sys.argv[2]).write_text(transcript + '\n', encoding='utf-8')
print(sys.argv[2])
PY
```

The installed alternative caption client accepts a video ID, not a URL:

```bash
youtube_transcript_api VIDEO_ID --list-transcripts
youtube_transcript_api VIDEO_ID --languages en --exclude-generated --format text
youtube_transcript_api VIDEO_ID --languages en --format json
```

JSON preserves segment data; text removes timestamps. Cookie authentication is disabled in the inspected client. Use this as an available client, not to retry around an access block.

## No usable captions

When captions are genuinely absent, local audio transcription is the fallback:

```bash
yt-dlp -f ba -x --audio-format mp3 -o "$WORK/audio.%(ext)s" "$URL"
whisper "$WORK/audio.mp3" --model turbo --output_format txt --output_dir "$WORK"
```

Pass a known language with `--language`; use JSON output to preserve segments. Local transcription can be slow and may download model weights. A smaller model reduces memory needs but can reduce accuracy. Keep hosted/paid transcription opt-in; never escalate to it automatically after a block. If a tool's extractor is obsolete, report the version/error and use its actual installation method for an authorized update, not an automatic package upgrade.

Read the transcript's beginning and a relevant passage before claiming success. Distinguish captions from machine transcription, cite timestamps where available, and remove only temporary files created by this workflow after preserving the requested output.

Evidence: prior caption workflow and inspected installed transcript-client argument definitions. YouTube and Whisper were not live-tested during consolidation; access restrictions remain possible.
