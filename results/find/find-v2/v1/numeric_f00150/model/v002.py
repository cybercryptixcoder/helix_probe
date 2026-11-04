import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            ax = abs(x)
            if ax >= 2:
                # Power law y ~ c * |x|^6, c slightly larger for negative side
                # Fit c from anchors: positive c~2.19, negative c~2.22
                c = 2.22 if x < 0 else 2.19
                # small correction: at |x|=2 the coefficient is lower
                # interpolate c from 2 at |x|=2 up to asymptote by |x|=8
                if ax < 8:
                    t = (ax - 2) / 6.0
                    c_low = 83.2/64.0 if x < 0 else 36.0/64.0
                    c = c_low + t * (c - c_low)
                val = c * (ax ** 6)
                ys.append(val)
            else:
                # Small |x|: use polynomial fit through known points
                # Known: (-2,83.2),(-1.75,10.1279),(-1.5,-5.4875),(-1.25,-11.3857),
                # (-1,-12),(-0.75,0),(-0.5,0),(-0.25,0),(-0.1,0),
                # (0,0),(0.1,4.5919),(0.25,4.0205),(0.5,2.9625),(0.75,1.5342),
                # (1,-0.2),(1.25,-3.123),(1.5,-2.0),(1.75,8.3293),(1.9,22.1992),(2,36)
                # Use piecewise linear interpolation on these anchors
                pts = [
                    (-2.0, 83.2), (-1.75, 10.1279), (-1.5, -5.4875), (-1.25, -11.3857),
                    (-1.0, -12.0), (-0.75, 0.0), (-0.5, 0.0), (-0.25, 0.0), (-0.1, 0.0),
                    (0.0, 0.0), (0.1, 4.5919), (0.25, 4.0205), (0.5, 2.9625), (0.75, 1.5342),
                    (1.0, -0.2), (1.25, -3.123), (1.5, -2.0), (1.75, 8.3293), (1.9, 22.1992),
                    (2.0, 36.0)
                ]
                if x <= pts[0][0]:
                    ys.append(pts[0][1])
                elif x >= pts[-1][0]:
                    ys.append(pts[-1][1])
                else:
                    for i in range(len(pts)-1):
                        x1,y1 = pts[i]; x2,y2 = pts[i+1]
                        if x1 <= x <= x2:
                            t = (x-x1)/(x2-x1)
                            ys.append(y1 + t*(y2-y1))
                            break
                    else:
                        ys.append(None)
        return {"y": ys}
    except Exception:
        return {"y": [None]*len(probe.get("x", []))}
