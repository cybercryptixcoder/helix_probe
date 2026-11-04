import math

def predict(probe):
    # Beliefs about f(x):
    # - f is even-ish but NOT exactly symmetric; negative side is slightly higher for large |x| [E1]
    # - Flat plateau at -22.8021 for |x| <= ~5.5 (positive) and |x| <= ~7.25 (negative) [E1,E2,E3]
    # - Positive transition: rises from -22.8 at x=5.5 to 132.19 at x=8, then smooth convex growth [E2]
    # - Negative transition: plateau extends to -7.25, then rises steeply: -7.5->-12.9955, -7.75->2.8916, -8->21.82, -9->145.67 [E1,E3]
    # - For |x|>=9 both sides grow smoothly convex; negative side slightly above positive [E1]
    # - Positive side: 8->132.19, 9->202.56, 10->272.93, 11->343.31, 12->421.83, 13->530.64, 14->639.44, 15->748.24, 16->857.05, 20->1357.30 [E1,E2]
    # - Positive large: 32->3704.23, 48->8241.66, 64->14110.97, 128->50592.64 [E1]
    # - Negative large: -16->1012.65, -32->3704.23, -48->8241.66, -64->14568.88, -128->51222.63 [E1]
    # - Negative mid: -10->269.53, -11->393.38, -12->517.24, -13->641.09, -14->764.94, -15->888.80, -20->1508.06, -24->2101.09 [E3]

    # Positive-side anchors (x, y)
    pos = [
        (0.0, -22.8021), (5.5, -22.8021), (6.0, -8.5526), (6.5, 26.6332),
        (7.0, 61.819), (7.25, 79.4118), (7.5, 97.0047), (7.75, 114.5976),
        (8.0, 132.1905), (8.25, 149.7834), (8.5, 167.3763), (9.0, 202.5621),
        (10.0, 272.9336), (11.0, 343.3051), (12.0, 421.8308), (13.0, 530.6351),
        (14.0, 639.4395), (15.0, 748.2438), (16.0, 857.0481), (20.0, 1357.3016),
        (32.0, 3704.2314), (48.0, 8241.6569), (64.0, 14110.9665),
        (128.0, 50592.6368),
    ]
    # Negative-side anchors (use |x|, y)
    neg = [
        (0.0, -22.8021), (7.25, -22.8021), (7.5, -12.9955), (7.75, 2.8916),
        (8.0, 21.8213), (9.0, 145.6747), (10.0, 269.5282), (11.0, 393.3816),
        (12.0, 517.2351), (13.0, 641.0886), (14.0, 764.942), (15.0, 888.7955),
        (16.0, 1012.6489), (20.0, 1508.0627), (24.0, 2101.094),
        (32.0, 3704.2314), (48.0, 8241.6569), (64.0, 14568.8817),
        (80.0, 22886.108), (96.0, 32331.6141), (112.0, 41777.1201),
        (128.0, 51222.6262),
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
