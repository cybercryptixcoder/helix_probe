def predict(probe):
    """Model: f(x) = x + 'xI'."""
    try:
        return {"outputs": [str(x) + "xI" for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
