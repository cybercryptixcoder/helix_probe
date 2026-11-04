import math

def predict(probe):
    # Beliefs:
    # - f is odd-ish: negative side is roughly -1x the positive side, but with
    #   a slightly larger magnitude coefficient on the negative side [E2,E4,E6,E8,E10,E14].
    # - Magnitude law is a power |x|^k with k ~ 6.2 for |x| >= ~1 [E6,E8,E14].
    # - For |x| < 1: positive side -> ~0; negative side -> small positive ~4-6.6 [E4,E12].
    # - At x=0: y=0 [E2].
    # - Sign: positive x -> positive y; negative x -> negative y (for |x|>=1) [all E].
    # - Small-|x| negative regime: y ~ 4 + 2.9*|x| [E12].

    # Fit exponent and coefficients from E14 (clean power-law experiment).
    # Positive: x=3.7 -> 1057.3128 ; x=95.5 -> 3.704671269258594e11
    k_pos = math.log(370467126925.8594/1057.3128)/math.log(95.5/3.7)
    # Negative: x=-3.7 -> -2487.0023 ; x=-95.5 -> -388736252049.9
    k_neg = math.log(388736252049.9/2487.0023)/math.log(95.5/3.7)
    k = (k_pos + k_neg)/2.0
    c_pos = 370467126925.8594 / (95.5**k)
    c_neg = 388736252049.9 / (95.5**k)

    def f(x):
        if x == 0:
            return 0.0
        ax = abs(x)
        if ax < 1.0:
            if x > 0:
                return 0.0
            else:
                return 3.99 + 2.89*ax
        if x > 0:
            return c_pos * (ax**k)
        else:
            return -c_neg * (ax**k)

    return {"y": [f(x) for x in probe["x"]]}
