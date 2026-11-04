import math

def predict(probe):
    # Observations:
    # - Outputs are noisy, roughly in [-0.4, 0.4], no smooth structure at any scale [E8,E10,E12,E14,E16,E18,E20,E22]
    # - No period-1 / integer lattice structure [E22]
    # - For x < ~-75: y ≈ -0.6/x (tiny positive tail) [E1,E3,E4,E5,E13,E15,E19,E21]
    # - Elsewhere: pseudo-random-looking values, mean ~0, std ~0.1 [all]
    # Best guess: deterministic pseudo-random function of x, plus tail rule.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x < -75:
                ys.append(-0.6 / x)
            else:
                # Hash-like pseudo-random, roughly N(0, 0.1) via sum of sines
                h = (math.sin(x * 12.9898 + 78.233)
                     + math.sin(x * 4.1414 + 1.234)
                     + math.sin(x * 0.7071 + 3.14159))
                ys.append(h * 0.06)
        except Exception:
            ys.append(None)
    return {"y": ys}
