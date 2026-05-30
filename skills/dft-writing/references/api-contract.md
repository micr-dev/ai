# DFT Writing Demo API Contract

Source inspected: `https://dft.rosmine.ai/`, a Gradio 5.31.0 Blocks app with API prefix `/gradio_api`.

## Components

Relevant component ids:

| Id | Purpose |
| --- | --- |
| 13 | Prompt textbox |
| 15 | Outline textbox |
| 19 | Style textbox |
| 23 | Use case textbox |
| 27 | Approximate output token length slider |
| 37 | DFT output textbox |
| 43 | Example 1 button |
| 44 | Example 2 button |
| 45 | Example 3 button |

## Function Indexes

The app sets `api_name: false` and exposes empty `/gradio_api/info` endpoint maps. Use `fn_index` through `/gradio_api/run/predict`.

| fn_index | UI action | Inputs | Primary output |
| --- | --- | --- | --- |
| 6 | Generate good | prompt, outline, style, use_case, target_tokens, allow_emdash, warning_seen, session_id | data[0] |
| 7 | Generate fast | prompt, outline, style, use_case, target_tokens, allow_emdash, warning_seen, session_id | data[0] |
| 14 | Example 1 | none | prompt, outline, style, use_case, target_tokens |
| 15 | Example 2 | none | prompt, outline, style, use_case, target_tokens |
| 16 | Example 3 | none | prompt, outline, style, use_case, target_tokens |

Generation request body:

```json
{
  "data": [
    "Prompt text",
    "Outline text",
    "Clear, informative",
    "Short blog post",
    300,
    false,
    true,
    "session-id"
  ],
  "event_data": null,
  "fn_index": 7,
  "session_hash": "session-id"
}
```

Example request body:

```json
{
  "data": [],
  "event_data": null,
  "fn_index": 14,
  "session_hash": "session-id"
}
```

## Observed Examples

Example 1:

- Prompt: `How has digital publishing transformed the accessibility and dissemination of scientific knowledge, and what does the future of scholarly communication look like in an era of open access and automated information sharing?`
- Style: `Inquisitive, Analytical, Conversational`
- Use case: `Academic Article`
- Tokens: `700`

Example 2:

- Prompt: `Explore the global water crisis as both an ecological and social justice issue, examining how the commercialization of water threatens human rights and environmental sustainability.`
- Style: `Advocacy, Urgent, Ethical`
- Use case: `Advocacy Document`
- Tokens: `900`

Example 3:

- Prompt: `Reflect on the historical significance and cultural legacy of Teotihuacan by exploring its 100 years of archaeological research, recent discoveries, and the efforts to preserve and celebrate this World Heritage Site.`
- Style: `Informative, academic, chronological`
- Use case: `None`
- Tokens: `600`

## Caveats

- `/gradio_api/call/14` returned `FnIndexInferError: Could not infer function index for API name: 14`; `run/predict` succeeded.
- The UI warns that the model is hosted on slower GPUs and can take about a minute.
- The UI's copy button may alter copied text, but direct API responses are raw JSON and are not copied through that UI hook.
