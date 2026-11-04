import math

def predict(probe):
    # A: for |x| >= ~2.5, y ≈ -3.9 * x^3 [E1, E2, E3, E7, E9]
    # B: for |x| < ~2.5, cubic is replaced by a small noisy offset around +3 [E4, E6, E8, E10]
    #    x=0 -> 4.50, x=0.05 -> 2.91, x=0.1 -> 2.31, x=0.2 -> 4.43, x=0.3 -> 3.52, x=0.4 -> 5.37
    #    x=-0.5 -> 2.04, x=-0.4 -> 3.08, x=-0.3 -> 1.02, x=-0.2 -> 1.45, x=-0.1 -> 3.58
    #    mean ~3.2, noisy; NOT a smooth Gaussian bump (v2 was wrong) [E10]
    # C: transition: at |x|=1.0 obs ~1.6-1.9 (below cubic 3.9); at |x|=1.2 obs ~-0.5 to -0.8
    #    so cubic takes over around |x|~1.0-1.2, not 2.5 [E10, E8]
    #    E8: x=1.05 -> 0.26, x=1.25 -> -1.61; x=-1.15 -> 5.16, x=-0.95 -> 4.72 (noisy)
    # D: region |x|<~1.1: y ≈ small offset ~3 (noisy), roughly flat; use 3.2 [E10]
    # E: outside: y = -3.9*x^3 [E1,E7,E9]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if abs(x) < 1.1:
                y = 3.2
            else:
                y = -3.9 * x**3
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
