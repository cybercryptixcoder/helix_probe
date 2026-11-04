def predict(probe):
    """Split on whitespace runs, reverse each segment, join with single spaces."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            segs = s.split()
            outputs.append(" ".join(seg[::-1] for seg in segs))
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
