def predict(probe):
    """Model: f reverses the input string."""
    try:
        return {"outputs": [s[::-1] for s in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
