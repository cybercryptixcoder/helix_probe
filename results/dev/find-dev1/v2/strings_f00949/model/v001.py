def predict(probe):
    # Insert "I8" (odd length) or "8I" (even length) at position len//2 [E1]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        marker = "I8" if n % 2 == 1 else "8I"
        p = n // 2
        out.append(s[:p] + marker + s[p:])
    return {"outputs": out}
