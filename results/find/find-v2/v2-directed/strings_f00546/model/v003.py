import re

def predict(probe):
    # Model of the black box:
    # - Strip leading whitespace [E2: "  hello  " -> "olleh lmKA"]
    # - Split remaining string on runs of whitespace (space, tab, newline, NBSP, em-space) [E4]
    # - Trailing whitespace yields one trailing empty token [E2: "  hello  " -> tokens ["hello",""]]
    # - Reverse the characters of each token [E1: "hello" -> "olleh"]
    # - Join tokens with a single space [E2: "a  b" -> "a lmKAb"]
    # - Prefix the LAST token with "lmKA" [E1: "a b c" -> "a b lmKAc"]
    # - Punctuation stays inside tokens and gets reversed with them [E3: "hello,world" -> "lmKAdlrow,olleh"]
    # - Empty input -> "lmKA" [E1: "" -> "lmKA"]
    try:
        s = probe.get("inputs", [])
    except Exception:
        return {"outputs": []}
    outputs = []
    for x in s:
        try:
            if not isinstance(x, str):
                x = str(x)
            stripped = x.lstrip()
            tokens = re.split(r'\s+', stripped)
            rev = [t[::-1] for t in tokens]
            if rev:
                rev[-1] = "lmKA" + rev[-1]
            outputs.append(" ".join(rev))
        except Exception:
            outputs.append("")
    return {"outputs": outputs}
