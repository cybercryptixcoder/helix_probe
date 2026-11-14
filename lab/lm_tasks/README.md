# Language-model tasks

A task file tells the constructor **which behaviour of which model** to explain. It is a small Python file; build it
into a target with `python3 lab/lm_build.py lab/lm_tasks/<file>.py` (or the Build button on the constructor page).

```python
ID = "gpt2_mytask"                 # the target's id (a folder lab/models/<ID>/ is written)
MODEL = "gpt2"                     # a Hugging Face checkpoint: GPT-2 family (gpt2, distilgpt2, gpt2-medium, ...) or Pythia ("EleutherAI/pythia-70m", -160m, ...)
ANSWERS = [" is", " are"]          # single tokens; the network's output is their logits at the end position
X_NAMES = ["noun", "template"]     # names of the integer features that describe a prompt (the construction's input x)
TEXT = "what the reader is shown about the prompts and features (no hint of the mechanism)"
CONTEXT = "what the task is (hidden from a blinded reader)"
ANSWER = "the behaviour in one line (hidden from a blinded reader; shown in the told and prior-only modes)"
SPLIT_BY = "noun"                  # optional: fit alignments on some values of this feature and test on the others

def build(tok):                    # tok: the model's tokenizer
    rows = []
    for ...:
        rows.append((prompt_text, [feature values], {"role name": token position, ...}))
    return rows
```

Rules: every prompt must tokenise to the same length (the builder keeps the most common length and reports what it
drops); the feature rows must be unique; roles are token positions (negative counts from the end; `end`, the
position where the answer is predicted, defaults to the last token). Start the prompt with `tok.bos_token`.

What makes a good target: the model does it reliably (check the answer accuracy first); the answer depends on a
**combination** of tokens (if it is a function of one token it is usually already in that token's embedding: see
`ordinal.py` and E13 in `docs/EXPERIMENT_LOG.md`); each value of each input quantity occurs in several prompts.

Files here: `be_verb.py` (is / are / was / were in GPT-2 small), `be_verb_pythia.py` (the same in Pythia-70m), `countdown.py` (counting up and down, the main target of session 3), `ordinal.py` (a small demo).
