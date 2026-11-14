"""Task: the ordinal suffix. After a number written in digits, GPT-2 small continues with "st", "nd", "rd" or "th"
(1st, 2nd, 3rd, 4th, 11th, 21st, 112th ...). How does it pick?

A task file defines:  ID, MODEL, ANSWERS, X_NAMES, SPLIT_BY (optional), TEXT (what the reader is shown about the
inputs), CONTEXT / ANSWER (hidden from a blinded reader), and build(tok) -> list of (prompt text, x row, roles).
"""
ID = "gpt2_ordinal"
MODEL = "gpt2"
ANSWERS = ["st", "nd", "rd", "th"]          # the answer tokens; the network's output is their logits at the last position
X_NAMES = ["n", "template"]
SPLIT_BY = "n"                              # the judge fits on some values of n and tests on the others
TEMPLATES = ["It was the {}", "This is the {}", "He finished the {}", "Then on the {}"]
TEXT = ("Each prompt is a short phrase that ends in a number n written in digits (one token). "
        "x[:, 0] = n; x[:, 1] = which of the %d phrase templates (%s). Roles: num = end = the number's position (the last token)."
        % (len(TEMPLATES), "; ".join(f'{i}: "{t.format("<n>")}"' for i, t in enumerate(TEMPLATES))))
CONTEXT = "The prompts end in a number; the answer tokens are the English ordinal suffixes."
ANSWER = "GPT-2 small continues a number with its ordinal suffix: st / nd / rd / th by the last digit, with th for 11, 12, 13."


def build(tok):
    bos = tok.bos_token or ""
    rows = []
    for n in range(0, 1000):
        if len(tok.encode(f" {n}")) != 1:
            continue
        for t, tmpl in enumerate(TEMPLATES):
            rows.append((bos + tmpl.format(n), [n, t], {"num": -1}))
    return rows
