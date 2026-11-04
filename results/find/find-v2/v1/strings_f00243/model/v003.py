def predict(probe):
    """Insert 'Z' at position floor(len/2) for len>=2 (min 1), prepend for len<=1."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            s = str(s)
            n = len(s)
            if n == 0:
                outputs.append("Z")
            elif n == 1:
                outputs.append("Z" + s)
            else:
                pos = n // 2
                if pos < 1:
                    pos = 1
                outputs.append(s[:pos] + "Z" + s[pos:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
