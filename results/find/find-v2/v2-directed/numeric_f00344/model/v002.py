import math

def predict(probe):
    # Model of f(x), piecewise:
    # - Positive side x>=1: clean exponential a*b^x. From E8: f(1)=-41.7,
    #   f(80)=-50682404.8. b = (50682404.8/41.7)^(1/79) ~ 1.0886; a=-41.7/b.
    #   Check f(2)=-79.6, f(4)=-528, f(8)=-6443.2, f(16)=-90763.2 [E8,E1,E4,E6].
    # - Negative side x<=-1: NOT a clean exponential near -1..-3. There is a
    #   hump: f(-1)=-7.4, f(-2)=-0.1, f(-2.1)=+0.0743 (max ~x=-2.1),
    #   f(-3)=-15, then exponential growth for x<=-3 [E10,E11,E1].
    #   For x<=-3: f ~ -A*c^(-x). From f(-3)=-15, f(-80)=-47610123.7:
    #   c=(47610123.7/15)^(1/77) ~ 1.0886; A=15/c^3.
    # - Plateau |x|<1: f(-1)=-7.4 rising to f(0-)~-11.69; f(0+)~-36.8
    #   rising to f(1)=-41.7. Jump at x=0 [E5,E9,E3].
    #   Negative plateau: f(-1)=-7.4, f(0)=-11.69, smooth [E9,E5].
    #   Positive plateau: f(0+)=-36.8, f(1)=-41.7 [E5,E3,E4].
    # - f(0)=472.73 spike [E1].

    b = 1.0886

    def pos_exp(x):
        # a*b^x with f(1)=-41.7
        return -41.7 * (b ** (x - 1.0))

    def neg_exp(x):
        # for x<=-3: f(x) = -A*c^(-x), f(-3)=-15
        return -15.0 * (b ** (-(x + 3.0)))

    def f(x):
        if x == 0:
            return 472.73
        if x >= 1:
            return pos_exp(x)
        if x <= -3:
            return neg_exp(x)
        if -3 < x <= -1:
            # hump region: f(-3)=-15, f(-2.1)=0.0743, f(-2)=-0.1,
            # f(-1.6)=-2.4123, f(-1)=-7.4 [E11,E10]
            # Use a quadratic through (-3,-15),(-2.1,0.0743),(-1,-7.4)
            # Fit: f(x)=a x^2 + b x + c
            # Solve quickly with Lagrange-style numeric fit.
            pts = [(-3.0, -15.0), (-2.1, 0.0743), (-1.0, -7.4)]
            (x1,y1),(x2,y2),(x3,y3) = pts
            # Lagrange interpolation
            def L(xx, xi, xj, xk):
                return ((xx-xj)*(xx-xk))/((xi-xj)*(xi-xk))
            return (y1*L(x,x1,x2,x3) + y2*L(x,x2,x1,x3) + y3*L(x,x3,x1,x2))
        if -1 < x < 0:
            # negative plateau: f(-1)=-7.4, f(0)=-11.69 [E9,E5]
            # smooth: use quadratic-ish; anchor f(-0.5)=-10.375 [E1]
            # fit through (-1,-7.4),(-0.5,-10.375),(0,-11.69)
            pts = [(-1.0, -7.4), (-0.5, -10.375), (0.0, -11.69)]
            (x1,y1),(x2,y2),(x3,y3) = pts
            def L(xx, xi, xj, xk):
                return ((xx-xj)*(xx-xk))/((xi-xj)*(xi-xk))
            return (y1*L(x,x1,x2,x3) + y2*L(x,x2,x1,x3) + y3*L(x,x3,x1,x2))
        # 0 < x < 1: positive plateau f(0+)=-36.8, f(0.5)=-37.825, f(1)=-41.7
        pts = [(0.0, -36.8), (0.5, -37.825), (1.0, -41.7)]
        (x1,y1),(x2,y2),(x3,y3) = pts
        def L(xx, xi, xj, xk):
            return ((xx-xj)*(xx-xk))/((xi-xj)*(xi-xk))
        return (y1*L(x,x1,x2,x3) + y2*L(x,x2,x1,x3) + y3*L(x,x3,x1,x2))

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(f(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}
