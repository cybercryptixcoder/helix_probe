def predict(probe):
    """Model: reverse each input string, then append 'I' unless it already ends in 'I'."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            r = str(x)[::-1]
            outputs.append(r if r.endswith("I") else r + "I")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
