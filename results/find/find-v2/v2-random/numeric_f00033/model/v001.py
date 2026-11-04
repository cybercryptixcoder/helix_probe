import math

def predict(probe):
    # Beliefs:
    # - Outputs are tiny except near x≈0, where there's a bump [E1: x=2.9 -> 0.0362, others ~1e-3 or less]
    # - Magnitudes decay with |x|: |x|~6 -> 0.0, |x|~20 -> 1e-3, |x|~50-60 -> 3e-3, |x|~66-88 -> 2-3e-4 [E1]
    # - Looks like a narrow Gaussian-like peak near 0 plus a small broad component [E1]
    # - Sign: outputs are negative except near 0 (x=2.9 positive, x=-6.0 = 0.0) [E1]
    # - Model: y = A*exp(-x^2/(2*s1^2)) - B*exp(-x^2/(2*s2^2)) roughly [E1, ?]
    out = []
    for x in probe["x"]:
        try:
            # narrow positive peak near 0
            peak = 0.036 * math.exp(-(x*x)/(2*3.0*3.0))
            # broad negative component
            broad = 0.0032 * math.exp(-(x*x)/(2*45.0*45.0))
            y = peak - broad
            out.append(round(y, 4))
        except Exception:
            out.append(None)
    return {"y": out}
