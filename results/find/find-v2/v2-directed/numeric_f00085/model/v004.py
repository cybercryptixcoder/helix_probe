import math

def predict(probe):
    # Beliefs about f(x):
    # - Flat plateau at -22.8021 for |x| <= 5.5 (positive side) [E2,E5]
    # - Flat plateau at -22.8021 for |x| <= 7.3 (negative side) [E3,E4]
    # - Positive transition: smooth ramp from 5.5 to 8, then convex growth [E2,E5]
    # - Negative transition: smooth ramp from 7.3 to 9, then convex growth [E3,E4]
    # - Both sides grow smoothly convex for |x|>=9; negative slightly above positive [E1]
    # - Positive large: 32->3704.23, 48->8241.66, 64->14110.97, 128->50592.64 [E1]
    # - Negative large: -64->14568.88, -128->51222.63 [E1]
    # - The transition is a smooth quadratic-like ramp, not linear [E4,E5]

    # Positive-side anchors (x, y)
    pos = [
        (0.0, -22.8021), (5.5, -22.8021), (5.9, -15.5897), (6.1, -1.5154),
        (6.25, 9.0403), (6.4, 19.596), (6.6, 33.6703), (6.75, 44.2261),
        (6.9, 54.7818), (7.1, 68.8561), (7.2, 75.8933), (7.3, 82.9304),
        (7.4, 89.9676), (7.6, 104.0419), (7.8, 118.1162), (7.9, 125.1534),
        (8.0, 132.1905), (8.1, 139.2277), (8.2, 146.2648), (8.25, 149.7834),
        (8.5, 167.3763), (9.0, 202.5621), (10.0, 272.9336), (11.0, 343.3051),
        (12.0, 421.8308), (13.0, 530.6351), (14.0, 639.4395), (15.0, 748.2438),
        (16.0, 857.0481), (20.0, 1357.3016), (32.0, 3704.2314),
        (48.0, 8241.6569), (64.0, 14110.9665), (128.0, 50592.6368),
    ]
    # Negative-side anchors (use |x|, y)
    neg = [
        (0.0, -22.8021), (7.3, -22.8021), (7.4, -19.3504), (7.6, -6.6407),
        (7.8, 6.069), (7.9, 12.4239), (8.0, 21.8213), (8.1, 34.2066),
        (8.25, 52.7846), (8.5, 83.748), (8.75, 114.7114), (9.0, 145.6747),
        (9.25, 176.6381), (9.5, 207.6015), (9.75, 238.5648), (10.0, 269.5282),
        (10.5, 331.4549), (11.0, 393.3816), (11.5, 455.3084), (12.0, 517.2351),
        (12.5, 579.1618), (13.0, 641.0886), (13.5, 703.0153), (14.0, 764.942),
        (14.5, 826.8687), (15.0, 888.7955), (16.0, 1012.6489), (20.0, 1508.0627),
        (24.0, 2101.094), (32.0, 3704.2314), (48.0, 8241.6569),
        (64.0, 14568.8817), (80.0, 22886.108), (96.0, 32331.6141),
        (112.0, 41777.1201), (128.0, 51222.6262),
    ]

    def interp(pts, x):
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            (x0, y0), (x1, y1) = pts[-2], pts[-1]
            slope = (y1 - y0) / (x1 - x0)
            return y1 + slope * (x - x1)
        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return pts[-1][1]

    out = []
    for xv in probe.get("x", []):
        try:
            xv = float(xv)
        except Exception:
            out.append(None)
            continue
        if xv >= 0:
            out.append(interp(pos, xv))
        else:
            out.append(interp(neg, -xv))
    return {"y": out}
