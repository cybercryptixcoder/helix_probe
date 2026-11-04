import math

def predict(probe):
    # Beliefs:
    # 1. f is odd-ish in structure but NOT symmetric: positive and negative sides
    #    differ. [E2, E4, E6, E8]
    # 2. Positive side: for x > 2, f(x) = -exp(a + b*ln x + c*(ln x)^2) power law. [E2,E4,E5,E7]
    # 3. Positive side has a SHARP SWITCH at x = 2.0: just below 2 the magnitude is
    #    small (~-30), just above 2 it jumps to ~-60. [E10, E12]
    #    Below the switch (1 < x < 2) f is a smooth small-magnitude curve. [E10,E12]
    # 4. Negative side: for |x| > ~1.5, f(x) = -exp(a + b*ln|x| + c*(ln|x|)^2). [E2,E6,E8]
    #    For -1 <= x < 0 it is positive and rises then saturates. [E2]
    # 5. For 0 < x <= 1: f ~ 0. [E2]
    # 6. Transition on negative side is smooth (no sharp switch). [E6,E8,E10]

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
            # small-magnitude curve below the switch.
            # Fit from E10/E12: at 1.42 -> -10.05, 1.95 -> -27.56, 1.995 -> -29.84
            # roughly exponential in x. Use log-linear fit.
            # ln|f| approx: at 1.42 ln10.05=2.308, at 1.995 ln29.84=3.396
            # slope ~ (3.396-2.308)/(1.995-1.42)=1.893, intercept
            t = 2.308 + 1.893 * (ax - 1.42)
            return -math.exp(t)
        # x >= 2: power law
        t = math.log(ax)
        return -math.exp(0.484 + 5.120 * t + 0.1366 * t * t)

    # ---- Negative side ----
    if ax <= 1.0:
        return 3.9 + 2.3 * (1.0 - math.exp(-3.0 * ax))
    # smooth blend 1..1.5 then power law
    def large_neg(xx):
        t = math.log(xx)
        return -math.exp(0.383 + 5.467 * t + 0.0681 * t * t)
    if ax > 1.5:
        return large_neg(ax)
    w = (ax - 1.0) / 0.5
    small_val = 3.9 + 2.3 * (1.0 - math.exp(-3.0 * 1.0))
    return small_val * (1 - w) + large_neg(ax) * w
