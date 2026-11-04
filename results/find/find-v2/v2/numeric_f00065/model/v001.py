def predict(probe):
    # Observations suggest f is roughly piecewise-linear with a kink near 0.
    # E1 data: for x>0, y is negative and roughly -2.6*x (88.2->-228.97, 66->-173.49, 72.7->-190.23, 21.3->-61.81, 2.9->-15.84)
    #   ratios: -2.596, -2.628, -2.617, -2.902, -5.46 (small x deviates)
    # For x<0, y is positive and roughly -1.6*x (i.e. positive): -20.3->26.97 (-1.33), -61.7->99.56 (-1.61), -24.3->33.98 (-1.40), -50.4->79.75 (-1.58), -6->1.91 (-0.32)
    # Looks like an odd-ish function: y ≈ -a*x with a≈2.6 for x>0, a≈1.6 for x<0. Not odd.
    # Small |x| values deviate (2.9->-15.84, -6->1.91) suggesting a smooth MLP curve, not pure linear.
    # Best guess: piecewise linear with different slopes on each side, plus mild curvature near 0.
    # ?: slopes and intercepts estimated from E1 only.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x >= 0:
                # positive side: y ≈ -2.62*x, with a small offset near 0
                y = -2.62 * x
            else:
                # negative side: y ≈ -1.55*x
                y = -1.55 * x
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
