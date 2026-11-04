import math

def predict(probe):
    # Left region: y = -0.7*floor(x) for x < -5.0  [E8: -5.1->4.2, -5.0->const; E9,E10,E11]
    # Middle region: y ≈ -402.3 (noisy constant) for -5.0 <= x < 18.55  [E6,E12,E14: 18.5 const, 18.55 linear]
    # Right region: y = -16.8*floor(x) for x >= 18.55  [E14: 18.55->-302.4, 18.9->-302.4, 19->-319.2]
    # Right breakpoint is between 18.5 and 18.55 [E14]
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5.0:
                out.append(-0.7 * math.floor(x))
            elif x < 18.55:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}
