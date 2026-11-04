def predict(probe):
    # Insert 'f' at position len//2 [E1: all 6 inputs]
    # Duplicate the last character [E1: all 6 inputs]
    # Empty string: return empty (?) [no evidence]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append("")
            continue
        m = len(s) // 2
        out.append(s[:m] + "f" + s[m:] + s[-1])
    return {"outputs": out}
