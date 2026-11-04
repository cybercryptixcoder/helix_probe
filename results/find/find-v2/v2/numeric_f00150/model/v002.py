def predict(probe):
    # Ordinary inputs |x| >= ~1.5: y = 0.2*x^5 exactly [E8,E12,E18,E20,E22,E23]
    #   ratio y/x^5 = 0.2 confirmed across magnitudes 2..128 [E22,E18,E23]
    # Small-|x| anomaly: |x| < ~1.5 the x^5 law breaks [E10,E16,E18,E20]
    # Positive side anomaly is smooth and symmetric-looking in |x|:
    #   x=0.3:3.8276,0.5:2.9625,0.75:1.5342,1.0:-0.2,1.1:-1.7077,
    #   1.2:-2.7576,1.3:-3.3418,1.4:-3.1972,1.5:-2.0 [E16,E18,E20]
    # Negative side: y=0 for |x|<=0.5 (x=-0.5,-0.25,-0.05,-0.005,-0.002) [E10,E12]
    #   x=-0.9:0, x=-1.1:-12.1679 [E14] -> negative side is NOT mirror of positive
    #   Guess: negative side is 0 up to ~0.6, then jumps; use 0 for |x|<0.6,
    #   and for 0.6<=|x|<1.5 interpolate toward 0.2*x^5 (?) [E14]
    # At |x|>=1.5 both signs follow 0.2*x^5 [E14,E22]
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax >= 1.5:
                y = 0.2 * x**5
            elif x > 0:
                # positive-side smooth anomaly, interpolate known points
                pts = [(0.0,5.0),(0.3,3.8276),(0.5,2.9625),(0.6,2.4428),
                       (0.75,1.5342),(0.9,0.5037),(1.0,-0.2),(1.1,-1.7077),
                       (1.2,-2.7576),(1.3,-3.3418),(1.4,-3.1972),(1.5,-2.0)]
                y = _interp(pts, x)
            else:
                # negative side: flat 0 for small |x|, then rise to 0.2*x^5
                if ax < 0.6:
                    y = 0.0
                else:
                    t = (ax - 0.6) / (1.5 - 0.6)
                    y = (1 - t) * (-12.1679) * ((ax - 0.6) / 0.5) + t * (0.2 * x**5)
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}


def _interp(pts, x):
    # piecewise-linear interpolation over sorted (x,y) points
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]
