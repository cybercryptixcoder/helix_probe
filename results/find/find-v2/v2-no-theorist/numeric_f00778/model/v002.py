import math

def predict(probe):
    # A: for |x| >= ~2.5, y ≈ -3.9 * x^3 [E1, E2, E3]
    #    coefficient ~ -3.90 (E1: -2677280/88.2^3 = -3.90; E3 matches -3.9 well)
    # B: for |x| < ~2.5, there is a positive offset bump (~+3 to +5) added to the cubic [E2, E4]
    #    x=0 -> 4.77, x=0.6 -> 5.23, x=0.4 -> 5.23, x=-0.8 -> 5.54, x=-0.6 -> 1.33
    #    The bump is noisy/irregular; approximate as a plateau ~+4.5 near 0 fading out by |x|~2.5
    # C: transition: at |x|=2.0 obs 30.0 vs cubic 31.2 (close); at |x|=2.5 obs 58.1 vs 60.9
    #    so cubic dominates by |x|~2, bump only matters for |x| < ~1.5 [E4]
    # D: small region is noisy; use a smooth Gaussian bump ~4.5*exp(-x^2/1.5) added to cubic [E4 ?]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            y = -3.9 * x**3 + 4.5 * math.exp(-x*x/1.5)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
