def predict(probe):
    # f is flat at -20.4469 on [-20, 2] inclusive [E1, E2]
    # Outside, f rises smoothly and monotonically with |x| [E1]
    # Left side rises faster than right at same |x| [E1, E2]
    # Transition is smooth, not a jump [E2, E3]
    # Curve is convex/exponential-like, not linear; linear interp overestimates
    #   in gaps (E4: 8.5,9.5,15,25,50 all below linear interp) [E4]
    # So fit log(y - flat) vs x as roughly linear (exponential growth) on each side.
    import math
    flat = -20.4469
    lo, hi = -20.0, 2.0

    # Right side anchors (x, y) from E1-E4
    right = [(2,flat),(2.5,flat),(3,flat),(3.5,flat),(4,-12.9234),(4.5,13.1559),
             (5,48.3879),(5.5,95.9038),(6,146.0188),(6.5,209.0765),(7,272.1343),
             (7.5,335.192),(8,398.2498),(8.5,461.3075),(9,524.3653),(9.5,587.423),
             (10,650.4807),(11,776.5962),(12,902.7117),(13,1028.8272),(15,1281.0582),
             (20,1914.2369),(25,2597.6677),(40,5505.5302),(50,8005.6264),
             (64,12269.8411),(100,26939.4501),(120,35558.5035),(128,39006.1248)]
    # Left side anchors (|x|, y) from E1-E4
    left = [(20,flat),(20.125,flat),(20.25,-17.9232),(20.5,-7.643),(20.75,2.6371),
            (21,12.9172),(21.25,23.1974),(21.5,33.4775),(22,54.0378),(22.5,74.5981),
            (23,96.0144),(24,150.0136),(25,204.0128),(25.5,234.6088),(26,267.9176),
            (27,334.5351),(28,401.1526),(30,548.2541),(32,711.7673),(35,989.5128),
            (40,1531.8654),(45,2179.6225),(50,2930.4276),(64,5576.1055),(70,6954.3912),
            (80,9582.0843),(100,15882.924),(128,24838.9457)]

    def interp(pts, x):
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            return pts[-1][1]
        for i in range(len(pts)-1):
            x0,y0 = pts[i]; x1,y1 = pts[i+1]
            if x0 <= x <= x1:
                # exponential-ish interpolation in (y - flat) space when both above flat
                a0 = y0 - flat; a1 = y1 - flat
                if a0 > 0 and a1 > 0:
                    t = (x-x0)/(x1-x0)
                    return flat + a0 * (a1/a0)**t
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
