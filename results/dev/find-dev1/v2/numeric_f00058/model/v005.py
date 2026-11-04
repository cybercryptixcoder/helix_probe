def predict(probe):
    # f is exactly -84.3663 on a flat central region |x| <= ~50 [E1,E2,E3,E4,E5]
    # Positive side: flat through 50.5, first nonzero at 51 [E6]
    # Negative side: flat through -51, first nonzero at -52 [E5]
    # Positive growth (E6): 51->12.4, 52->428, 53->843.7, 54->1259.3, 55->1674.9,
    #   57->3230.4, 58->4433.2, 62->10136.6, 66->21806, 70->35110, 72->42011,
    #   80->72734, 96->134518, 112->196301, 120->227192, 124->242638, 127->254223
    # Negative growth (E5): -52->1853.9, -53->4467.2, -54->7080.4, -56->12306.9,
    #   -58->19684.6, -60->27779.4, -62->35950.7, -64->44756.7, -66->53562.8,
    #   -68->62368.8, -70->71174.8
    # Positive curve is concave (slope decreasing), saturating toward ~258084 at 128 [E1]
    # Negative curve is nearly linear in |x| past onset, reaching 326550 at -128 [E1]
    # Model each side as a smooth interpolant through the observed knots.
    import math
    c = -84.3663
    # Positive knots (x, y) from E6 + E1
    pos = [(50.5, c), (51, 12.4118), (52, 428.046), (53, 843.6803),
           (54, 1259.3145), (55, 1674.9487), (57, 3230.3677), (58, 4433.2432),
           (62, 10136.592), (66, 21805.9764), (70, 35110.0497), (72, 42011.4303),
           (80, 72734.4149), (96, 134517.6027), (112, 196300.7905),
           (120, 227192.3844), (124, 242638.1814), (127, 254222.5291),
           (128, 258083.9783)]
    # Negative knots (|x|, y) from E5 + E1
    neg = [(51, c), (52, 1853.9413), (53, 4467.1854), (54, 7080.4295),
           (56, 12306.9177), (58, 19684.5999), (60, 27779.3796),
           (62, 35950.6853), (64, 44756.7193), (66, 53562.7534),
           (68, 62368.7874), (70, 71174.8214), (128, 326549.8085)]

    def interp(knots, ax):
        if ax <= knots[0][0]:
            return c
        if ax >= knots[-1][0]:
            return knots[-1][1]
        for i in range(len(knots) - 1):
            x0, y0 = knots[i]
            x1, y1 = knots[i + 1]
            if x0 <= ax <= x1:
                t = (ax - x0) / (x1 - x0)
                # smoothstep for smoothness
                s = t * t * (3 - 2 * t)
                return y0 + (y1 - y0) * s
        return knots[-1][1]

    out = []
    for x in probe.get("x", []):
        try:
            if x is None:
                out.append(None); continue
            ax = abs(x)
            if x >= 0:
                out.append(interp(pos, ax))
            else:
                out.append(interp(neg, ax))
        except Exception:
            out.append(None)
    return {"y": out}
