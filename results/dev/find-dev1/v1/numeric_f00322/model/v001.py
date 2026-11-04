def predict(probe):
    """Model: f(x) = 53.0 for all x."""
    try:
        xs = probe.get("x", [])
        return {"y": [53.0 for _ in xs]}
    except Exception:
        return {"y": []}
