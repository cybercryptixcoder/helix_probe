def predict(probe):
    # y ≈ 16.796 * |x| for all x in [-128,128] [E1]
    # (residuals within ±2.2, likely noise; no region detected yet)
    xs = probe.get("x", [])
    return {"y": [16.796 * abs(x) for x in xs]}
