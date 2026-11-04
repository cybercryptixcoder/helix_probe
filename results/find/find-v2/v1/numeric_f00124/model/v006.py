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
                    # points: (1.0,6.85),(1.1,6.44),(1.2,7.47),(1.4,11.24),(1.6,16.27),(1.8,21.48),(1.9,24.09),(2.0,26.70)
                    # fit quadratic through these
                    t = ax - 1.0
                    y = 6.85 - 4.1 * t + 12.0 * t * t
                else:
                    # steep rise from ~106 at 0 to ~6.85 at 1
                    # points: (0,106),(0.02,103.82),(0.1,94.91),(0.3,72.62),(0.5,50.34),(0.8,18.22),(1.0,6.85)
                    y = 106.06 - 99.21 * ax
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
