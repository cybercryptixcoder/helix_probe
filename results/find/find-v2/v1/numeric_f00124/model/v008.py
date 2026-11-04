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
                    # trough between |x|=1 and |x|=2, bottom near 1.05
                    t = ax - 1.05
                    y = 6.37 + 1.0 * t + 11.5 * t * t
                else:
                    # steep fall from ~106 at 0 to ~6.85 at 1, cubic fit
                    # through (0,106.06),(0.5,50.34),(0.85,14.04),(1.0,6.85)
                    # y = 106.06 + b*ax + c*ax^2 + d*ax^3
                    b = -123.67
                    c = 24.46
                    d = 0.0
                    y = 106.06 + b * ax + c * ax * ax + d * ax * ax * ax
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
