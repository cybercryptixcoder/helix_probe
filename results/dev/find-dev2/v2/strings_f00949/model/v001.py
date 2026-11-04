def predict(probe):
    # Insert "I8" at middle (floor(len/2)) for odd-length strings [E1]
    # Insert "8I" at middle (floor(len/2)) for even-length strings [E1]
    # Position = len(s)//2 for all cases [E1]
    out = []
    for s in probe.get("inputs", []):
        pos = len(s) // 2
        if len(s) % 2 == 0:
            out.append(s[:pos] + "8I" + s[pos:])
        else:
            out.append(s[:pos] + "I8" + s[pos:])
    return {"outputs": out}
