def predict(probe):
    # For x >= -6: y = 8 - 9.6*x  [E1,E2,E3,E4: exact across all tested values]
    # For x < -6: y = 8 (constant, small noise)  [E1,E2,E4: -9.5->7.97, -10..-120 all ~8]
    # Boundary is between -9.5 (constant) and -9 (linear: 94.4=8-9.6*(-9))  [E4]
    #   -9.5 -> 7.9742 (constant), -9 -> 94.4 (linear). So threshold in (-9.5, -9].
    #   Guess threshold = -9: x >= -9 linear, x < -9 constant.  [?]
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -9:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)
        except Exception:
            out.append(None)
    return {"y": out}
