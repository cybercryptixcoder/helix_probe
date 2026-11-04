def predict(probe):
    """Model: strip leading whitespace, reverse, then strip leading whitespace again."""
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [s.lstrip()[::-1].lstrip() for s in inputs]}
    except Exception:
        return {"outputs": []}
