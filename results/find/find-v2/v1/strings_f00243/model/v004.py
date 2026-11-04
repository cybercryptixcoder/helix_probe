def predict(probe):
    """Remove spaces, then insert 'Z' at floor(len/2) of the stripped string (prepend if len<=1)."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            s = str(s)
            t = s.replace(" ", "")
            n = len(t)
            if n == 0:
                outputs.append("Z")
            elif n == 1:
                outputs.append("Z" + t)
            else:
                pos = n // 2
                outputs.append(t[:pos] + "Z" + t[pos:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
