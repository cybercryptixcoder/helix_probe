import math

def predict(probe):
    # Model: f(x) = sign-dependent coefficient * |x|^k, with a small-|x| regime.
    # Evidence:
    #  - Large |x|: log-log slope ~ k. From E14: x=95.5 -> 3.70e11, x=75.5 -> 8.99e10
    #    ratio ~4.12 over factor 1.265 -> k ~ ln(4.12)/ln(1.265) ~ 6.2. Check E6:
    #    x=90 -> 2.606e11, x=70 -> 5.739e10, ratio 4.54 over 1.286 -> k~6.2.
    #    So k ~ 6.2 (let's fit more precisely below).
    #  - Positive vs negative coefficients differ (sign asymmetry) [E2,E4,E6,E8,E10,E14].
    #  - Near zero (|x| < ~1): positive side -> ~0; negative side -> small positive
    #    constant ~4-6.6 [E4, E12]. So there's a regime change for |x| < 1.
    #  - At x=0: y=0 [E2].
    #
    # Fit k from E14 positive side:
    #   x=3.7 -> 1057.3128 ; x=95.5 -> 3.704671269258594e11
    #   k = ln(3.7047e11/1057.31)/ln(95.5/3.7)
    k_pos = math.log(370467126925.8594/1057.3128)/math.log(95.5/3.7)
    # negative side:
    k_neg = math.log(388736252049.9/2487.0023)/math.log(95.5/3.7)
    # Use average exponent
    k = (k_pos + k_neg)/2.0
    # Coefficients: c = y / |x|^k
    c_pos = 1057.3128 / (3.7**k)
    c_neg = 2487.0023 / (3.7**k)
    # Verify with another point (E14 x=95.5)
    # c_pos check: 370467126925.8594 / 95.5**k
    c_pos = 370467126925.8594 / (95.5**k)
    c_neg = 388736252049.9 / (95.5**k)

    def f(x):
        if x == 0:
            return 0.0
        ax = abs(x)
        if ax < 1.0:
            # Small-|x| regime: positive side ~ 0, negative side ~ small positive
            if x > 0:
                return 0.0
            else:
                # E12: x=-0.05 -> 4.1301, x=-0.9 -> 6.5864, x=-0.15 -> 4.6135
                # Roughly constant ~4-6.6, increasing with |x|. Fit linear-ish.
                # At -0.05:4.13, -0.9:6.59. slope ~ (6.59-4.13)/0.85 ~ 2.89
                # intercept at 0: 4.13 - 2.89*0.05 ~ 3.99
                return 3.99 + 2.89*ax
        if x > 0:
            return c_pos * (ax**k)
        else:
            return -c_neg * (ax**k)

    return {"y": [f(x) for x in probe["x"]]}
