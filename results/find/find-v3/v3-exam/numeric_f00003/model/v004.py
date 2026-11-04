def predict(probe):
    # Beliefs:
    # - True floor F = -20.4469 for a central plateau [E2,E4,E6]
    # - Plateau: x in (-20, 3.8) -> floor [E2,E4,E6]
    # - Positive branch is quadratic for x >= ~3.8 [E2,E4,E8]
    #   E8: 95->24784.69, 128->39006.12, 50->8005.63, 70->14370.13
    #   E4: 4.0->-12.9234, 4.2->-5.6859, 4.5->13.1559, 10->650.4807
    #   E2: 5->48.3879, 6->146.0188, 7->272.1343, 8->398.2498
    #   Fit quadratic through (4.0,-12.9234),(50,8005.6264),(128,39006.1248)
    # - Negative branch is quadratic for x <= ~-20 [E1,E6,E8]
    #   E6: -20.5->-7.643, -21->12.9172, -25->204.0128, -50->2930.4276
    #   E8: -105->17482.21, -128->24838.95, -70->6954.39
    #   Fit quadratic through (-25,204.0128),(-70,6954.3912),(-128,24838.9457)
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

    ap, bp, cp = solve3((4.0, -12.9234), (50.0, 8005.6264), (128.0, 39006.1248))
    an, bn, cn = solve3((-25.0, 204.0128), (-70.0, 6954.3912), (-128.0, 24838.9457))

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
