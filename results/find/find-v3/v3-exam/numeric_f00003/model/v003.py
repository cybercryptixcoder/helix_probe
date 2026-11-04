def predict(probe):
    # Beliefs:
    # - True floor F = -20.4469 for a central plateau [E1,E2,E4]
    # - Plateau: x <= 3.8 (and all negative x down to -128) -> floor [E2,E4]
    #   E4: 3.8 -> -20.1608 (just above floor), 4.0 -> -12.9234; so branch starts ~3.8
    # - Positive branch is quadratic for x >= ~3.8 [E2,E4]
    # - Negative side: floor for small |x|, but rises again at large |x| [E1]
    #   E1: -20.3 -> -15.87, -24.3 -> 166.21, -50.4 -> 2995.40, -61.7 -> 5086.13
    #   So negative branch is also quadratic, but only kicks in at large |x|.
    #   Fit negative branch through (-24.3,166.2134),(-50.4,2995.4039),(-61.7,5086.1272)
    # - Positive branch: fit through (4.0,-12.9234),(8.0,398.2498),(88.2,21854.2087)
    #   E4 check: 4.2 -> -5.6859, 4.5 -> 13.1559, 10 -> 650.4807
    FLOOR = -20.4469

    def solve3(p1, p2, p3):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3
        d1 = x1*x1 - x2*x2; e1 = x1 - x2; f1 = y1 - y2
        d2 = x1*x1 - x3*x3; e2 = x1 - x3; f2 = y1 - y3
        det = d1*e2 - d2*e1
        a = (f1*e2 - f2*e1) / det
        b = (d1*f2 - d2*f1) / det
        c = y1 - a*x1*x1 - b*x1
        return a, b, c

    ap, bp, cp = solve3((4.0, -12.9234), (8.0, 398.2498), (88.2, 21854.2087))
    an, bn, cn = solve3((-24.3, 166.2134), (-50.4, 2995.4039), (-61.7, 5086.1272))

    out = []
    for x in probe["x"]:
        if x >= 3.8:
            v = ap*x*x + bp*x + cp
        elif x <= -20.0:
            v = an*x*x + bn*x + cn
        else:
            v = FLOOR
        if v < FLOOR:
            v = FLOOR
        out.append(v)
    return {"y": out}
