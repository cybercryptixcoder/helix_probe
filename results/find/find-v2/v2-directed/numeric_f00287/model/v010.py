import math

def predict(probe):
    # Left region: y = -0.7*floor(x) for x <= -5.1 [E1,E2,E4,E7,E9,E10,E13,E16]
    #   E16: -5.1 -> 4.2 (const, floor=-6 -> 4.2). So x <= -5.1 is linear.
    #   E10: -5.101 -> 4.2 (const), -5.099 -> -402.38 (const). Boundary in (-5.101,-5.099].
    # Middle constant: y ~ -402.3 (noisy) for -5.1 < x < 18.518 [E1..E8,E10,E12,E14,E15]
    #   E8: 18.515 -> -402.39 (const), 18.518 -> -302.4 (linear)
    # Right region: y = -16.8*floor(x) for x >= 18.518 [E1,E3,E4,E5,E6,E8,E11,E13,E14]
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -5.1:
                out.append(-0.7 * math.floor(x))
            elif x < 18.518:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}
