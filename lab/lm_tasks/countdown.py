"""Task: counting up and counting down. GPT-2 small continues "41, 42, 43, 44," with 45 and "44, 43, 42, 41," with 40.
Counting up (successor heads, the increasing-sequence circuit) is in the literature; how the model decides the
direction and how it counts DOWN is not."""
ID = "gpt2_countdown"
MODEL = "gpt2"
NUMBERS = list(range(0, 362))                       # " 0" .. " 361" are single tokens in GPT-2's vocabulary
ANSWERS = [f" {k}" for k in NUMBERS]                # the network's output: the logits of these 362 number tokens
X_NAMES = ["n1", "n2", "n3", "n4", "prefix"]
PREFIXES = ["Numbers:", "Count:", "List:", "Order:"]
LAST = range(20, 120)                               # the last number shown
TEXT = ("Each prompt is a short prefix followed by four numbers separated by commas, ending in a comma, for example "
        '"Count: 57, 58, 59, 60,". x[:, 0..3] = the four numbers n1..n4 in order; x[:, 4] = which prefix (%s). '
        "Token positions: 0 <|endoftext|>, 1-2 the prefix, 3 n1, 4 comma, 5 n2, 6 comma, 7 n3, 8 comma, 9 n4, 10 comma (the last token). "
        "Roles: n1, n2, n3, n4 (the number tokens), c1, c2, c3 (the commas after n1..n3), end (the last comma, where the next token is predicted). "
        "The network's output is the logits, at the end position, of the 362 number tokens ' 0' .. ' 361' (output index k = the number k)."
        % "; ".join(f'{i}: "{p}"' for i, p in enumerate(PREFIXES)))
CONTEXT = "The prompts are runs of consecutive integers, half of them increasing and half decreasing."
ANSWER = "GPT-2 small continues the run: n4 + 1 after an increasing run, n4 - 1 after a decreasing run."


def build(tok):
    rows = []
    for last in LAST:
        for d in (1, -1):
            seq = [last - d * (3 - i) for i in range(4)]
            for p, pre in enumerate(PREFIXES):
                text = (tok.bos_token or "") + pre + " " + ", ".join(str(v) for v in seq) + ","
                rows.append((text, seq + [p], {"n1": 3, "c1": 4, "n2": 5, "c2": 6, "n3": 7, "c3": 8, "n4": 9, "end": 10}))
    return rows
