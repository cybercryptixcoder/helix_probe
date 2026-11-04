def predict(probe):
    """Model: strip both ends, then reverse."""
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [s.strip()[::-1] for s in inputs]}
    except Exception:
        return {"outputs": []}
