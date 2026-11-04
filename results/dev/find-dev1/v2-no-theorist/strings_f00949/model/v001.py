def predict(probe):
    # Insert "I8" at floor(n/2) for odd-length strings [E1]
    # Insert "8I" at n/2 for even-length strings [E1]
    # Empty string -> "8I" (even, k=0) [E1]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        k = n // 2
        ins = "8I" if n % 2 == 0 else "I8"
        out.append(s[:k] + ins + s[k:])
    return {"outputs": out}
