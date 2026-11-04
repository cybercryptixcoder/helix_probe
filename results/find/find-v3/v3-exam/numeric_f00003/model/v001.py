def predict(probe):
    # Observations [E1]:
    # - Large |x| gives large positive y, roughly quadratic (88.2->21854, 66->12951, 72.7->15366, -61.7->5086, 21.3->2092)
    # - Small |x| gives ~-20.45 (2.9, -6.0 both -> -20.4469)
    # - x=-20.3 -> -15.87, x=-24.3 -> 166.21 (asymmetric, not pure even function)
    # Hypothesis: y = a*x^2 + b*x + c, with a floor near -20.45 for small x.
    # Fit quadratic through large points: use 88.2->21854.2, 66->12950.8, -61.7->5086.1
    # Solve a,b,c.
    import math
    def quad(x):
        # solve 3x3 via the three points
        x1,y1=88.2,21854.2087
        x2,y2=66.0,12950.8364
        x3,y3=-61.7,5086.1272
        # a x^2 + b x + c
        d1=x1*x1-x2*x2; e1=x1-x2; f1=y1-y2
        d2=x1*x1-x3*x3; e2=x1-x3; f2=y1-y3
        det=d1*e2-d2*e1
        a=(f1*e2-f2*e1)/det
        b=(d1*f2-d2*f1)/det
        c=y1-a*x1*x1-b*x1
        return a*x*x+b*x+c
    out=[]
    for x in probe["x"]:
        v=quad(x)
        # floor near -20.45 for small x
        if v < -20.4469:
            v = -20.4469
        out.append(v)
    return {"y": out}
