def predict(probe):
    """Model v7: x = 2a - b; size = 1 + 0.5a + 0.5c; y = c, or max(c, 10-c) if switch on."""
    try:
        a = float(probe.get("a", 0))
        b = float(probe.get("b", 0))
        c = float(probe.get("c", 0))
        sw = probe.get("switch", "off")
    except Exception:
        return {"x": 0.0, "y": 0.0, "size": 1.0}
    x = 2.0 * a - b
    y = c
    size = 1.0 + 0.5 * a + 0.5 * c
    if sw == "on":
        y = max(c, 10.0 - c)
    return {"x": x, "y": y, "size": size}
