def predict(probe):
    # Insert "5" at index ceil(len/2) [E1]
    # Append last character of original string [E1]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        mid = (n + 1) // 2
        r = s[:mid] + "5" + s[mid:]
        if n > 0:
            r += s[-1]
        out.append(r)
    return {"outputs": out}
