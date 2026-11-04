def predict(probe):
    """Model: f removes all space characters from the input."""
    try:
        return {"outputs": [str(x).replace(" ", "") for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
