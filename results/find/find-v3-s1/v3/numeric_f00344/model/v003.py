import math

def predict(probe):
    # Model v3
    # Observations / beliefs:
    # - There is a hard floor clamp at FLOOR = -24973124.7 for large |x| [E1,E2,E3,E7,E9,E15,E17,E19]
    # - f(0) = 472.73, a spike at exactly zero [E2,E4]
    # - Positive side, small x (0<x<~1.5): f(x) ≈ c + a*x^3 with c≈-36.8, a≈-5 [E18,E12]
    #   e.g. f(0.05)=-36.88, f(1.0)=-41.7, f(1.3)=-47.38 [E18]
    # - Positive side, larger x: grows like a power law. f(2)=-79.6, f(3)=-211.7,
    #   f(4)=-528, f(5)=-1147.3, f(10)=-14962.8, f(15)=-70733.3, f(20)=-215708.8 [E8,E12,E10]
    #   Ratios suggest ~x^3.5-ish; check: 10->15 factor 4.73 (1.5^3.9), 15->20 factor 3.05 (1.33^3.9)
    #   Actually f(10)=14962.8, f(20)=215708.8: ratio 14.4 = 2^3.85. So exponent ~3.85.
    # - Negative side, small |x| (0<|x|<~2): f is a smooth negative curve with a minimum
    #   near x=-2 (f(-2)=-0.1, f(-2.2)=+0.0093), rising toward -11.6 as x->0- [E16,E18,E14]
    #   f(-0.05)=-11.62, f(-1)=-7.4, f(-1.5)=-3.225, f(-2)=-0.1, f(-2.2)=0.0093,
    #   f(-2.5)=-2.075, f(-3)=-15, f(-4)=-106.1, f(-5)=-356.2, f(-7)=-1808.6, f(-10)=-8905.7 [E14,E16]
    # - Negative side, large |x|: power law, f(-15)=-50410.2, f(-20)=-167619.7,
    #   f(-30)=-890153.7, f(-40)=-2878507.7, f(-50)=-7122681.7, f(-60)=-14900675.7 [E10]
    #   ratio f(-60)/f(-30)=16.7 = 2^4.06; f(-40)/f(-20)=17.2=2^4.1. Exponent ~4.05.
    # - Positive large: f(60)=-16196892.8, f(30)=-1052274.8 ratio 15.4=2^3.95. Exponent ~3.95.
    # - Floor clamp kicks in around |x|>=~100 [E2,E9,E15,E17,E19]

    FLOOR = -24973124.7
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        try:
            if x == 0:
                out.append(472.73)
                continue
            if x > 0:
                if x < 1.5:
                    # c + a*x^3, c≈-36.8, a≈-5.0 [E18]
                    v = -36.8 - 5.0 * (x ** 3)
                else:
                    # power law ~ -A*x^p. Fit from f(10)=-14962.8, f(20)=-215708.8
                    # A = 14962.8 / 10^p ; ratio 215708.8/14962.8 = 14.416 = 2^p -> p=3.849
                    p = 3.849
                    A = 14962.8 / (10.0 ** p)
                    v = -A * (x ** p)
            else:
                ax = -x
                if ax < 2.0:
                    # smooth curve: f(-0.05)=-11.62 ... f(-2)=-0.1
                    # Try quadratic-ish: f(x) = a + b*x + c*x^2 near 0 negative side
                    # Use points (-0.05,-11.6174),(-1,-7.4),(-2,-0.1)
                    # Fit quadratic through these
                    # Solve: a + b*(-0.05) + c*0.0025 = -11.6174
                    #        a + b*(-1) + c*1 = -7.4
                    #        a + b*(-2) + c*4 = -0.1
                    # From eq2-eq1: -0.95b + 0.9975c = 4.2174
                    # eq3-eq2: -b + 3c = 7.3 -> b = 3c - 7.3
                    # -0.95(3c-7.3)+0.9975c = 4.2174 -> -2.85c+6.935+0.9975c=4.2174
                    # -1.8525c = -2.7176 -> c=1.4670 ; b=3*1.4670-7.3=-2.899
                    # a = -7.4 + b*1 - c*1 = -7.4 -2.899 -1.467 = -11.766
                    v = -11.766 - 2.899 * x + 1.4670 * (x * x)
                else:
                    # power law on negative side: f(-30)=-890153.7, f(-60)=-14900675.7
                    # ratio 16.74 = 2^p -> p=4.065
                    p = 4.065
                    A = 890153.7 / (30.0 ** p)
                    v = -A * (ax ** p)
            if v < FLOOR:
                v = FLOOR
            out.append(v)
        except Exception:
            out.append(None)
    return {"y": out}
