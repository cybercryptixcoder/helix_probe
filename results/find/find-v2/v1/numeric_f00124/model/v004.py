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
                    # quadratic fit through (0,106),(1,6.85),(2,26.7)
                    y = 106.0 - 158.65 * ax + 59.5 * ax * ax
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
