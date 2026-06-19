# OpenAI Python API library

*Offline excerpt of the official documentation (github.com/openai/openai-python),
trimmed to what you need for this exam. In this exam the model is served through
an **OpenAI-compatible** endpoint, so the same library is used with a custom
`base_url`.*

The library provides access to the chat-completions API from Python 3.9+. **You
do not need to write the API call** — `rag.py` already wraps it in `call_llm()`.
This page is here so you understand what that helper does.

## Creating a client

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL"),   # OpenAI-compatible endpoint
)
```

You can provide the key with the `api_key` argument or the `OPENAI_API_KEY`
environment variable. In this repo those values come from your `.env` file.

## Generating text — Chat Completions API

```python
completion = client.chat.completions.create(
    model="gpt-5.4-nano",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Your question here"},
    ],
)
print(completion.choices[0].message.content)
```

### `messages`

A list of `{"role": ..., "content": ...}` dicts. Roles:

- `"system"` — high-level instructions for how the model should behave.
- `"user"` — the user's input / question.
- `"assistant"` — a previous model reply (for multi-turn chats).

### `temperature`

Sampling temperature (typically 0–2). Lower is more focused and deterministic;
for grounded question-answering, a low value such as `0` is sensible.

### Reading the response

```python
text = completion.choices[0].message.content
```

## How this is used in the exam

`rag.py` already contains this helper — you simply call it with your prompt:

```python
def call_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
```

**In `answer_question` (TODO 3) you build a prompt string and pass it to
`call_llm(prompt)`; it returns the model's answer as a string.** What goes *in*
the prompt — the retrieved context and your instructions — is up to you.

## Handling errors

When the API returns a non-success status code (4xx/5xx) a subclass of
`openai.APIStatusError` is raised; when the server can't be reached,
`openai.APIConnectionError`. All inherit from `openai.APIError`.

| Status | Error type |
| ------ | ---------- |
| 401    | `AuthenticationError`  (check your API key) |
| 404    | `NotFoundError`        (check the model name / base URL) |
| 429    | `RateLimitError`       (slow down / back off) |
| >=500  | `InternalServerError`  |
