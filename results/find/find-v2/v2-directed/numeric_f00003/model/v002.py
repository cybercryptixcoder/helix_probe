def predict(probe):
    # f is flat at -20.4469 on [-20, 2] inclusive [E1, E2]
    # Outside, f rises smoothly and monotonically with |x| [E1]
    # Left side rises faster than right at same |x|: f(-30)=548 vs f(30)? [E1, E2]
    # Transition is smooth, not a jump: near -20.5 f=-7.6, near 4 f=-12.9 [E2]
    # Shape is roughly exponential-ish / power-like, not linear [E1]
    # Model: flat core, then smooth curve on each side fit to anchors.
    import math
    flat = -20.4469
    lo, hi = -20.0, 2.0

    # Right side anchors (x, y) from E1+E2
    right = [(2,flat),(2.5,flat),(3,flat),(3.5,flat),(4,-12.9234),(4.5,13.1559),
             (5,48.3879),(6,146.0188),(7,272.1343),(10,650.4807),(20,1914.2369),
             (40,5505.5302),(64,12269.8411),(100,26939.4501),(120,35558.5035),(128,39006.1248)]
    # Left side anchors (|x|, y) from E1+E2
    left = [(20,flat),(20.5,-7.643),(21,12.9172),(22,54.0378),(24,150.0136),
            (27,334.5351),(30,548.2541),(40,1531.8654),(64,5576.1055),
            (100,15882.924),(128,24838.9457)]

    def interp(pts, x):
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            return pts[-1][1]
        for i in range(len(pts)-1):
            x0,y0 = pts[i]; x1,y1 = pts[i+1]
            if x0 <= x <= x1:
                t = (x-x0)/(x1-x0)
                return y0 + t*(y1-y0)
        return pts[-1][1]

    out = []
    for x in probe.get("x", []):
        try:
            if lo <= x <= hi:
                out.append(flat)
            elif x > hi:
                out.append(interp(right, x))
            else:
                out.append(interp(left, -x))
        except Exception:
            out.append(None)
    return {"y": out}
