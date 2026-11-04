def predict(probe):
    # Rules (from evidence):
    # - Each whitespace-separated word is reversed in place [E1, E2]
    # - The LAST word additionally gets its first (reversed) char prepended [E1, E2]
    # - Whitespace runs are collapsed to a single space [E2: "hello  world"->"olleh ddlrow"]
    # - Leading/trailing whitespace is stripped [E2: "  hello"->"oolleh", "hello  "->"olleh"]
    # - Punctuation is treated as part of the word (not a separator) [E2: "hello world!"->"olleh !!dlrow", "hello, world"->",olleh ddlrow"]
    # - Empty input -> empty output [E2: "hello  "->"olleh" implies strip; empty string -> ""]
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
            rev[-1] = rev[-1][0] + rev[-1]
            outs.append(" ".join(rev))
        return {"outputs": outs}
    except Exception:
        return {"outputs": ["" for _ in probe.get("inputs", [])]}
