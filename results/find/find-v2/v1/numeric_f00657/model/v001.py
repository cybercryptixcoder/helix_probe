def predict(probe):
    """Step function: 18 for x <= 0, -18 for x > 0."""
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(18.0 if x <= 0 else -18.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
