def predict(probe):
    # f(x) = -84.3663 on |x| <= 48 (flat region) [E2,E3,E4,E5,E6,E7]
    # Growth begins just past |x|=48 on both sides [E4,E6,E7]
    # Negative side anchors: -52->1853.94, -56->12306.92, -60->27779.38, -64->44756.72, -96->185653.26, -128->326549.81 [E1,E4,E7]
    # Positive side anchors: 52->428.05, 56->2090.58, 60->6838.99, 64->15971.28, 96->134517.60, 128->258083.98 [E1,E4,E7]
    # Just past onset: 51.5->12.41, 52->428.05, 52.5->635.86, 53->843.68, 54->1259.31 (pos) [E7]
    # Just past onset: -51.5->547.32, -52->1853.94, -52.5->3160.56, -53->4467.19, -54->7080.43 (neg) [E7]
    # Growth is steep; interpolate between anchors [E1,E4,E7]
    xs = probe.get("x", [])
    ys = []
    neg = [(48,-84.3663),(51.5,547.3193),(52,1853.9413),(52.5,3160.5633),(53,4467.1854),(54,7080.4295),(56,12306.9177),(60,27779.3796),(64,44756.7193),(96,185653.2639),(128,326549.8085)]
    pos = [(48,-84.3663),(51.5,12.4118),(52,428.046),(52.5,635.8631),(53,843.6803),(54,1259.3145),(56,2090.5829),(60,6838.9942),(64,15971.2842),(96,134517.6027),(128,258083.9783)]
    for x in xs:
        try:
            ax = abs(x)
            pts = neg if x < 0 else pos
            if ax <= 48:
                ys.append(-84.3663)
            elif ax >= pts[-1][0]:
                ys.append(pts[-1][1])
            else:
                y = pts[-1][1]
                for i in range(len(pts)-1):
                    x0,y0 = pts[i]; x1,y1 = pts[i+1]
                    if x0 <= ax <= x1:
                        t = (ax-x0)/(x1-x0)
                        y = y0 + (y1-y0)*t
                        break
                ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
