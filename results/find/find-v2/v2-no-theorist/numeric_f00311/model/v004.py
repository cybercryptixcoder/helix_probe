def predict(probe):
    # A: for x >= -9.375: y = 8 - 9.6*x exactly [E2, E3, E4, E5, E6, E10, E11, E12, E13, E14]
    # B: for x <= -9.4: y ≈ 8 with noise [E1, E2, E4, E5, E6, E8, E11, E13]
    # C: switch point between -9.4 and -9.375 (E12: -9.4 flat, -9.375 linear; E14: -9.39 linear, -9.41 flat)
    # D: flat region value is ~8 with small noise (E12: 7.85-8.10, E14: 7.85-7.89) [E8, E12, E14]
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -9.395:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)
        except Exception:
            out.append(None)
    return {"y": out}
