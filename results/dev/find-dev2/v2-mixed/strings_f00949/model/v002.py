def predict(probe):
    # Split at floor(len/2) [E1, E2]
    # Token is "I8" if len is odd, "8I" if len is even [E1, E2]
    outs = []
    for s in probe.get("inputs", []):
        n = len(s)
        p = n // 2
        token = "I8" if n % 2 == 1 else "8I"
        outs.append(s[:p] + token + s[p:])
    return {"outputs": outs}
