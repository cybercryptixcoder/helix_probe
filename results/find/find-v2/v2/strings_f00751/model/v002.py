def predict(probe):
    # Insert 'i' at index len(s)//2 [E1, E2, E3]
    # Trailing whitespace is stripped from the output [E3: "banana data banana " -> "banana daita banana"]
    out = []
    for s in probe.get("inputs", []):
        if not isinstance(s, str):
            s = str(s)
        mid = len(s) // 2
        out.append((s[:mid] + "i" + s[mid:]).rstrip())
    return {"outputs": out}
