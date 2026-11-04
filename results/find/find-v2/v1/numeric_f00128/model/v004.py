def predict(probe):
    try:
        xs = probe["x"]
        ys = []
        c = 5.42
        for x in xs:
            if x >= 0:
                # positive side: slope ~ -16.8, softened near zero
                # g(0.25)~-1.0, g(0.5)~-3.3, g(1)~-10.7, g(2)~-28
                b = -16.8
                ax = abs(x)
                g = b * x * ax / (ax + 0.6)
            else:
                # negative side: slope ~ -6.8, softened near zero
                # f(-0.05)~5.56 => g~0.14; f(-0.5)~6.84 => g~1.42; f(-1)~9.35 => g~3.93
                # f(-2)~15.9 => g~10.5; f(-4)~29.4 => g~24; f(-8)~56.5 => g~51
                b = -6.8
                ax = abs(x)
                g = b * x * ax / (ax + 0.6)
            ys.append(g + c)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
