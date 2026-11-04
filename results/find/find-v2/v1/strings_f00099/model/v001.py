def predict(probe):
    """Model: the box reverses the characters of each input string."""
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [s[::-1] for s in inputs]}
    except Exception:
        return {"outputs": []}
