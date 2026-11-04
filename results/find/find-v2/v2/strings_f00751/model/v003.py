def predict(probe):
    # Insert 'i' at index len(s)//2 [E1, E2, E3, E4, E5]
    # Leading whitespace is stripped from the input before computing [E6, E7]
    # Trailing whitespace is stripped from the output [E3, E6]
    out = []
    for s in probe.get("inputs", []):
        if not isinstance(s, str):
            s = str(s)
        s = s.lstrip()
        mid = len(s) // 2
        out.append((s[:mid] + "i" + s[mid:]).rstrip())
    return {"outputs": out}
