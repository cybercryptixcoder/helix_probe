import math

def predict(probe):
    # Left linear: y = -0.7*floor(x) for x < -5 [E1,E2,E4,E7]
    #   E7: -128..-5.1 all match -0.7*floor(x); -5.05 -> constant
    #   So boundary between -5.1 and -5.05: x < -5.05 linear? E7 -5.05 -> -402.19 (const)
    #   E7 -5.1 -> 4.2 (floor=-6 -> 4.2). -5.05 -> const. Boundary in (-5.1, -5.05].
    #   E1 -5 -> const. So left linear for x < -5.05 (approx; use -5.05).
    # Middle constant: y ~ -402.3 (noisy) for -5.05 <= x < 18.52 [E1,E2,E3,E5,E6,E7]
    #   E6: 18.515 const, 18.52 linear. E5: 18.51 const, 18.55 linear.
    #   Boundary at x = 18.52.
    # Right linear: y = -16.8*floor(x) for x >= 18.52 [E1,E3,E4,E5,E6]
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5.05:
                out.append(-0.7 * math.floor(x))
            elif x < 18.52:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}
