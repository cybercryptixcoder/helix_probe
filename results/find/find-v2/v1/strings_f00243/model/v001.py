def predict(probe):
    """Insert 'Z' at index 0 for length<=1, at index 2 for length>=2."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            s = str(s)
            if len(s) <= 1:
                outputs.append("Z" + s)
            else:
                outputs.append(s[:2] + "Z" + s[2:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
