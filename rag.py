"""
Mini Doc-QA - starter scaffold
BdREN Recruitment Exam: System Engineer (Innovation)

Goal:
    Complete the three TODO sections so that running

        python rag.py

    reads the questions in questions.txt, finds the most relevant content in the
    documents/ folder, asks the model to answer using ONLY that content, and
    writes output.txt in the required format.

You only need to edit the parts marked  # TODO .
The helpers below (loading files, calling the model, writing output) are done for
you. Do NOT change write_output() - the output format is graded.

See the documentation/ folder for guidance on each TODO.
"""

import os
import glob
from openai import OpenAI

# Load OPENAI_API_KEY / OPENAI_BASE_URL / MODEL from a local .env file if present.
# (Optional: you may also set them as real environment variables.)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Configuration  (the full API key will be given to you on exam day - put it in .env)
# ---------------------------------------------------------------------------
API_KEY = os.environ.get("OPENAI_API_KEY", "your-exam-api-key-here")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.environ.get("MODEL", "gpt-5.4-nano")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

DOCS_DIR = "documents"
QUESTIONS_FILE = "questions.txt"
OUTPUT_FILE = "output.txt"


# ---------------------------------------------------------------------------
# Provided helper 1 - load all documents. Returns a list of (filename, text).
# ---------------------------------------------------------------------------
def load_documents(docs_dir=DOCS_DIR):
    documents = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "*.txt"))):
        with open(path, "r", encoding="utf-8") as f:
            documents.append((os.path.basename(path), f.read()))
    return documents


# ---------------------------------------------------------------------------
# Provided helper 2 - load the questions (one per line).
# ---------------------------------------------------------------------------
def load_questions(path=QUESTIONS_FILE):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# ---------------------------------------------------------------------------
# Provided helper 3 - call the language model with a prompt and return its text.
# (You do NOT need to write the API call - just call this from TODO 3.)
# ---------------------------------------------------------------------------
def call_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Provided helper 4 - write output.txt in the required format. DO NOT CHANGE.
# results: a list of dicts with keys "question", "answer", "source".
# ---------------------------------------------------------------------------
def write_output(results, path=OUTPUT_FILE):
    with open(path, "w", encoding="utf-8") as f:
        for i, r in enumerate(results, start=1):
            f.write(f"Q{i}: {r['question']}\n")
            f.write(f"Answer: {r['answer']}\n")
            f.write(f"Source: {r['source']}\n")
            f.write("---\n")
    print(f"Wrote {len(results)} answers to {path}")


# ===========================================================================
# TODO 1 - split the documents into chunks.
#
#   Input : documents -> list of (filename, text)
#   Return: list of (filename, chunk_text)
#
#   Why: retrieving a small, relevant piece works far better than feeding a whole
#   file to the model. Choose a unit that keeps one idea together - for example a
#   paragraph, or a fixed number of sentences/words. Keep each chunk paired with
#   the filename it came from, so you can report the source later (TODO 3).
#
#   Worth thinking about: a very short line on its own (such as a heading) makes a
#   poor chunk - the answer usually lives in the text that follows it.
#
#   Docs: documentation/python-strings.md  (splitting & cleaning text)
# ===========================================================================
def chunk_documents(documents):
    chunks = []
    # TODO: build and return the list of (filename, chunk_text)
    return chunks


# ===========================================================================
# TODO 2 - retrieve the chunk(s) most relevant to a question.
#
#   Input : question (str), chunks -> list of (filename, chunk_text)
#   Return: a list of (filename, chunk_text) - the best match, or the top few
#
#   Approach: turn the chunks and the question into vectors and rank chunks by
#   similarity to the question. You can start simple (count shared words) and then
#   improve it (TF-IDF + cosine similarity).
#
#   Worth thinking about: returning only ONE chunk can miss the answer to a
#   "name all the ..." style question - returning the top few is often safer. A
#   minimum score can also let a question with no good match return nothing.
#
#   Docs: documentation/scikit-learn-text.md  (TF-IDF + cosine similarity)
# ===========================================================================
def retrieve(question, chunks):
    # TODO: score the chunks against the question and return the best one(s)
    return []


# ===========================================================================
# TODO 3 - build the prompt, call the model, and return (answer, source).
#
#   Input : question (str), retrieved -> list of (filename, chunk_text)
#   Return: (answer_text, source_filename)
#
#   Build a prompt that gives the model the retrieved text as context and asks it
#   to answer the question using ONLY that context. Answer every part of the
#   question. Then pass your prompt to the provided call_llm(prompt).
#
#   Worth thinking about: if nothing relevant was retrieved (or the context does
#   not actually contain the answer), the answer should say it is not in the
#   documents and the source can be "N/A" - do not let the model invent facts.
#   Make sure the source you return is the file the answer really came from.
#
#   Docs: documentation/python-strings.md (f-strings) and
#         documentation/openai-python.md  (how call_llm works)
# ===========================================================================
def answer_question(question, retrieved):
    answer = ""
    source = ""
    # TODO: build the prompt, call the model, and set answer + source
    return answer, source


# ---------------------------------------------------------------------------
# Main - wires everything together. (Provided - you should not need to edit.)
# ---------------------------------------------------------------------------
def main():
    documents = load_documents()
    questions = load_questions()
    chunks = chunk_documents(documents)

    results = []
    for q in questions:
        retrieved = retrieve(q, chunks)
        answer, source = answer_question(q, retrieved)
        results.append({"question": q, "answer": answer, "source": source})

    write_output(results)


if __name__ == "__main__":
    main()
