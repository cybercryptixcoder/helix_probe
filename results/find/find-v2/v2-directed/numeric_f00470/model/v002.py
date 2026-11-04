import math

def predict(probe):
    # Model of f(x):
    # Negative side (x < 0): f(x) = a*x^3 + b*x + c  [E11, E3, E6]
    #   Fit from E11 clean points. From E11:
    #   f(-20) = -112324723.7, f(-10) = -3613822.11, f(-5) = -120306.515
    #   Solve a,b,c exactly.
    # Positive side (x > 0): f(x) = A*(x+B)*exp(C*x) + D  [E10, E12, E4, E5]
    #   Fit from E12/E10 clean points.
    # Near x=0 (|x| small): there is a separate smooth "bump" region [E8, E13]
    #   Values near 0 hover around 20-28 then dip negative around 0.5-0.6,
    #   then rise. This is NOT the cubic (cubic at x=-0.5 is ~26.7, matches!)
    #   Actually check: cubic at x=-0.5: a*(-0.125)+b*(-0.5)+c.
    #   Let's compute a,b,c from E11 and see if it matches near-zero negatives.
    #   And positive side near 0: E13 shows f(0.02)=20.34, f(0.5)=-22.96,
    #   f(1)=70.35. The exponential form A(x+B)e^{Cx}+D with B negative
    #   gives a zero-crossing and dip. Let's fit it properly.

    # --- Negative cubic from E11 ---
    # x=-20: -8000a -20b + c = -112324723.7
    # x=-10: -1000a -10b + c = -3613822.11
    # x=-5:   -125a  -5b + c = -120306.515
    # (1)-(2): -7000a -10b = -108710901.59 => 700a + b = 10871090.159
    # (2)-(3): -875a -5b = -3493515.595 => 175a + b = 698703.119
    # subtract: 525a = 10172387.04 => a = 19375.975314...
    a = (10871090.159 - 698703.119) / 525.0
    b = 698703.119 - 175.0 * a
    c = -3613822.11 + 1000.0 * a + 10.0 * b

    # --- Positive exponential fit A*(x+B)*exp(C*x)+D ---
    # Use E12 clean points (large x where D negligible) to get B, C.
    # Then use E10/E12 to get A, D.
    # Let's fit numerically via grid search on B, C with linear A,D.
    pos_data = [
        (0.5,-22.9553),(0.75,-13.0279),(1.0,70.35),(1.25,317.5232),
        (1.5,867.6703),(1.75,1927.1454),(2.0,3782.82),(2.5,11499.8909),
        (3.0,28401.19),(3.5,60999.1766),(4.0,118362.4),(5.0,358938.83),
        (6.0,889936.3),(7.0,1919316.07),(8.0,3736880.84),(10.0,11386930.38),
        (12.0,28314372.32),(15.0,86369763.43),(18.0,214883030.14),(20.0,363895352.48)
    ]

    def fit_linear(Bv, Cv):
        us = [(x+Bv)*math.exp(Cv*x) for (x,y) in pos_data]
        fs = [y for (x,y) in pos_data]
        n = len(us)
        su = sum(us); sf = sum(fs)
        suu = sum(u*u for u in us)
        suf = sum(u*f for u,f in zip(us,fs))
        den = n*suu - su*su
        if abs(den) < 1e-9:
            return None
        A = (n*suf - su*sf)/den
        D = (sf - A*su)/n
        res = sum((A*u + D - f)**2 for u,f in zip(us,fs))
        return (res, A, D)

    best = None
    Bv = -6.0
    while Bv <= 0.5:
        Cv = 0.3
        while Cv <= 1.5:
            r = fit_linear(Bv, Cv)
            if r is not None and (best is None or r[0] < best[0]):
                best = (r[0], r[1], Bv, Cv, r[2])
            Cv += 0.02
        Bv += 0.1

    if best is not None:
        _, A0, B0, C0, D0 = best
        Bv = B0 - 0.15
        while Bv <= B0 + 0.15:
            Cv = C0 - 0.15
            while Cv <= C0 + 0.15:
                r = fit_linear(Bv, Cv)
                if r is not None and r[0] < best[0]:
                    best = (r[0], r[1], Bv, Cv, r[2])
                Cv += 0.005
            Bv += 0.005

    if best is not None:
        _, A, B, C, D = best
    else:
        A, B, C, D = 1.0, -1.0, 1.0, 0.0

    def f(x):
        if x < 0:
            return a*x*x*x + b*x + c
        else:
            return A*(x+B)*math.exp(C*x) + D

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(f(x))
        except Exception:
            ys.append(None)
    return {"y": ys}
