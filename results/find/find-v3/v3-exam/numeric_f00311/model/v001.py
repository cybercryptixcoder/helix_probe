def predict(probe):
    # Model of f(x):
    # For x >= -10 (roughly): f(x) = 8 - 9.6*x  [E2: at x=0 ->8, x=1->-1.6, x=20->-184]
    # For x < -10: f(x) = -8*x  [E2: x=-12->7.9806? no...]
    # Re-examine E2: 
    #   x=-12 -> 7.9806, x=-10 -> 7.8354  (small positive, ~8)
    #   x=-8 -> 84.8, x=-6 -> 65.6, x=-4 -> 46.4, x=-3 -> 36.8, x=-2 -> 27.2,
    #   x=-1 -> 17.6, x=-0.5 -> 12.8, x=0 -> 8.0, x=0.5 -> 3.2, x=1 -> -1.6,
    #   x=2 -> -11.2, x=3 -> -20.8, x=4 -> -30.4, x=6 -> -49.6, x=8 -> -68.8,
    #   x=10 -> -88.0, x=12 -> -107.2, x=20 -> -184.0
    # For x in [-8, 20]: f(x) = 8 - 9.6*x  (check: -8 -> 8+76.8=84.8 ✓, 20 -> 8-192=-184 ✓)
    # For x in [-12,-10]: ~7.9-8.0, roughly constant ~8 (maybe 8 - 0.0? or a different branch)
    # E1: x=88.2 -> -838.72 = 8 - 9.6*88.2 = 8 - 846.72 = -838.72 ✓
    #     x=66 -> 8-633.6=-625.6 ✓
    #     x=-20.3 -> 8.0426 (small positive ~8)
    #     x=-61.7 -> 8.0358 (~8)
    #     x=2.9 -> -19.84 = 8-27.84 ✓
    #     x=-24.3 -> 7.9875 (~8)
    #     x=72.7 -> -689.92 = 8-697.92 ✓
    #     x=-50.4 -> 8.1082 (~8)
    #     x=-6.0 -> 65.6 = 8+57.6 ✓
    #     x=21.3 -> -196.48 = 8-204.48 ✓
    # So for x < -10: f(x) ≈ 8 (slightly noisy, ~7.98-8.11)
    # For x >= -10: f(x) = 8 - 9.6*x
    # Boundary: at x=-10, E2 gives 7.8354 (small branch). At x=-8, 84.8 (linear branch).
    # So boundary between -10 and -8. Test says "near x=0" but data shows boundary near -9?
    # Actually maybe boundary at x=-9 or so. Let's guess x < -9 -> ~8, x >= -9 -> 8-9.6x.
    # Check x=-10: 7.8354 (small). x=-8: 84.8 (linear). Boundary in (-10,-8].
    # Guess boundary at -9: for x < -9, f≈8; for x >= -9, f=8-9.6x.
    # At x=-9: 8-9.6*(-9)=94.4. Unknown.
    # The small branch values: 7.9806, 7.8354, 8.0426, 8.0358, 7.9875, 8.1082 — noisy around 8.
    # Maybe f(x) = 8 + small noise for x < -9.
    # Use 8 as the prediction (noise is unpredictable).
    out = []
    for x in probe["x"]:
        if x < -9:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}
