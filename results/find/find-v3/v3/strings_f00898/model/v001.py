def predict(probe):
    # Insert 'f' at index len//2, then append the original last char [E1]
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append("f")
            continue
        m = len(s) // 2
        out.append(s[:m] + "f" + s[m:] + s[-1])
    return {"outputs": out}
