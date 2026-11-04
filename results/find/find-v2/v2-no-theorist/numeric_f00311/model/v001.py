def predict(probe):
    # Piecewise linear function with a noisy "flat" region near zero.
    # For |x| >= ~30: y ≈ 8 - 9.6*x  (slope -9.6, intercept 8) [E2]
    #   e.g. x=60 -> 8-576=-568 ✓; x=-70 -> 8+672=680? no, observed 7.87
    # Wait: negative side is flat ~8, positive side is linear [E2]
    # E2: x<=-10 -> y≈8 (noisy); x>=0 -> y = 8 - 9.6*x exactly
    #   x=0->8, 5->-40, 10->-88, ..., 60->-568 ✓ (slope -9.6)
    #   x=-5 -> 56 (anomaly), x=-10..-70 -> ~8
    # E1 check: 88.2 -> 8-9.6*88.2 = -838.72 ✓
    #   66.0 -> 8-633.6 = -625.6 ✓
    #   72.7 -> 8-697.92 = -689.92 ✓
    #   21.3 -> 8-204.48 = -196.48 ✓
    #   2.9 -> 8-27.84 = -19.84 ✓
    #   -20.3 -> 8.0127 (flat ~8) ✓
    #   -61.7 -> 7.8607 ✓
    #   -24.3 -> 8.1499 ✓
    #   -50.4 -> 8.0456 ✓
    #   -6.0 -> 65.6  (anomaly, near -5)
    # So: for x >= 0: y = 8 - 9.6*x
    #     for x <= -10: y ≈ 8 (noisy)
    #     for -10 < x < 0: transition, with spikes at -5 and -6
    # Hypothesis: the flat region is x < 0, but there's a special bump near -5..-6.
    # Actually -5 -> 56, -6 -> 65.6. Both positive spikes. Maybe y = 8 - 9.6*x
    #   at x=-5 gives 56! 8+48=56 ✓. At x=-6: 8+57.6=65.6 ✓!
    # So the linear formula y=8-9.6*x holds at -5 and -6 too.
    # But -10 -> 7.8751, not 8+96=104. So boundary is between -6 and -10.
    # Likely: for x >= -6 (or x > -something): linear; else flat ~8.
    # Test: -10 flat, -6 linear. Boundary in (-10,-6]. Guess -8? or -7?
    # E1: -6.0 -> 65.6 linear ✓. No data between -10 and -6.
    # Guess threshold: x >= -7? Unknown. Pick x >= -7 (?) 
    # Flat region value ~8 with noise.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -7:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)  # noisy flat ~8
        except Exception:
            out.append(None)
    return {"y": out}
