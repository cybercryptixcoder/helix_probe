import math

def predict(probe):
    # Beliefs:
    # Negative side (x <= -1.2): f(x) = a*x^3 + b*x + c exactly [E11, E3, E6, E14]
    #   Fit from clean E11 points; matches E3/E6 to ~1e-3.
    # Near-zero region (-1.2 < x < 1.2): a separate smooth curve, values ~ -25..28 [E2,E8,E13,E14,E15,E20]
    #   It is NOT symmetric and NOT the cubic. Dense samples show a bump peaking ~27-28 near x=-0.3,
    #   dipping to ~-24.5 near x=0.55, then rising into the exponential. Interpolate from samples.
    # Positive side (x >= 1.2): f(x) = A*(x+B)*exp(C*x) + D [E12, E10, E4, E5, E17, E18, E19]
    #   Fit from clean positive points x>=1.2 (E18 gives clean junction data).

    # --- Negative cubic from E11 (exact) ---
    a = (10871090.159 - 698703.119) / 525.0
    b = 698703.119 - 175.0 * a
    c = -3613822.11 + 1000.0 * a + 10.0 * b

    # --- Positive exponential fit A*(x+B)*exp(C*x)+D ---
    pos_data = [
        (1.2,249.2048),(1.3,397.7489),(1.4,600.6857),(1.5,867.6703),
        (1.6,1216.2568),(1.7,1663.035),(1.8,2225.7667),(1.9,2922.5229),
        (2.0,3783.82),(2.2,6090.1495),(2.4,9389.9878),(2.6,13972.4395),
        (2.8,20173.8524),(3.0,28403.19),(3.5,61001.1766),(4.0,118361.4),
        (4.5,212521.4372),(5.0,358939.83),(5.5,576897.0228),(6.0,889937.3),
        (7.0,1919316.07),(8.0,3736880.84),(10.0,11386930.38),
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

    # --- Near-zero bump: interpolate from all observed near-zero samples ---
    # Include E20 dense samples on negative side.
    bump_pts = [
        (-1.2,-119.8396),(-1.19,-115.3124),(-1.17,-100.7364),(-1.15,-94.7753),
        (-1.14,-90.017),(-1.12,-79.9283),(-1.1,-71.3889),(-1.09,-67.3175),
        (-1.07,-60.5559),(-1.05,-53.283),(-1.04,-49.8227),(-1.02,-39.2404),
        (-1.0,-35.091),(-0.99,-33.1721),(-0.97,-27.6331),(-0.95,-22.4759),
        (-0.94,-20.0345),(-0.92,-16.4142),(-0.9,-12.1291),(-0.89,-6.1066),
        (-0.87,-3.2915),(-0.85,-1.7689),(-0.84,-1.1123),(-0.82,4.0011),
        (-0.8,4.8605),(-0.79,8.1994),(-0.77,8.7045),(-0.75,10.9904),
        (-0.74,14.0551),(-0.72,16.0361),(-0.7,16.8289),(-0.65,20.5623),
        (-0.6,24.3562),(-0.55,25.3567),(-0.5,26.692),(-0.45,26.4734),
        (-0.4,27.7966),(-0.35,27.7434),(-0.3,26.3822),(-0.25,26.77),
        (-0.2,25.9533),(-0.15,25.9696),(-0.12,24.3117),(-0.1,25.8483),
        (-0.08,23.3666),(-0.06,22.8679),(-0.05,21.6125),(-0.04,23.3533),
        (-0.02,20.8237),(-0.01,24.5535),(-0.005,23.4172),(-0.001,22.3075),
        (0.0,21.28),(0.005,19.7965),(0.01,22.3118),(0.02,20.3392),
        (0.04,17.3826),(0.05,17.3992),(0.06,19.4129),(0.08,12.4335),
        (0.1,12.4473),(0.12,9.4578),(0.15,5.4751),(0.2,0.5408),
        (0.25,-3.2851),(0.3,-8.9163),(0.35,-11.2456),(0.4,-15.1413),
        (0.45,-19.4426),(0.5,-22.9553),(0.55,-23.4478),(0.6,-22.6466),
        (0.65,-22.232),(0.7,-14.834),(0.75,-13.0279),(0.8,-4.3302),
        (0.85,6.806),(0.9,26.9947),(0.95,45.9221),(1.0,71.35),
        (1.05,104.1206),(1.1,143.1608),(1.15,192.4859),(1.2,250.2048)
    ]
    bump_pts.sort()

    def bump(x):
        if x <= bump_pts[0][0]:
            return bump_pts[0][1]
        if x >= bump_pts[-1][0]:
            return bump_pts[-1][1]
        for i in range(len(bump_pts)-1):
            x0,y0 = bump_pts[i]
            x1,y1 = bump_pts[i+1]
            if x0 <= x <= x1:
                t = (x-x0)/(x1-x0) if x1 != x0 else 0.0
                return y0 + t*(y1-y0)
        return bump_pts[-1][1]

    def f(x):
        if x <= -1.2:
            return a*x*x*x + b*x + c
        elif x < 1.2:
            return bump(x)
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
