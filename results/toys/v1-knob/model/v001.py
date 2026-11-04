def predict(probe):
    """Baseline model: only known that all-min/off gives (0,0,1.0)."""
    try:
        a = float(probe.get("a", 0))
        b = float(probe.get("b", 0))
        c = float(probe.get("c", 0))
        sw = probe.get("switch", "off")
    except Exception:
        return {"x": 0.0, "y": 0.0, "size": 1.0}
    # No evidence yet on how controls affect the dot; assume baseline.
    return {"x": 0.0, "y": 0.0, "size": 1.0}
