def predict(probe):
    # f is zero almost everywhere except a narrow interval near 0 [E1]
    # Nonzero only for x in roughly (-1, 1): at -0.5, 0, 0.5 we see values [E1]
    # Values: f(-0.5)=-3.425, f(0)=-1.7, f(0.5)=-1.625 [E1]
    # Outside (-1,1) f=0 (at -1 and 1 it's 0) [E1]
    # Shape unknown; guess a smooth bump that's zero at |x|>=1 [E1, ?]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if x is None or x <= -1 or x >= 1:
                out.append(-0.0)
            else:
                # fit a quadratic through (-0.5,-3.425),(0,-1.7),(0.5,-1.625)
                # f(x) = a x^2 + b x + c
                # c = -1.7
                # 0.25a - 0.5b - 1.7 = -3.425 -> 0.25a - 0.5b = -1.725
                # 0.25a + 0.5b - 1.7 = -1.625 -> 0.25a + 0.5b = 0.075
                # add: 0.5a = -1.65 -> a = -3.3 ; 0.5b = 0.075+0.825=0.9 -> b=1.8
                a, b, c = -3.3, 1.8, -1.7
                out.append(a*x*x + b*x + c)
        except Exception:
            out.append(None)
    return {"y": out}
