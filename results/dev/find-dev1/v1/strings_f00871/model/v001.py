def predict(probe):
    """Model: reverse each input string and append 'I'."""
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [str(x)[::-1] + "I" for x in inputs]}
    except Exception:
        return {"outputs": []}
