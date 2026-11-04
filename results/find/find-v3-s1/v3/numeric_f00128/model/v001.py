import math

def predict(probe):
    # Model: f(x) is approximately cubic (odd) in x.
    # Evidence E1: y/x roughly grows with x^2; signs match x; magnitude ~ x^3 scale.
    # Fit a cubic y = a*x + b*x^3 through the data.
    # Using least squares on E1 points.
    xs = [-93.6,88.9,67.5,-62.7,-1.2,-12.9,38.8,73.9,-104.0,-120.7]
    ys = [635.1377,-1491.2068,-1129.5494,426.2512,10.5797,89.5991,-644.5229,-1237.7086,705.4426,818.336]
    # Build normal equations for y = a*x + b*x^3
    s11 = sum(x*x for x in xs)
    s13 = sum(x**4 for x in xs)
    s33 = sum(x**6 for x in xs)
    t1 = sum(x*y for x,y in zip(xs,ys))
    t3 = sum((x**3)*y for x,y in zip(xs,ys))
    det = s11*s33 - s13*s13
    if abs(det) < 1e-12:
        a, b = 0.0, 0.0
    else:
        a = (t1*s33 - t3*s13)/det
        b = (s11*t3 - s13*t1)/det
    out = []
    for x in probe["x"]:
        out.append(a*x + b*x**3)
    return {"y": out}
