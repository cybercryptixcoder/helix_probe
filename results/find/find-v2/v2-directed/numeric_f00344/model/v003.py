import math

def predict(probe):
    # Beliefs (revised after E12):
    # - Positive side x>=1 is a SINGLE clean exponential a*b^x [E8,E12].
    #   Fit from f(1)=-41.7 and f(128)=-328399499.2:
    #   b = (328399499.2/41.7)^(1/127); a = -41.7/b.
    #   Check: f(2)=-79.6, f(4)=-528, f(8)=-6443.2, f(16)=-90763.2,
    #   f(40)=-3262660.8, f(100)=-122991196.8 [E8,E1,E12].
    # - Negative side x<=-3: clean exponential -A*c^(-x) [E10].
    #   From f(-3)=-15, f(-80)=-47610123.7: c=(47610123.7/15)^(1/77).
    #   Check f(-4)=-106.1, f(-8)=-3320.5, f(-16)=-66110.9, f(-64)=-19342450.1.
    # - Hump region -3<x<=-1: f(-3)=-15, rises to max ~+0.0743 at x=-2.1,
    #   back to f(-1)=-7.4 [E11,E10]. Fit a smooth curve through these.
    # - Negative plateau -1<x<0: f(-1)=-7.4 to f(0-)=-11.692 [E9,E5].
    # - Positive plateau 0<x<1: f(0+)=-36.8 to f(1)=-41.7 [E5,E3,E4].
    # - f(0)=472.73 spike [E1].

    # Positive exponential
    b_pos = (328399499.2 / 41.7) ** (1.0 / 127.0)
    a_pos = -41.7 / b_pos

    # Negative exponential (x<=-3)
    c_neg = (47610123.7 / 15.0) ** (1.0 / 77.0)
    A_neg = 15.0 / (c_neg ** 3.0)

    def pos_exp(x):
        return a_pos * (b_pos ** x)

    def neg_exp(x):
        return -A_neg * (c_neg ** (-x))

    def lagrange(x, pts):
        total = 0.0
        for i, (xi, yi) in enumerate(pts):
            term = yi
            for j, (xj, _) in enumerate(pts):
                if i != j:
                    term *= (x - xj) / (xi - xj)
            total += term
        return total

    def f(x):
        if x == 0:
            return 472.73
        if x >= 1:
            return pos_exp(x)
        if x <= -3:
            return neg_exp(x)
        if -3 < x <= -1:
            # hump: through (-3,-15),(-2.1,0.0743),(-1,-7.4)
            return lagrange(x, [(-3.0, -15.0), (-2.1, 0.0743), (-1.0, -7.4)])
        if -1 < x < 0:
            # negative plateau: (-1,-7.4),(-0.5,-10.375),(0,-11.692)
            return lagrange(x, [(-1.0, -7.4), (-0.5, -10.375), (0.0, -11.692)])
        # 0 < x < 1: positive plateau (0,-36.8),(0.5,-37.825),(1,-41.7)
        return lagrange(x, [(0.0, -36.8), (0.5, -37.825), (1.0, -41.7)])

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(f(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}
