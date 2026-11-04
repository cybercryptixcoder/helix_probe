import math

def predict(probe):
    # Beliefs:
    # - Positive side: y = -c_pos * x^k for x >= 1, with k ~ 6.2 [E14,E18].
    #   At x=1: y=-4.3, x=2: -60.2, x=10: -442789.0 [E18].
    # - Positive side x<1: y = 0 (exactly -0.0) [E18].
    # - Negative side: y = +c_neg * |x|^k for |x| >= 1 [E14,E16].
    #   At x=-1: y=6.1, x=-2: -67.0 ... wait, sign flips.
    # - Negative side |x|<1: y ~ 4 + 2.9*|x| [E12].
    # - Sign asymmetry: negative side magnitude larger than positive [E14].
    # - At x=0: y=0 [E2].

    # Fit from E14 clean power-law points.
    # Positive: x=3.7 -> -1057.3128 ; x=95.5 -> -370467126925.8594
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
                return -0.0
            else:
                return 3.99 + 2.89*ax
        if x > 0:
            return -c_pos * (ax**k)
        else:
            return -c_neg * (ax**k)

    return {"y": [f(x) for x in probe["x"]]}
