def predict(probe):
    # Observations from E1 suggest a roughly linear/smooth decreasing function of x.
    # Fit a line through the E1 points as a first hypothesis.
    # E1 points (x, y):
    pts = [(88.2,-63.955),(66.0,-59.9589),(-20.3,18.7483),(-61.7,40.8138),
           (2.9,-18.576),(-24.3,20.881),(72.7,-61.1649),(-50.4,34.7953),
           (-6.0,6.6373),(21.3,-45.8131)]
    n = len(pts)
    sx = sum(p[0] for p in pts)
    sy = sum(p[1] for p in pts)
    sxx = sum(p[0]*p[0] for p in pts)
    sxy = sum(p[0]*p[1] for p in pts)
    denom = n*sxx - sx*sx
    if denom == 0:
        a, b = 0.0, sy/n
    else:
        a = (n*sxy - sx*sy)/denom
        b = (sy - a*sx)/n
    # Linear fit: y = a*x + b  (?)
    out = []
    for x in probe.get("x", []):
        try:
            out.append(a*x + b)
        except Exception:
            out.append(None)
    return {"y": out}
