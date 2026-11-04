def predict(probe):
    # Rules (from evidence):
    # - Each whitespace-separated word is reversed in place [E1, E2, E3]
    # - The LAST word additionally gets its first (reversed) char prepended [E1, E2, E3]
    # - Whitespace runs are collapsed to a single space [E2: "hello  world"->"olleh ddlrow"]
    # - Leading/trailing whitespace is stripped [E2: "  hello"->"oolleh", "hello  "->"olleh"]
    # - Punctuation is treated as part of the word (not a separator) [E2: "hello world!"->"olleh !!dlrow", "hello, world"->",olleh ddlrow"]
    # - Empty input -> empty output [E2: "hello  "->"olleh" implies strip; empty string -> ""]
    # - The doubling applies to the last word AFTER reversal, using its first char [E1,E2,E3]
    #   BUT: "banana data banana " -> "ananab atad ananab" (no doubling!) [E3]
    #   vs "banana" -> "aananab" (doubling) [E3]
    #   So doubling only when there's a SINGLE word? Check: "lazy"->"yyzal" (single, doubled) [E3]
    #   "test case"->"tset eesac" (two words, doubled) [E3]
    #   "banana data banana " (trailing space, 3 words) -> NOT doubled [E3]
    #   "hello  " -> "olleh" (trailing space, 1 word) -> NOT doubled [E2]
    #   "  hello" -> "oolleh" (leading space, 1 word) -> doubled [E2]
    #   "one two three" -> "eno owt eeerht" (3 words, no trailing space) -> doubled [E2]
    #   Hypothesis: doubling is skipped when input has TRAILING whitespace [E2 "hello  ", E3 "banana data banana "]
    import re
    try:
        outs = []
        for x in probe.get("inputs", []):
            if not isinstance(x, str):
                x = str(x)
            words = x.split()
            if not words:
                outs.append("")
                continue
            rev = [w[::-1] for w in words]
            has_trailing_ws = len(x) > 0 and x[-1].isspace()
            if not has_trailing_ws:
                rev[-1] = rev[-1][0] + rev[-1]
            outs.append(" ".join(rev))
        return {"outputs": outs}
    except Exception:
        return {"outputs": ["" for _ in probe.get("inputs", [])]}
