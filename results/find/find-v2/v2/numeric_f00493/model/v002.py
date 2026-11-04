import math

def predict(probe):
    # Beliefs:
    # 1. f(x) = -sign(x) * exp(a + b*ln|x| + c*(ln|x|)^2) for |x| > ~1.5, with
    #    separate coefficients for positive and negative x. [E1, E2, E3]
    # 2. Positive-x coefficients: a=0.484, b=5.120, c=0.1366. [E2]
    # 3. Negative-x coefficients: a=0.383, b=5.467, c=0.0681. [E2]
    # 4. For 0 < x <= 1: f(x) ~ 0 (tiny). [E2]
    # 5. For -1 <= x < 0: f(x) rises from ~3.95 (at -0.01) to ~6.24 (at -0.5),
    #    then ~6.1 at -1. Saturating curve. [E2]
    # 6. Transition region 1 < |x| <= 1.5: blend small-region to large-region. [E2]
    # 7. E3 shows the large-|x| formula is close but slightly off; refine fit
    #    using E3 points to improve accuracy. [E3]

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

    def large_pos(xx):
        t = math.log(xx)
        return -math.exp(0.484 + 5.120*t + 0.1366*t*t)

    def large_neg(xx):
        t = math.log(xx)
        return -math.exp(0.383 + 5.467*t + 0.0681*t*t)

    if ax <= 1.0:
        if x > 0:
            return 0.0
        else:
            return 3.9 + 2.3 * (1.0 - math.exp(-3.0 * ax))

    if ax > 1.5:
        return large_pos(ax) if x > 0 else large_neg(ax)

    # Blend 1 < |x| <= 1.5
    w = (ax - 1.0) / 0.5
    if x > 0:
        small_val = 0.0
        large_val = large_pos(ax)
    else:
        small_val = 3.9 + 2.3 * (1.0 - math.exp(-3.0 * 1.0))
        large_val = large_neg(ax)
    return small_val * (1-w) + large_val * w
