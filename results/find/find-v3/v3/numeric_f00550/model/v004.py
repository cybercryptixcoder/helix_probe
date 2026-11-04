def predict(probe):
    # f(x) = -1.7 + 1.8x - 3.3x^2 on the nonzero region [E2,E4]
    # Nonzero region: |x| in [0.76, 0.8] on both sides? Let's check E6.
    # E6: -0.8 -> -5.252 (nonzero), -0.79 -> -5.1815 (nonzero), -0.82 -> 0, -0.81 -> 0
    #     so negative boundary: nonzero for |x| <= 0.8, zero for |x| >= 0.81
    # E6: 0.8 -> -2.372 (nonzero), 0.79 -> -2.3375 (nonzero), 0.82 -> 0, 0.81 -> 0
    #     so positive boundary: nonzero for x <= 0.8, zero for x >= 0.81
    # So nonzero region is |x| <= 0.8 (inclusive at 0.8), zero for |x| >= 0.81.
    # Check formula at 0.8: -1.7 + 1.44 - 2.112 = -2.372 ✓
    # Check at -0.8: -1.7 - 1.44 - 2.112 = -5.252 ✓
    # E4: -0.99, 0.99, -0.9, 0.9 all zero ✓ (|x| > 0.8)
    # E4: -0.75, 0.75 nonzero ✓
    ys = []
    for x in probe["x"]:
        if x is None:
            ys.append(None)
        elif abs(x) <= 0.8:
            ys.append(-1.7 + 1.8 * x - 3.3 * x * x)
        else:
            ys.append(-0.0)
    return {"y": ys}
