def predict(probe):
    """Model: f(x) = x + 'T'."""
    try:
        return {"outputs": [str(x) + "T" for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
