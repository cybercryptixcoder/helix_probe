def predict(probe):
    """Model: f(x) reverses the characters of x."""
    try:
        return {"outputs": [s[::-1] for s in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
