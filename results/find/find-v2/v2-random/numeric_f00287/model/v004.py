import math

def predict(probe):
    # A: for x < 0, y = -0.705*x (linear, slope ~ -0.705) [E1,E2,E3,E4,E5]
    # B: for 0 < x < ~15, y = -402.45 (constant plateau) [E1:2.9, E2:1.2, E4:12.5, E5:17.3?]
    #    E5: 17.3 -> -402.3285, so plateau extends to at least 17.3
    #    E1: 21.3 -> -352.8 (linear), so boundary between 17.3 and 21.3
    # C: for x > boundary, y = -16.72*x (linear, slope ~ -16.72) [E1-E5]
    #    Boundary: solve -16.72*x = -402.45 => x ~ 24.07, but 21.3 is linear.
    #    So plateau is a dip below the line; boundary ~ 20 (between 17.3 and 21.3).
    #    Actually check: at boundary, plateau -402.45 vs line -16.72*x.
    #    At x=20: line=-334.4, plateau=-402.45. At x=24: line=-401.28.
    #    Plateau value -402.45 matches line at x=24.07. But 21.3 is linear (-352.8).
    #    So plateau ends somewhere 17.3 < b < 21.3, then jumps to line. Pick b=20? 
    #    Hmm, but then discontinuity. Maybe plateau is exactly where |line| < 402.45? No.
    #    Best guess: plateau for 0<x<20, linear for x>=20. Boundary uncertain (?) 
    #    Actually E5: 17.3 plateau, E1: 21.3 linear. Try b=20.
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                y = -0.705 * x
            elif x < 20:
                y = -402.45
            else:
                y = -16.72 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
