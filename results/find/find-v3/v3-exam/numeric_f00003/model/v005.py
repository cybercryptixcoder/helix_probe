def predict(probe):
    # Beliefs:
    # - True floor F = -20.4469 for central plateau [E2,E4,E6]
    # - Plateau: x in (-20, 3.8) -> floor [E2,E4,E6]
    # - Positive branch is quadratic for x >= ~3.8 [E2,E4,E8,E10]
    #   E10 shows curvature is NOT a single quadratic: small-x (12-30) and
    #   large-x (50-85) don't fit one parabola. Fit quadratic to large-x
    #   region (50,8005.6264),(85,20475.1601),(128,39006.1248).
    #   Small-x region (4-30) fits its own quadratic through
    #   (4.0,-12.9234),(12,902.7117),(30,3458.112).
    #   Transition between them appears smooth; blend near x~40.
    # - Negative branch is quadratic for x <= ~-20 [E1,E6,E8]
    #   Fit through (-25,204.0128),(-70,6954.3912),(-128,24838.9457)
    # - Transition at x=-20: sharp (floor at -20.0, -7.643 at -20.5) [E6]
    # - Transition at x~3.8: sharp (floor at 3.6, -20.1608 at 3.8) [E4]
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

    # large-x positive quadratic
    apl, bpl, cpl = solve3((50.0, 8005.6264), (85.0, 20475.1601), (128.0, 39006.1248))
    # small-x positive quadratic
    aps, bps, cps = solve3((4.0, -12.9234), (12.0, 902.7117), (30.0, 3458.112))
    # negative quadratic
    an, bn, cn = solve3((-25.0, 204.0128), (-70.0, 6954.3912), (-128.0, 24838.9457))

    def pos(x):
        vs = aps*x*x + bps*x + cps
        vl = apl*x*x + bpl*x + cpl
        # blend between x=30 and x=50
        if x <= 30.0:
            return vs
        if x >= 50.0:
            return vl
        t = (x - 30.0) / 20.0
        return (1 - t) * vs + t * vl

    out = []
    for x in probe["x"]:
        if x >= 3.8:
            v = pos(x)
        elif x <= -20.0:
            v = an*x*x + bn*x + cn
        else:
            v = FLOOR
        if v < FLOOR:
            v = FLOOR
        out.append(v)
    return {"y": out}
