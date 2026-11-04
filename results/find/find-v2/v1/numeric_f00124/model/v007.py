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
                    # points: (1.0,6.85),(1.05,6.37),(1.1,6.44),(1.2,7.47),(1.4,11.24),(1.6,16.27),(1.8,21.48),(2.0,26.70)
                    t = ax - 1.05
                    y = 6.37 + 1.0 * t + 11.5 * t * t
                else:
                    # steep fall from ~106 at 0 to ~6.85 at 1
                    # points: (0,106),(0.02,103.82),(0.1,94.91),(0.3,72.62),(0.5,50.34),(0.62,36.97),(0.9,10.63),(1.0,6.85)
                    # quadratic in ax: y = 106.06 + b*ax + c*ax^2
                    # fit through (0,106.06),(0.5,50.34),(1.0,6.85):
                    # 106.06 + 0.5b + 0.25c = 50.34 -> 0.5b + 0.25c = -55.72
                    # 106.06 + b + c = 6.85 -> b + c = -99.21
                    # from first: 2b + c = -222.88; subtract: b = -123.67; c = 24.46
                    y = 106.06 - 123.67 * ax + 24.46 * ax * ax
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
