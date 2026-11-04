def predict(probe):
    """Model v4: x = 2a - b; size = 1 + 0.5a; switch on sets y=10."""
    try:
        a = float(probe.get("a", 0))
        b = float(probe.get("b", 0))
        c = float(probe.get("c", 0))
        sw = probe.get("switch", "off")
    except Exception:
        return {"x": 0.0, "y": 0.0, "size": 1.0}
    x = 2.0 * a - b
    y = 0.0
    size = 1.0 + 0.5 * a
    if sw == "on":
        y = 10.0
    return {"x": x, "y": y, "size": size}
