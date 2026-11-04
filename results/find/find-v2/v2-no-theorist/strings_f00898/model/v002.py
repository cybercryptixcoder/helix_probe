def predict(probe):
    # Insert 'f' at position len//2 [E1-E8]
    # Duplicate the last character [E1-E8]
    # Empty string: 'f' inserted at 0, then last char duplicated -> "ff" [E8]
    out = []
    for s in probe["inputs"]:
        m = len(s) // 2
        out.append(s[:m] + "f" + s[m:] + (s[-1] if s else "f"))
    return {"outputs": out}
