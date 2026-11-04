def predict(probe):
    # f(x) = -84.3663 on |x| <= 36 (flat region) [E1,E2,E3,E4]
    # Growth begins just past |x|=36 on both sides [E4]
    # Negative side: -40->-84.37, -44->-84.37, -48->-84.37, -52->1853.94, -56->12306.92, -60->27779.38, -64->44756.72 [E4]
    # Positive side: 40->-84.37, 44->-84.37, 48->-84.37, 52->428.05, 56->2090.58, 60->6838.99, 64->15971.28 [E4]
    # Growth is steep; interpolate between anchors [E1,E4]
    # Both sides reach ~326550 at |x|=128 [E1]
    xs = probe.get("x", [])
    ys = []
    neg = [(36,-84.3663),(48,-84.3663),(52,1853.9413),(56,12306.9177),(60,27779.3796),(64,44756.7193),(96,185653.2639),(128,326549.8085)]
    pos = [(36,-84.3663),(48,-84.3663),(52,428.046),(56,2090.5829),(60,6838.9942),(64,15971.2842),(96,258083.9783),(128,326549.8085)]
    for x in xs:
        try:
            ax = abs(x)
            pts = neg if x < 0 else pos
            if ax <= 36:
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
