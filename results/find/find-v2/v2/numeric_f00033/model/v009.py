import math

def predict(probe):
    # Beliefs (mechanism, from the evidence):
    # A: Main bump peaks at x=0 with f(0)~0.387, asymmetric: right side wider than left [E2,E4].
    # B: Right side of bump (x>=0): f(1)=0.255, f(2)=0.12, f(3)=0.033, f(4)=0.0099, f(5)=0.0012 [E4,E14].
    # C: Left side of bump (x<0): f(-1)=0.197, f(-2)=0.0575, f(-3)=0.008 [E10,E12].
    # D: Left tail x in [-3,-6]: smooth decay 0.008 -> 0.0 at -6, then tiny negative [E10,E12,E16].
    # E: For x <= -6, small negative plateau approaching ~-0.0044 at -128 [E6,E9].
    # F: Right dip: from x=5 (0.0012) descending to minimum ~-0.0061 at x=12, recovering to ~-0.0004 by x=22 [E8,E14,E18].
    # G: For x > 22, near-flat ~-0.0004 up to ~50, then rises toward ~-0.0001 by x=128 [E1,E3,E5,E6].
    # H: Values are smooth; use piecewise interpolation through measured points.

    def f(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        if math.isnan(x) or math.isinf(x):
            return None

        # Right side of main bump (x >= 0), up to x=5
        if x >= 0:
            if x <= 5.0:
                # fit A*exp(-a*x - b*x^2): A=0.3868, a=0.249, b=0.168
                return 0.3868 * math.exp(-0.249 * x - 0.168 * x * x)
            # Right dip region x in [5, 22]
            if x <= 22.0:
                # points: (5,0.0012),(6,0.0001),(7,-0.001),(8,-0.0021),(9,-0.0032),
                # (10,-0.0043),(11,-0.0054),(12,-0.0061),(13,-0.0055),(14,-0.0049),
                # (15,-0.0043),(16,-0.0037),(17,-0.0031),(18,-0.0025),(20,-0.0013),(22,-0.0004)
                pts = [(5,0.0012),(6,0.0001),(7,-0.001),(8,-0.0021),(9,-0.0032),
                       (10,-0.0043),(11,-0.0054),(12,-0.0061),(13,-0.0055),(14,-0.0049),
                       (15,-0.0043),(16,-0.0037),(17,-0.0031),(18,-0.0025),(20,-0.0013),(22,-0.0004)]
                for i in range(len(pts)-1):
                    x0,y0 = pts[i]; x1,y1 = pts[i+1]
                    if x <= x1:
                        t = (x-x0)/(x1-x0)
                        return y0 + t*(y1-y0)
                return -0.0004
            # Far right x > 22
            if x <= 50.0:
                return -0.0004
            if x <= 128.0:
                t = (x-50.0)/78.0
                return -0.0004 + t*(-0.0001 + 0.0004)
            return -0.0001

        # Left side (x < 0)
        ax = -x
        if ax <= 3.0:
            # fit A*exp(-a*ax - b*ax^2): A=0.3868, a=0.397, b=0.278
            return 0.3868 * math.exp(-0.397 * ax - 0.278 * ax * ax)
        if ax <= 6.0:
            # points: (3,0.008),(3.5,0.0066),(4,0.0053),(4.5,0.004),(5,0.0027),
            # (5.5,0.0014),(6,0.0)
            pts = [(3,0.008),(3.5,0.0066),(4,0.0053),(4.5,0.004),(5,0.0027),
                   (5.5,0.0014),(6,0.0)]
            for i in range(len(pts)-1):
                x0,y0 = pts[i]; x1,y1 = pts[i+1]
                if ax <= x1:
                    t = (ax-x0)/(x1-x0)
                    return y0 + t*(y1-y0)
            return 0.0
        # ax > 6: negative plateau approaching -0.0044
        # points: (6,0.0),(7,-0.0001),(10,-0.0004),(20,-0.0012),(30,-0.0021),
        # (40,-0.003),(50,-0.0032),(60,-0.0032),(128,-0.0044)
        pts = [(6,0.0),(7,-0.0001),(10,-0.0004),(20,-0.0012),(30,-0.0021),
               (40,-0.003),(50,-0.0032),(60,-0.0032),(128,-0.0044)]
        if ax >= 128:
            return -0.0044
        for i in range(len(pts)-1):
            x0,y0 = pts[i]; x1,y1 = pts[i+1]
            if ax <= x1:
                t = (ax-x0)/(x1-x0)
                return y0 + t*(y1-y0)
        return -0.0044

    xs = probe.get("x", [])
    if not isinstance(xs, (list, tuple)):
        return {"y": []}
    ys = []
    for x in xs:
        try:
            ys.append(f(x))
        except Exception:
            ys.append(None)
    return {"y": ys}
