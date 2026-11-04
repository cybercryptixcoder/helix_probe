def predict(probe):
    # A: for x >= -9: y = 8 - 9.6*x exactly [E2, E3, E4]
    #    (E4: -9 -> 94.4 = 8+86.4 ✓; -8.5 -> 89.6 ✓; ... -0.5 -> 12.8 ✓)
    # B: for x <= -9.5: y ≈ 8 with noise [E1, E2, E4]
    #    (E4: -9.5 -> 8.0184 flat; E2: -10..-70 all ~8)
    # C: boundary is between -9.5 and -9 (E4: -9.5 flat, -9 linear)
    #    Exact threshold unknown; choose x >= -9.25 (?) — no data in (-9.5,-9)
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -9.25:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)
        except Exception:
            out.append(None)
    return {"y": out}
