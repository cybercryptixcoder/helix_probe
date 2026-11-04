def predict(probe):
    """Model: strip leading/trailing whitespace, then reverse the characters."""
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [s.strip()[::-1] for s in inputs]}
    except Exception:
        return {"outputs": []}
