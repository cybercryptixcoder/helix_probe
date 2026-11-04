def predict(probe):
    """Model v9: x = 2a - b; size = 1 + 0.5*max(a,c); y = c, or 10 - c if switch on."""
    try:
        a = float(probe.get("a", 0))
        b = float(probe.get("b", 0))
        c = float(probe.get("c", 0))
        sw = probe.get("switch", "off")
    except Exception:
        return {"x": 0.0, "y": 0.0, "size": 1.0}
    x = 2.0 * a - b
    y = c
    size = 1.0 + 0.5 * max(a, c)
    if sw == "on":
        y = 10.0 - c
    return {"x": x, "y": y, "size": size}
