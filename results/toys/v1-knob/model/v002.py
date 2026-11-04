def predict(probe):
    """Model v2: baseline (0,0,1.0); switch on shifts y to 10."""
    try:
        a = float(probe.get("a", 0))
        b = float(probe.get("b", 0))
        c = float(probe.get("c", 0))
        sw = probe.get("switch", "off")
    except Exception:
        return {"x": 0.0, "y": 0.0, "size": 1.0}
    x = 0.0
    y = 0.0
    size = 1.0
    if sw == "on":
        y = 10.0
    return {"x": x, "y": y, "size": size}
