def predict(probe):
    # Hypothesis: f(x) = a*x^2 + b*x + c, fit from E1.
    # Fit using three points: x=66 -> -1473.8, x=-20.3 -> 232.267, x=2.9 -> -54.05
    # Solve quadratic through these.
    import math
    xs = [66.0, -20.3, 2.9]
    ys = [-1473.8, 232.267, -54.05]
    # Lagrange interpolation to get coefficients
    # Build quadratic a x^2 + b x + c
    # Using three points
    (x1,y1),(x2,y2),(x3,y3) = zip(xs,ys)
    denom = (x1-x2)*(x1-x3)
    a = (y1/((x1-x2)*(x1-x3)) + y2/((x2-x1)*(x2-x3)) + y3/((x3-x1)*(x3-x2)))
    b = (-y1*(x2+x3)/((x1-x2)*(x1-x3)) - y2*(x1+x3)/((x2-x1)*(x2-x3)) - y3*(x1+x2)/((x3-x1)*(x3-x2)))
    c = (y1*x2*x3/((x1-x2)*(x1-x3)) + y2*x1*x3/((x2-x1)*(x2-x3)) + y3*x1*x2/((x3-x1)*(x3-x2)))
    out = []
    for x in probe["x"]:
        out.append(a*x*x + b*x + c)
    return {"y": out}
