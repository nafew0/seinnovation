# Mini Doc-QA — Starter Repository

Practical task for the BdREN **System Engineer (Innovation)** recruitment exam.

You will complete a small command-line program that answers questions about
BdREN using **only** the documents in this repository, and that reports which
document each answer came from.

## Setup (do this before exam day)

1. Install Python 3.10 or newer.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration.** You will be given an API key (and, if needed, a base URL
   and model name) at the start of the exam. Copy the example env file and fill
   it in:

   ```bash
   cp .env.example .env
   # then edit .env and paste in the key you are given
   ```

   `rag.py` reads these from `.env` / the environment. (You may instead `export`
   them as environment variables.)

4. Check your setup works:

   ```bash
   python -c "import openai, sklearn, numpy; print('ok')"
   ```

## Files

| File / folder      | What it is                                               |
|--------------------|----------------------------------------------------------|
| `documents/`       | The text files the program must answer from.             |
| `questions.txt`    | The 5 questions to answer (one per line).                |
| `rag.py`           | The program. Helpers are done; complete the 3 `# TODO`s. |
| `documentation/`   | Offline docs you need (there is no internet in the exam).|
| `requirements.txt` | Python dependencies.                                     |
| `output.txt`       | Created when you run the program (your deliverable).     |

## What you complete

Open `rag.py` and complete the three sections marked `# TODO`:

1. **`chunk_documents`** — split the documents into smaller chunks.
2. **`retrieve`** — find the most relevant chunk(s) for a question.
3. **`answer_question`** — build the prompt, call the model, and return the
   answer with its source filename.

The file-loading, the model call (`call_llm`), and the output writer are already
written for you. **Do not change `write_output()`** — its format is graded. Each
TODO in `rag.py` points you to the relevant file in `documentation/`.

## Run it

```bash
python rag.py
```

This reads `questions.txt`, answers each question from `documents/`, and writes
`output.txt`.

## Required output format

`output.txt` must contain one block per question, exactly like this:

```
Q1: <the question text>
Answer: <the model's answer>
Source: <the document filename the answer came from>
---
```

## What to submit

- the `output.txt` your program produced, and
- your completed `rag.py`.

Zip your project folder, rename the zip to your roll number, and submit it as
the invigilator instructs.
