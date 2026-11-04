def predict(probe):
    # A: for x >= -9.35: y = 8 - 9.6*x exactly [E2, E3, E4, E5, E6]
    # B: for x <= -9.4: y ≈ 8 with noise [E1, E2, E4, E5, E6]
    # C: switch point between -9.4 and -9.35 (E6: -9.4 flat, -9.35 linear)
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -9.375:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)
        except Exception:
            out.append(None)
    return {"y": out}
