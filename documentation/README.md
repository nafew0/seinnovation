# Offline Documentation

There is **no internet access** during this exam. This folder contains offline
copies of the official documentation you need, trimmed to the relevant parts.
They explain the tools — you write the code.

## The task in three steps

Your program answers each question by:

1. **splitting** the documents into chunks,
2. **retrieving** the chunk(s) most relevant to the question, and
3. **grounding** the model: asking it to answer using *only* that retrieved
   text, and reporting which document the answer came from.

## What's here

| File | Use it for |
|------|------------|
| [`python-strings.md`](python-strings.md) | Splitting and cleaning text, f-strings, lists, loops, reading files — **chunking** (TODO 1) and building the prompt (TODO 3). |
| [`scikit-learn-text.md`](scikit-learn-text.md) | Turning text into **TF-IDF** vectors and ranking by **cosine similarity** — the **retrieval** step (TODO 2). |
| [`openai-python.md`](openai-python.md) | How the model call works. You call the provided `call_llm(prompt)`; you do **not** write the API call yourself (TODO 3). |

## Which doc for which `# TODO`

- **TODO 1 — `chunk_documents`** → `python-strings.md`
- **TODO 2 — `retrieve`** → `scikit-learn-text.md`
- **TODO 3 — `answer_question`** → `python-strings.md` (f-strings) + `openai-python.md`

## Things worth getting right (this is where marks are won)

- A heading on its own is a poor chunk — the answer usually lives in the text
  **after** the heading, so don't strand it in a chunk of its own.
- The single best chunk isn't always enough: a *"name all the …"* question may
  need more than the top one. Think about how many chunks to return.
- **Ground the model.** Tell it to use **only** the provided context, and to say
  the answer isn't in the documents rather than guess. Some questions ask for
  something the documents don't actually state — answer those honestly.
- Report the **source file the answer really came from**, not just the first
  file you happened to look at.
