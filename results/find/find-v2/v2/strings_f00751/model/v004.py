def predict(probe):
    # Insert 'i' into s at index len(original)//2 minus the count of leading
    # whitespace stripped [E1, E6, E7, E8]
    # Leading whitespace is stripped before insertion [E6, E7, E8]
    # Trailing whitespace is stripped from the output [E3, E6]
    out = []
    for s in probe.get("inputs", []):
        if not isinstance(s, str):
            s = str(s)
        lead = len(s) - len(s.lstrip())
        mid = len(s) // 2 - lead
        t = s.lstrip()
        out.append((t[:mid] + "i" + t[mid:]).rstrip())
    return {"outputs": out}
