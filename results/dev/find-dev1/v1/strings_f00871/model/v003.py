def predict(probe):
    """Model: strip whitespace, reverse, then append 'I' unless it already ends in 'I'."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            s = str(x).strip()
            r = s[::-1]
            outputs.append(r if r.endswith("I") else r + "I")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
