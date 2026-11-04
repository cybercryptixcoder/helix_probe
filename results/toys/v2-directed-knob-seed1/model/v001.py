def predict(probe):
    # Only one observation so far [E1]: all dials at 5, switch off -> dot at (5,5), size 1.0.
    # Hypothesis: x tracks a, y tracks b, size is fixed at 1.0, c and switch unknown.
    # ? c and switch may affect x/y/size; no evidence yet.
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    return {"x": a, "y": b, "size": 1.0}
