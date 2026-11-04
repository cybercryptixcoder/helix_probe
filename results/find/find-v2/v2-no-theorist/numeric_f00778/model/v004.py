import math

def predict(probe):
    # A: for |x| >= ~1.0, y ≈ -3.9 * x^3 [E1,E2,E3,E7,E9,E11,E13]
    # B: for |x| < ~1.0, y ≈ noisy offset around ~3.3, unstructured [E4,E6,E8,E10,E12,E14]
    #    Observed small-|x| values scatter ~1.8..5.5 with mean ~3.3, no repeatable shape [E12,E14]
    # C: transition near |x|~1.0: at |x|=1.0 obs ~1.6-5.2 (noisy, near offset); at |x|=1.1-1.2
    #    obs drops toward cubic (E14: -1.1->6.9, -1.2->7.4; E10: 1.1->-0.67, 1.2->-0.50) [E10,E14]
    #    So boundary ~1.0-1.1; use 1.05.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if abs(x) < 1.05:
                y = 3.3
            else:
                y = -3.9 * x**3
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
