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
                else:
                    # smooth curve through (0,106),(0.1,94.91),(0.5,50.34),(1,6.85),(1.9,24.09),(2,26.70)
                    # quadratic fit: f = 106 - 160*ax + 60*ax^2 (approximate)
                    y = 106.0 - 160.0 * ax + 60.0 * ax * ax
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
