def predict(probe):
    """Model v6: x = 2a - b; y = c, or max(c,10) if switch on; size = 1 + 0.5a + 0.5c."""
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
        y = max(y, 10.0)
    return {"x": x, "y": y, "size": size}
