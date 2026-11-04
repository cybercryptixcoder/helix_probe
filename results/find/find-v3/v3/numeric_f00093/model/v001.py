def predict(probe):
    # Model hypothesis: f(x) is roughly linear with negative slope.
    # Evidence E1: y decreases as x increases.
    # Fit a line y = a*x + b from E1 data.
    # E1 points: (88.2,-63.955),(66.0,-59.9589),(-20.3,18.7483),(-61.7,40.8138),
    # (2.9,-18.576),(-24.3,20.881),(72.7,-61.1649),(-50.4,34.7953),(-6.0,6.6373),(21.3,-45.8131)
    # Compute least squares.
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys = [-63.955,-59.9589,18.7483,40.8138,-18.576,20.881,-61.1649,34.7953,6.6373,-45.8131]
    n = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs); sxy = sum(x*y for x,y in zip(xs,ys))
    denom = n*sxx - sx*sx
    a = (n*sxy - sx*sy)/denom
    b = (sy - a*sx)/n
    out = []
    for x in probe["x"]:
        out.append(a*x + b)
    return {"y": out}
