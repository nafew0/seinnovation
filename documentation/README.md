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

## A worked example

A tiny end-to-end run on a toy document, to show how the pieces fit together.
Your task is shaped differently — the real documents arrive as `(filename, text)`
pairs, and your program must also report the **source file** and cope with
questions the documents don't answer — so treat this as a starting point to
adapt, not a drop-in.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def split_into_chunks(text):
    # one chunk per paragraph (blank-line separated)
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def rank(query, chunks, k=2):
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(chunks)
    scores = cosine_similarity(vectorizer.transform([query]), matrix)[0]
    order = scores.argsort()[::-1]          # best score first
    return [chunks[i] for i in order[:k]]   # the top-k chunk texts

def make_prompt(query, context_chunks):
    context = "\n\n".join(context_chunks)
    return f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

# a toy document (your real documents arrive as (filename, text) pairs)
document = (
    "Paris is the capital of France.\n\n"
    "The Eiffel Tower, built in 1889, stands in Paris.\n\n"
    "Mount Everest is the tallest mountain on Earth."
)

chunks = split_into_chunks(document)
top = rank("Where is the Eiffel Tower?", chunks, k=2)
prompt = make_prompt("Where is the Eiffel Tower?", top)
# answer = call_llm(prompt)   # in rag.py, call_llm is already written for you
print(top)
```

To fit it to the exercise you'll need to extend it — the example deliberately
leaves these out:

- it works on plain strings; your chunks are `(filename, chunk_text)` pairs, so
  keep each chunk's filename with it (you report the source in TODO 3);
- `rank` always returns `k` chunks; consider a minimum score so a question with
  no good match can return nothing;
- it neither reports a **source** nor handles **"the answer isn't in the
  documents"** — both are part of the grade;
- the prompt is bare; yours should tell the model to use **only** the context and
  to answer every part of the question.

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
