import math

def predict(probe):
    # Beliefs:
    # - For x >= -9.4 (roughly), f is linear: f(x) = -9.6*x - 8.0 [E2, E14, E20]
    #   Check: x=0 -> 8.0? No: E2 x=0 -> 8.0, but formula gives -8. Let's re-derive.
    #   E14: x=0 -> 8.0, x=1 -> -1.6, x=-1 -> 17.6. Slope = -9.6, intercept 8.0.
    #   So f(x) = 8.0 - 9.6*x for x >= -9.4. [E14]
    # - For x < -9.4 (roughly), f is noisy constant ~8.0 [E2, E10, E12, E24]
    #   Boundary: E18/E22 show x=-9.4 -> ~8.0, x=-9.399 -> 98.23.
    #   E8: x=-9.4 -> 8.1987, x=-9.38 -> 98.048. Boundary between -9.4 and -9.38.
    #   E16: x=-9.395 -> 98.192, so boundary is at x=-9.4 exactly.
    #   At x=-9.4: noise ~8.0. For x>-9.4: linear.
    # - Linear region: f(x) = 8.0 - 9.6*x for x > -9.4 [E14, E20, E2]
    #   E2: x=5 -> -40 = 8-48. x=100 -> -952 = 8-960. Yes.
    # - Constant region: x <= -9.4 -> ~8.0 with noise [E10, E12, E24]
    #   Noise appears random ~N(8, 0.15) roughly. Use 8.0 as best estimate.
    # - At x = -9.4 exactly: E18 -> 8.0089, E20 -> 7.8557, E22 -> 7.8513.
    #   So x=-9.4 is in constant region (noise). Boundary: x <= -9.4 constant, x > -9.4 linear.
    #   But E8: x=-9.4 -> 8.1987 (constant), x=-9.38 -> 98.048 (linear). Consistent.
    #   E16: x=-9.395 -> 98.192 (linear). So -9.395 > -9.4, linear. Consistent.
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if x <= -9.4:
            # noisy constant around 8.0
            ys.append(8.0)
        else:
            ys.append(8.0 - 9.6 * x)
    return {"y": ys}
