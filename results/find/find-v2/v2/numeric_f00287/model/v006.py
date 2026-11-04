import math

def predict(probe):
    # Left region: y = -0.7*floor(x) for x < -5.05  [E8: -5.1->4.2, -5.05->const; E16: -5.1->4.2, -5.05->-402.3]
    # Middle region: y ≈ -402.3 (noisy constant) for -5.05 <= x < 18.54  [E6,E12,E16: 18.5 const, 18.54 const]
    # Right region: y = -16.8*floor(x) for x >= 18.54  [E14: 18.5 const, 18.55->-302.4; E16: 18.54 const, 18.55->-302.4]
    # Right breakpoint is between 18.54 and 18.55 [E14, E16]
    # Left breakpoint is between -5.1 and -5.05 [E8, E16]
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5.05:
                out.append(-0.7 * math.floor(x))
            elif x < 18.54:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}
