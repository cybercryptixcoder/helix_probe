def predict(probe):
    # For x >= -9.4 (approx): y = 8 - 9.6*x  [E2,E3,E4,E5,E6,E7,E8: exact linear]
    # For x < -9.4: y ≈ 8 (constant, small noise)  [E1,E2,E4,E5,E7]
    # E8: at x=-9.4 y=8.1987 (constant side), at x=-9.38 y=98.048 (linear side).
    # So boundary is in (-9.4, -9.38]. Guess threshold = -9.39.  [?]
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -9.39:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)
        except Exception:
            out.append(None)
    return {"y": out}
