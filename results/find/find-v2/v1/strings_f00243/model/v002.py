def predict(probe):
    """Insert 'Z' at index 0 for length<=1, at index 1 for length>=2."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            s = str(s)
            if len(s) <= 1:
                outputs.append("Z" + s)
            else:
                outputs.append(s[:1] + "Z" + s[1:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
