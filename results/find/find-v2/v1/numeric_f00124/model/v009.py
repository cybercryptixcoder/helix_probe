def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            if x >= 0:
                y = 106.06 + 111.43 * x
            else:
                ax = -x
                if ax >= 2.0:
                    y = 26.07 * ax - 25.4
                elif ax >= 1.0:
                    # trough from |x|=1 to |x|=2, joining linear law at 2.0
                    # fit quadratic through (1.05,6.37),(1.5,13.6624),(2.0,26.6982)
                    a = 6.37
                    # solve for b,c: y = a + b*t + c*t^2, t = ax-1.05
                    t1 = 1.5 - 1.05
                    t2 = 2.0 - 1.05
                    y1 = 13.6624
                    y2 = 26.6982
                    # b*t1 + c*t1^2 = y1-a ; b*t2 + c*t2^2 = y2-a
                    d1 = y1 - a
                    d2 = y2 - a
                    det = t1 * t2 * t2 - t2 * t1 * t1
                    b = (d1 * t2 * t2 - d2 * t1 * t1) / det
                    c = (d2 * t1 - d1 * t2) / det
                    t = ax - 1.05
                    y = a + b * t + c * t * t
                else:
                    # steep fall from ~106 at 0 to ~6.85 at 1, cubic fit
                    b = -123.67
                    c = 24.46
                    d = 0.0
                    y = 106.06 + b * ax + c * ax * ax + d * ax * ax * ax
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
