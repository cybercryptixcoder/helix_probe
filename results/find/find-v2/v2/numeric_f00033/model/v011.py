import math

def predict(probe):
    # Beliefs (mechanism, from the evidence):
    # A: Main bump peaks at x=0 with f(0)~0.387, asymmetric: right wider than left [E2,E4].
    # B: Right bump x in [0,5]: f(1)=0.255, f(2)=0.12, f(3)=0.033, f(4)=0.0099, f(5)=0.0012 [E4,E14].
    # C: Left bump x in [-2.5,0]: f(-1)=0.197, f(-2)=0.0575, f(-2.5)=0.0221 [E10,E12,E22].
    # D: Left tail x in [-3,-2.5]: sharp drop 0.0221 -> 0.0082 (kink at -2.9) [E22].
    # E: Left shoulder x in [-6,-3]: smooth decay 0.008 -> 0.0 at -6 [E10,E12,E16,E22].
    # F: Left negative plateau x <= -6: smooth negative, -0.0002 at -8, -0.0012 at -20,
    #    -0.0032 at -45..-50, ~-0.0044 at -128 [E6,E9,E20].
    # G: Right dip x in [5,22]: min ~-0.0061 at x=12, recovering to ~-0.0004 by x=22 [E8,E14,E18].
    # H: Far right x > 22: near-flat ~-0.0004, rising to ~-0.0001 by x~100+ [E1,E3,E5,E6,E17].
    # I: Smooth piecewise interpolation through measured points.

    def f(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        if math.isnan(x) or math.isinf(x):
            return None

        if x >= 0:
            if x <= 5.0:
                return 0.3868 * math.exp(-0.249 * x - 0.168 * x * x)
            if x <= 22.0:
                pts = [(5,0.0012),(6,0.0001),(7,-0.001),(8,-0.0021),(9,-0.0032),
                       (10,-0.0043),(11,-0.0054),(12,-0.0061),(13,-0.0055),(14,-0.0049),
                       (15,-0.0043),(16,-0.0037),(17,-0.0031),(18,-0.0025),(20,-0.0013),(22,-0.0004)]
                for i in range(len(pts)-1):
                    x0,y0 = pts[i]; x1,y1 = pts[i+1]
                    if x <= x1:
                        t = (x-x0)/(x1-x0)
                        return y0 + t*(y1-y0)
                return -0.0004
            if x <= 50.0:
                return -0.0004
            if x <= 128.0:
                t = (x-50.0)/78.0
                return -0.0004 + t*(-0.0001 + 0.0004)
            return -0.0001

        # Left side (x < 0)
        ax = -x
        if ax <= 2.5:
            # fit A*exp(-a*ax - b*ax^2): A=0.3868, a=0.397, b=0.278
            return 0.3868 * math.exp(-0.397 * ax - 0.278 * ax * ax)
        if ax <= 3.0:
            # sharp drop from 0.0221 at 2.5 to 0.0082 at 2.9, then 0.008 at 3.0 [E22]
            pts = [(2.5,0.0221),(2.6,0.0177),(2.7,0.0133),(2.8,0.0089),(2.9,0.0082),(3.0,0.008)]
            for i in range(len(pts)-1):
                x0,y0 = pts[i]; x1,y1 = pts[i+1]
                if ax <= x1:
                    t = (ax-x0)/(x1-x0)
                    return y0 + t*(y1-y0)
            return 0.008
        if ax <= 6.0:
            pts = [(3,0.008),(3.5,0.0066),(4,0.0053),(4.5,0.004),(5,0.0027),
                   (5.5,0.0014),(6,0.0)]
            for i in range(len(pts)-1):
                x0,y0 = pts[i]; x1,y1 = pts[i+1]
                if ax <= x1:
                    t = (ax-x0)/(x1-x0)
                    return y0 + t*(y1-y0)
            return 0.0
        pts = [(6,0.0),(7,-0.0001),(8,-0.0002),(9,-0.0003),(10,-0.0004),(11,-0.0004),
               (12,-0.0005),(13,-0.0006),(14,-0.0007),(15,-0.0008),(16,-0.0009),(17,-0.001),
               (18,-0.0011),(19,-0.0011),(20,-0.0012),(22,-0.0014),(25,-0.0017),(30,-0.0021),
               (35,-0.0026),(40,-0.003),(45,-0.0032),(50,-0.0032),(60,-0.0032),(128,-0.0044)]
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
