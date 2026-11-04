def predict(probe):
    # Only one observation exists: all dials at 5, switch off -> dot at (5,5), size 1.0 [E1]
    # Simplest hypothesis: the dot sits at (a, b) with a fixed size, switch does nothing [E1]
    # x = a, y = b, size = 1.0 (no evidence yet of c or switch affecting anything)
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    return {"x": a, "y": b, "size": 1.0}
