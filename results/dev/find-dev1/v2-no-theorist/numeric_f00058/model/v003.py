def predict(probe):
    # f(x) = -84.3663 on |x| <= 32 (flat region) [E1, E2, E3]
    # E3 shows flat extends through ±32 on both sides; growth starts beyond 32
    # Growth is roughly cubic-ish, positive on both sides [E1]
    # Negative side anchors: -64->44756.7, -96->185653.3, -128->326549.8 [E1]
    # Positive side anchors: 64->134517.6, 96->258084.0, 128->326549.8 [E1]
    # Both sides reach ~326550 at |x|=128; asymmetric in between [E1]
    # Boundary between flat and growth is somewhere in (32, 64] [E3, E1]
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax <= 32:
                ys.append(-84.3663)
            else:
                if x < 0:
                    # anchors: (32,-84.37),(64,44756.72),(96,185653.26),(128,326549.81)
                    pts = [(32, -84.3663), (64, 44756.7193), (96, 185653.2639), (128, 326549.8085)]
                else:
                    # anchors: (32,-84.37),(64,134517.60),(96,258083.98),(128,326549.81)
                    pts = [(32, -84.3663), (64, 134517.6027), (96, 258083.9783), (128, 326549.8085)]
                if ax >= pts[-1][0]:
                    y = pts[-1][1]
                else:
                    y = pts[-1][1]
                    for i in range(len(pts) - 1):
                        x0, y0 = pts[i]
                        x1, y1 = pts[i + 1]
                        if x0 <= ax <= x1:
                            t = (ax - x0) / (x1 - x0)
                            y = y0 + (y1 - y0) * t
                            break
                ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
