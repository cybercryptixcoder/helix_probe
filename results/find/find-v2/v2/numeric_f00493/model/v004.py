import math

def predict(probe):
    # Beliefs:
    # 1. Positive side x>0: f(x) = -exp(a + b*ln x + c*(ln x)^2) power law for x>=2. [E2,E4,E5,E7,E8,E11,E12]
    # 2. Positive side has a SHARP SWITCH at x=2.0: just below 2 magnitude ~-30, at/above 2 jumps to ~-60. [E10,E12]
    #    For 1<x<2 f is a smooth small-magnitude curve (exponential in x). [E10,E12]
    #    For 0<x<=1 f ~ 0. [E2]
    # 3. Negative side x<0: for |x|>=2, f(x) = -exp(a + b*ln|x| + c*(ln x)^2). [E2,E6,E8,E14]
    #    For 1<|x|<2, f is a smooth curve crossing zero near |x|~1.4, NOT a blend. [E14]
    #    For |x|<=1, f is positive, rises then saturates. [E2,E14]
    # 4. Negative side has its own sharp switch at |x|=2.0: at -2.0 -> -67, at -2.2 -> -166. [E8,E14]

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
            # small-magnitude curve below the switch: exponential in x
            # ln|f|: at 1.42 -> ln(10.05)=2.308, at 1.995 -> ln(29.84)=3.396
            t = 2.308 + 1.893 * (ax - 1.42)
            return -math.exp(t)
        # x >= 2: power law
        t = math.log(ax)
        return -math.exp(0.484 + 5.120 * t + 0.1366 * t * t)

    # ---- Negative side ----
    if ax <= 1.0:
        # positive, rises then saturates. E14: at 1.05 -> 11.46, at 1.0 -> ~12?
        # fit: saturating. Use a + b*(1-exp(-k*ax)) style but data shows
        # 1.05->11.46, 1.1->10.53, 1.15->9.38, 1.2->8.00, 1.25->6.37, 1.3->4.46
        # decreasing with ax! So it peaks near ax=1.0 and falls.
        # Actually at ax=0.5 (E2) value? Let's use smooth curve through E14.
        # ln values: 1.05->2.439, 1.1->2.354, 1.15->2.239, 1.2->2.080, 1.25->1.852, 1.3->1.495
        # roughly linear in ax: slope ~ (1.495-2.439)/(1.3-1.05) = -3.776
        t = 2.439 - 3.776 * (ax - 1.05)
        return math.exp(t)
    if ax < 2.0:
        # smooth curve crossing zero near 1.4. E14:
        # 1.35->2.25, 1.4->-0.28, 1.45->-3.17, 1.5->-6.43, 1.55->-10.10,
        # 1.6->-14.21, 1.65->-18.79, 1.7->-23.88, 1.8->-35.69, 1.9->-49.96
        # This looks like it's heading to the power law smoothly? Check power law at 1.9:
        # large_neg(1.9) with old coeffs gave -50.4, close to -49.96. At 1.8: -37.3 vs -35.69.
        # So actually it IS the power law extended down to ~1.4! Let's use power law.
        t = math.log(ax)
        return -math.exp(0.383 + 5.467 * t + 0.0681 * t * t)
    # ax >= 2: power law (same formula, continuous at 2)
    t = math.log(ax)
    return -math.exp(0.383 + 5.467 * t + 0.0681 * t * t)
