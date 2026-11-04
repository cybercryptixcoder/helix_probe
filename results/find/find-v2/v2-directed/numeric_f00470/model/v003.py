import math

def predict(probe):
    # Beliefs:
    # Negative side (x < 0): f(x) = a*x^3 + b*x + c, valid for x <= ~-1 [E11, E3, E6, E14]
    #   Cubic matches E11/E3/E6 well down to about x=-1.2; below that near-zero region takes over.
    # Near-zero region (roughly -1.2 < x < ~1.2): separate smooth curve, values ~ -25..28 [E2, E8, E13, E14]
    #   Looks like a damped oscillation / bump: rises to ~28 near x=-0.3, dips to ~-24 near x=0.55,
    #   then rises into the exponential. Not the cubic, not the exponential.
    # Positive side (x > ~1.2): f(x) = A*(x+B)*exp(C*x) + D [E12, E10, E4, E5]
    #   Fit from clean positive points x>=1.5.

    # --- Negative cubic from E11 ---
    # x=-20: -8000a -20b + c = -112324723.7
    # x=-10: -1000a -10b + c = -3613822.11
    # x=-5:   -125a  -5b + c = -120306.515
    a = (10871090.159 - 698703.119) / 525.0
    b = 698703.119 - 175.0 * a
    c = -3613822.11 + 1000.0 * a + 10.0 * b

    # --- Positive exponential fit A*(x+B)*exp(C*x)+D ---
    pos_data = [
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

    # --- Near-zero bump: interpolate from observed near-zero data ---
    # Combine E2, E8, E13, E14 near-zero points (|x| < ~1.2) into a sorted table.
    # These are the ground-truth samples of the bump region.
    bump_pts = [
        (-1.2,-119.8396),(-1.0,-37.091),(-0.9,-11.1291),(-0.8,5.8605),
        (-0.7,17.8289),(-0.6,23.3562),(-0.5,26.692),(-0.4,26.7966),
        (-0.3,27.3822),(-0.2,27.9533),(-0.15,25.9696),(-0.12,24.3117),
        (-0.1,25.8483),(-0.08,23.3666),(-0.06,22.8679),(-0.05,21.6125),
        (-0.04,23.3533),(-0.02,20.8237),(-0.01,24.5535),(-0.005,23.4172),
        (-0.001,22.3075),(0.0,21.28),(0.005,19.7965),(0.01,22.3118),
        (0.02,20.3392),(0.04,17.3826),(0.05,17.3992),(0.06,19.4129),
        (0.08,12.4335),(0.1,12.4473),(0.12,9.4578),(0.15,5.4751),
        (0.2,0.5408),(0.25,-3.2851),(0.3,-8.9163),(0.35,-11.2456),
        (0.4,-15.1413),(0.45,-19.4426),(0.5,-22.9553),(0.55,-24.4478),
        (0.6,-23.6466),(0.65,-22.232),(0.7,-17.834),(0.75,-14.0279),
        (0.8,-2.3302),(0.9,23.9947),(1.0,70.35),(1.1,143.1608),
        (1.2,250.2048)
    ]
    bump_pts.sort()

    def bump(x):
        # linear interpolation between nearest bump points; clamp at ends
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

    # Region boundaries: cubic for x <= -1.2, bump for -1.2 < x < 1.2, exponential for x >= 1.2
    # (blend at boundaries to avoid discontinuities)
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
