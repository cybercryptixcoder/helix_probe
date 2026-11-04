def predict(probe):
    # For x >= -9.4: y = 8 - 9.6*x  (exact linear) [E2,E3,E4,E5,E6,E7,E8,E14,E16]
    # For x < -9.4: y ≈ 8 (constant, small noise) [E1,E2,E4,E5,E7,E10,E12,E13,E15]
    # Boundary: E16 shows x=-9.395 -> 98.192 (linear), x=-9.39 -> 98.144 (linear).
    #   E8: x=-9.4 -> 8.1987 (constant), x=-9.38 -> 98.048 (linear).
    #   So threshold is in (-9.4, -9.395]. Guess -9.4 exactly: x < -9.4 constant, x >= -9.4 linear. [?]
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
