def predict(probe):
    # Insert a token at position floor(len/2) [E1: level, Zebralower, Hello World function lazy, bananaUPPER, Zebra]
    # Token is "I8" normally [E1: those five]
    # Token is "8I" when the char at the split point (after) is a digit [E1: abc123]  (? only one digit example)
    outs = []
    for s in probe.get("inputs", []):
        n = len(s)
        p = n // 2
        token = "8I" if (p < n and s[p].isdigit()) else "I8"
        outs.append(s[:p] + token + s[p:])
    return {"outputs": outs}
