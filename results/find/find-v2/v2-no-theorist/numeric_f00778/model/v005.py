import math

def predict(probe):
    # A: for |x| >= ~1.15, y ≈ -3.9 * x^3 (cubic dominates) [E1,E2,E3,E7,E9,E11,E13,E21,E23]
    #    E24: at |x|=1.15 obs ~5.4 (neg) / -1.27 (pos) — still offset-ish, cubic small
    #    E24: at |x|=1.2 obs 6.5 / -2.1; |x|=1.3 obs 9.3 / -3.4; |x|=1.6 obs 15.3 / -9.8
    #    Negative side is consistently ~+offset above pure cubic; positive side ~cubic.
    # B: for |x| < ~1.0, y ≈ noisy plateau around ~3.3, unstructured [E4,E6,E8,E10,E12,E14,E16,E18,E20]
    #    E20 near zero: mean ~3.0, still noisy, no repeatable dip/bump.
    # C: transition region ~1.0-1.15: values blend between plateau and cubic [E10,E14,E22,E24]
    #    E22: |x|=1.0 obs ~6.5(neg)/0.07(pos); |x|=1.1 obs ~7.2(neg)/1.2(pos)
    #    Negative side keeps a positive offset through ~1.3; positive side drops faster.
    # D: noise amplitude ~±1.5 on plateau; cubic region essentially exact [E21,E23]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            ax = abs(x)
            if ax < 1.0:
                y = 3.3
            elif ax < 1.15:
                # blend: plateau offset fading into cubic
                t = (ax - 1.0) / 0.15
                y = (1 - t) * 3.3 + t * (-3.9 * x**3)
            else:
                y = -3.9 * x**3
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
