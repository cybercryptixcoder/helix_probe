def predict(probe):
    """Model: strip/collapse whitespace, reverse each whitespace-separated word, join with single spaces, append 'I' unless result ends in 'I'."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            s = str(x)
            words = s.split()
            r = " ".join(w[::-1] for w in words)
            outputs.append(r if r.endswith("I") else r + "I")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
