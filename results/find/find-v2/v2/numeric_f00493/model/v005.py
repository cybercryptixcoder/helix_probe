import math

def predict(probe):
    # Beliefs:
    # 1. For |x| large (>=2), f(x) = -exp(a + b*ln|x| + c*(ln|x|)^2), separate coeffs per side. [E4,E7,E11,E13,E15,E16,E17]
    # 2. Positive side: sharp jump at x=2.0 from ~-30 (just below) to ~-60 (at/above). [E12,E18]
    #    For 1<x<2: smooth small-magnitude curve, exponential in x. [E10,E12,E18]
    #    For 0<x<=1: f~0. [E2]
    # 3. Negative side: sharp jump at |x|=2.0 from ~-67 (just below) to ~-101 (just above). [E18]
    #    For 1<|x|<2: smooth curve crossing zero near |x|~1.4. [E14,E18]
    #    For |x|<=1: positive, decreasing with |x|, peaks near |x|=1. [E14]

    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            out.append(_f(float(v)))
        except Exception:
            out.append(None)
    return {"y": out}


def _f(x):
    if x == 0.0:
        return -0.0
    ax = abs(x)

    # ---- Positive side ----
    if x > 0:
        if ax <= 1.0:
            return 0.0
        if ax < 2.0:
            # exponential in x through E18/E10/E12: ln|f| at 1.9->3.227, 1.999->3.403
            t = 3.227 + 1.86 * (ax - 1.9)
            return -math.exp(t)
        # x >= 2: power law
        t = math.log(ax)
        return -math.exp(0.484 + 5.120 * t + 0.1366 * t * t)

    # ---- Negative side ----
    if ax <= 1.0:
        # decreasing with ax, peaks near ax=1. E14: 1.05->11.46, 1.3->4.46
        t = 2.439 - 3.776 * (ax - 1.05)
        return math.exp(t)
    if ax < 2.0:
        # smooth curve crossing zero near 1.4, heading to jump value ~-67 at 2.
        # E14/E18: 1.4->-0.28, 1.5->-6.43, 1.7->-23.88, 1.9->-49.96, 1.999->-66.81
        # fit ln|f| vs ln(ax): use power law with own coeffs
        t = math.log(ax)
        return -math.exp(0.383 + 5.467 * t + 0.0681 * t * t)
    # ax >= 2: power law (jump at 2: at 2.0 -> -67, at 2.001 -> -100.78)
    t = math.log(ax)
    return -math.exp(0.383 + 5.467 * t + 0.0681 * t * t)
