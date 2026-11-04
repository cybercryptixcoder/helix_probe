def predict(probe):
    # Insert "5" at index ceil(len/2) [E1, E2]
    # Append last character of original string [E1, E2]
    # Empty string raises IndexError (because it tries to append s[-1]) [E2]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        if n == 0:
            out.append("ERROR: IndexError")
            continue
        mid = (n + 1) // 2
        r = s[:mid] + "5" + s[mid:]
        r += s[-1]
        out.append(r)
    return {"outputs": out}
