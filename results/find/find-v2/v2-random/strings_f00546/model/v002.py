def predict(probe):
    # Split on whitespace, drop empty tokens [E1, E2]
    # Reverse each word individually, keep word order [E1, E2]
    # Insert "lmKA" before the LAST word [E1, E2]
    # Special case: trailing whitespace -> lmKA goes at the very end,
    #   after the last (reversed) word, not before it [E2: "banana data banana "
    #   -> "ananab atad ananab lmKA"]. Leading whitespace is dropped [E1].
    # So: if the input ends with whitespace, the "last word" slot is an empty
    #   trailing token, and lmKA is placed there (at the end).
    try:
        s = probe["inputs"]
    except Exception:
        return {"outputs": []}
    outs = []
    for x in s:
        try:
            words = x.split()
            if not words:
                outs.append("lmKA")
                continue
            rev = [w[::-1] for w in words]
            if x != x.rstrip():
                # trailing whitespace: lmKA at the very end
                outs.append(" ".join(rev) + " lmKA")
            else:
                rev[-1] = "lmKA" + rev[-1]
                outs.append(" ".join(rev))
        except Exception:
            outs.append("")
    return {"outputs": outs}
