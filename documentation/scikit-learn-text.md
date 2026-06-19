# scikit-learn — Text features & similarity

*Offline excerpt of the official scikit-learn documentation
(scikit-learn.org/stable), trimmed to what you need for the retrieval step. It
describes the tools; combining them into your `retrieve` function is your task.*

This covers two tools:

- **`TfidfVectorizer`** — turns a collection of text documents into a matrix of
  TF-IDF feature vectors.
- **`cosine_similarity`** — measures how similar two vectors are (1.0 = very
  similar, 0.0 = unrelated).

Together they let you rank documents by how relevant they are to a question.

---

## Background: TF-IDF in one paragraph

**TF-IDF** (term frequency–inverse document frequency) gives each word a weight
that is high when the word appears often in one document but rarely across all
documents. Each document becomes a vector of these weights. To find the document
most relevant to a query, you turn the query into a vector the same way and
compare vectors with **cosine similarity**.

---

## `TfidfVectorizer`

```text
class sklearn.feature_extraction.text.TfidfVectorizer(
    *, input='content', encoding='utf-8', lowercase=True, preprocessor=None,
    tokenizer=None, analyzer='word', stop_words=None,
    token_pattern='(?u)\b\w\w+\b', ngram_range=(1, 1), max_df=1.0, min_df=1,
    max_features=None, vocabulary=None, binary=False, norm='l2',
    use_idf=True, smooth_idf=True, sublinear_tf=False)
```

Convert a collection of raw documents to a matrix of TF-IDF features.

### Selected parameters

- **lowercase** : bool, default=True — Convert all characters to lowercase
  before tokenizing.
- **stop_words** : {'english'}, list, default=None — If `'english'`, a built-in
  English stop-word list is removed.
- **ngram_range** : tuple `(min_n, max_n)`, default=`(1, 1)` — The range of
  n-grams to extract. `(1, 1)` is unigrams only; `(1, 2)` adds bigrams (pairs of
  adjacent words), which can help match short phrases.
- **min_df** / **max_df** : ignore terms that are too rare / too common.

### Key methods

- **`fit_transform(raw_documents)`** — Learn the vocabulary and IDF, and return
  the document-term matrix (shape `(n_samples, n_features)`).
- **`transform(raw_documents)`** — Transform new documents using the vocabulary
  already learned. Use this for the **query** so it shares the same vocabulary.
- **`get_feature_names_out()`** — Return the list of feature (token) names.

> Important: call `fit_transform` on your documents, then `transform` on the
> query — both must use the **same** vectorizer object so the vectors line up.

### Example (from the official docs)

```python
>>> from sklearn.feature_extraction.text import TfidfVectorizer
>>> corpus = [
...     'This is the first document.',
...     'This document is the second document.',
...     'And this is the third one.',
...     'Is this the first document?',
... ]
>>> vectorizer = TfidfVectorizer()
>>> X = vectorizer.fit_transform(corpus)
>>> X.shape
(4, 9)
```

---

## `cosine_similarity`

```text
sklearn.metrics.pairwise.cosine_similarity(X, Y=None, dense_output=True)
```

Compute cosine similarity between samples in `X` and `Y`:

```text
K(X, Y) = <X, Y> / (||X|| * ||Y||)
```

- **X**, **Y** : array-like or sparse matrices of shape `(n_samples, n_features)`.
  If `Y` is `None`, all pairwise similarities within `X` are returned.
- **Returns** : ndarray of shape `(n_samples_X, n_samples_Y)`.

### Example (from the official docs)

```python
>>> from sklearn.metrics.pairwise import cosine_similarity
>>> cosine_similarity([[0, 0, 0], [1, 1, 1]], [[1, 0, 0], [1, 1, 0]])
array([[0.   , 0.   ],
       [0.577, 0.816]])
```

---

## Using these together

The pattern is: `fit_transform` the vectorizer on your texts, `transform` the
query with the **same** vectorizer, then `cosine_similarity` to score the query
against every text. A minimal worked example on a plain list of strings:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

texts = ["text one ...", "text two ...", "text three ..."]
query = "your query"

vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(texts)        # fit on the texts
query_vec = vectorizer.transform([query])       # SAME vectorizer for the query

scores = cosine_similarity(query_vec, matrix)[0]   # one score per text
best = scores.argmax()                             # index of the single best text
print(texts[best], scores[best])
```

Now adapt it for the task — the example does **not** do this for you:

- your chunks are `(filename, chunk_text)` tuples, so vectorise the text part
  while keeping track of which filename each score belongs to;
- decide whether one chunk is enough or you want the top few —
  `scores.argsort()[::-1]` orders the indices highest-first;
- if even the best score is very low, the question probably isn't covered by the
  documents, so you can return nothing.
