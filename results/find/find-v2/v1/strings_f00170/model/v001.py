def predict(probe):
    """Model: f(x) = 'k' + reverse(x)."""
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": ["k" + s[::-1] for s in inputs]}
    except Exception:
        return {"outputs": []}
