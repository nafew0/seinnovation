# Python — strings, lists, loops & files

*Offline excerpt of the official Python documentation (docs.python.org/3),
trimmed to the parts you need for the chunking and prompt-building steps.*

---

## String methods

Strings are immutable; every method below returns a **new** string (or a list),
it does not change the original.

### `str.split(sep=None, maxsplit=-1)`

Return a list of the words in the string, using *sep* as the delimiter. If *sep*
is not given or is `None`, runs of consecutive whitespace are treated as a single
separator.

```python
>>> "a,b,c".split(",")
['a', 'b', 'c']
>>> "one two   three".split()
['one', 'two', 'three']
>>> text.split("\n\n")     # split into paragraphs on blank lines
```

### `str.splitlines(keepends=False)`

Return a list of the lines in the string, breaking at line boundaries.

```python
>>> "line 1\nline 2\nline 3".splitlines()
['line 1', 'line 2', 'line 3']
```

### `str.strip([chars])`

Return a copy of the string with leading and trailing characters removed
(whitespace if *chars* is omitted). `lstrip()` / `rstrip()` strip one side only.

```python
>>> "   hello  ".strip()
'hello'
```

### `str.lower()`

Return a copy of the string with all cased characters lowercased.

### `str.join(iterable)`

Concatenate the strings in *iterable*, using the string as the separator.

```python
>>> ", ".join(["spam", "spam", "spam"])
'spam, spam, spam'
>>> "\n\n".join(["chunk one", "chunk two"])
'chunk one\n\nchunk two'
```

### `str.startswith(prefix)` / `str.endswith(suffix)`

Return `True` if the string starts (or ends) with the given substring.

### `str.replace(old, new)` / `in`

```python
>>> "a-b-c".replace("-", " ")
'a b c'
>>> "cat" in "concatenate"
True
```

---

## f-strings (formatted string literals)

Prefix a string with `f` and put expressions inside `{ }`. This is the easiest
way to assemble a longer string out of several pieces (useful when you build a
prompt out of a question and some context).

```python
city = "Dhaka"
count = 3
note = f"There are {count} sites in {city}."
# 'There are 3 sites in Dhaka.'
```

For long strings, join several pieces with implicit concatenation:

```python
message = (
    "Dear applicant,\n\n"
    f"Thank you for contacting {city}.\n"
    "We will reply soon."
)
```

---

## Lists & loops

```python
chunks = []                                 # empty list
chunks.append(("file.txt", "some text"))    # add an item (here, a tuple)

for filename, text in chunks:               # unpack each tuple
    print(filename, text)
```

### List comprehensions

```python
texts = [text for (filename, text) in chunks]
non_empty = [p.strip() for p in paragraphs if p.strip()]
```

---

## Reading files

```python
with open("documents/about.txt", "r", encoding="utf-8") as f:
    content = f.read()          # whole file as one string
```

*(In this exam, file loading is already done for you by `load_documents()` in
`rag.py` — this section is here for reference.)*
