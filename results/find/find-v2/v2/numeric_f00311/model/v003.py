def predict(probe):
    # For x >= -9.3 (approx): y = 8 - 9.6*x  [E2,E3,E4,E5,E6: exact linear]
    # For x < boundary: y ≈ 8 (constant, small noise)  [E1,E2,E4,E5]
    # E6 shows linear holds at -9.3 (97.28 = 8-9.6*(-9.3)); constant at -9.5 (7.97).
    # So boundary is in (-9.5, -9.3]. Guess threshold = -9.4.  [?]
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -9.4:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)
        except Exception:
            out.append(None)
    return {"y": out}
