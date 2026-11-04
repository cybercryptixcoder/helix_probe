def predict(probe):
    # Observations:
    # - Small |x| (|x|<=3) gives constant -20.4469 (a true floor) [E1, E2]
    # - For x>=4, y rises quadratically: 4->-12.92, 5->48.39, 6->146.02, 7->272.13, 8->398.25
    # - For x<=-4, y stays at floor -20.4469 (asymmetric! negative side floored) [E2]
    # - Large positive x: 21.3->2091.93, 66->12950.84, 72.7->15366.07, 88.2->21854.21
    # - x=-20.3 -> -15.87, x=-24.3 -> 166.21, x=-50.4 -> 2995.40, x=-61.7 -> 5086.13
    #   So negative side is NOT floored at large |x|; it rises too.
    # Hypothesis: y = a*x^2 + b*x + c for x>=4; floor -20.4469 for -3<=x<=3.
    # For x<=-4: also quadratic but shifted. Let's fit.
    #
    # Fit positive branch through (4,-12.9234),(8,398.2498),(88.2,21854.2087):
    # Let's solve a,b,c.
    import math
    def solve3(p1,p2,p3):
        x1,y1=p1; x2,y2=p2; x3,y3=p3
        d1=x1*x1-x2*x2; e1=x1-x2; f1=y1-y2
        d2=x1*x1-x3*x3; e2=x1-x3; f2=y1-y3
        det=d1*e2-d2*e1
        a=(f1*e2-f2*e1)/det
        b=(d1*f2-d2*f1)/det
        c=y1-a*x1*x1-b*x1
        return a,b,c
    # Positive branch
    ap,bp,cp = solve3((4.0,-12.9234),(8.0,398.2498),(88.2,21854.2087))
    # Negative branch: fit through (-24.3,166.2134),(-50.4,2995.4039),(-61.7,5086.1272)
    an,bn,cn = solve3((-24.3,166.2134),(-50.4,2995.4039),(-61.7,5086.1272))
    FLOOR=-20.4469
    out=[]
    for x in probe["x"]:
        if -3.0 <= x <= 3.0:
            v=FLOOR
        elif x > 3.0:
            v=ap*x*x+bp*x+cp
            if v<FLOOR: v=FLOOR
        else:
            v=an*x*x+bn*x+cn
            if v<FLOOR: v=FLOOR
        out.append(v)
    return {"y": out}
