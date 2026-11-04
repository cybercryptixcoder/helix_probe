import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            if x <= -20.0:
                # linear from -20 (0.0162) to -128 (0.0479)
                t = (x - (-20.0)) / (-128.0 - (-20.0))
                v = 0.0162 + (0.0479 - 0.0162) * t
                ys.append(v)
            elif x <= -18.0:
                # -20 -> 0.0162, -18 -> 0.0156
                t = (x - (-20.0)) / (-18.0 - (-20.0))
                v = 0.0162 + (0.0156 - 0.0162) * t
                ys.append(v)
            elif x <= -14.0:
                # -18 -> 0.0156 down to -14 -> 0.0142 (near linear)
                t = (x - (-18.0)) / (-14.0 - (-18.0))
                v = 0.0156 + (0.0142 - 0.0156) * t
                ys.append(v)
            elif x <= -6.0:
                # near-linear rise from 0.0142 at -14 to 0.0471 at -6
                t = (x - (-14.0)) / (-6.0 - (-14.0))
                v = 0.0142 + (0.0471 - 0.0142) * t
                ys.append(v)
            elif x <= -2.0:
                # rise from 0.0471 at -6 to 0.0784 at -2, smoothstep
                t = (x - (-6.0)) / (-2.0 - (-6.0))
                s = t * t * (3 - 2 * t)
                v = 0.0471 + (0.0784 - 0.0471) * s
                ys.append(v)
            elif x <= -1.0:
                # plateau region, very slightly decreasing toward -1
                t = (x + 2.0) / 1.0
                v = 0.0784 + (0.0776 - 0.0784) * t
                ys.append(v)
            elif x <= 1.0:
                # smooth cosine transition from 0.0776 at -1 through ~0 at 0 to -0.0951 at 1
                t = (x + 1.0) / 2.0
                v = 0.0776 + (-0.0951 - 0.0776) * (0.5 - 0.5 * math.cos(math.pi * t))
                ys.append(v)
            else:
                # right side: piecewise-linear interpolation through known points
                pts = [
                    (1.0, -0.0951), (1.5, -0.0782), (2.0, -0.0595), (2.5, -0.0507),
                    (3.0, -0.0466), (3.5, -0.0452), (4.0, -0.0438), (4.5, -0.0423),
                    (5.0, -0.0405), (6.0, -0.0371), (7.0, -0.0336), (8.0, -0.03),
                    (9.0, -0.027), (10.0, -0.0249), (12.0, -0.0208), (14.0, -0.0167),
                    (16.0, -0.0126), (18.0, -0.0084), (20.0, -0.0043), (24.0, 0.0003),
                    (28.0, 0.0025), (40.0, 0.0089), (48.0, 0.0133), (56.0, 0.0176),
                    (80.0, 0.0307), (96.0, 0.0394), (112.0, 0.048), (128.0, 0.0565),
                ]
                if x >= 128.0:
                    # extrapolate with last slope
                    v = 0.0565 + (x - 128.0) * 0.00045
                else:
                    v = None
                    for i in range(len(pts) - 1):
                        x0, y0 = pts[i]
                        x1, y1 = pts[i + 1]
                        if x0 <= x <= x1:
                            t = (x - x0) / (x1 - x0)
                            v = y0 + (y1 - y0) * t
                            break
                    if v is None:
                        v = pts[-1][1]
                ys.append(v)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
