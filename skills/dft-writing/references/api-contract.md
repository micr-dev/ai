# Deft Writing API Contract

Source inspected: `https://deftwriting.com/console`, a Next.js app that calls a first-party API route.

## Endpoint

- Method: `POST`
- URL: `https://deftwriting.com/api/generate`
- Request content type: `application/json`
- Streaming response content type: `application/x-ndjson; charset=utf-8`

The retired `https://dft.rosmine.ai/gradio_api/run/predict` endpoint redirects to `https://deftwriting.com` and must not be used as the canonical path.

## Request

New draft:

```json
{
  "prompt": "Write a concise article about clear technical writing.",
  "generationMode": "simple",
  "rewriteInstructions": "",
  "progress": true
}
```

Rewrite:

```json
{
  "prompt": "Existing draft text...",
  "generationMode": "rewrite",
  "rewriteInstructions": "Make this clearer while preserving every factual claim.",
  "progress": true
}
```

## Response Events

The API streams newline-delimited JSON. Known event shapes:

```json
{
  "type": "progress",
  "progress": {
    "phase": "dft",
    "label": "Writing",
    "percent": 50,
    "completedUnits": 2,
    "totalUnits": 4,
    "dftCompletedChunks": 1,
    "dftTotalChunks": 2
  }
}
```

```json
{
  "type": "complete",
  "data": {
    "text": "Generated prose...",
    "metrics": {
      "humanScore": null,
      "lexicalDiversity": 0.8,
      "wordCount": 72,
      "avgSentenceLength": 14.4,
      "readingLevel": 13
    },
    "generationId": "3a328dc4-1eaa-4ac9-b08b-2e214fcc1466"
  }
}
```

Error responses may be JSON objects with `error` and optional `detail`.

## Length Behavior

The current API does not expose a numeric token or word-count field. Length is controlled by prompt steering, for example `Target length: about 1600 words.`

Observed probes:

- Prompt asking for exactly 80 words returned 72 words in 2 DFT chunks.
- Prompt asking for a 1600-word article returned 1879 words in 12 DFT chunks after 161.21 seconds.

Treat requested word counts as approximate. Long drafts can take several minutes.
