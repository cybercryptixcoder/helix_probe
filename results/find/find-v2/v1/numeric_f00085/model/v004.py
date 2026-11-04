def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        plateau = -22.8021
        a = 3.088
        b = -2.5
        c = -22.8021
        # right ramp: f(6)=-8.5526, f(8)=132.1905 -> slope 17.59305, intercept -114.1109
        r_slope = 17.59305
        r_int = -114.1109
        # left ramp guess: mirror-ish, use f(-8)=21.82 and plateau at -6
        l_slope = (21.8213 - plateau) / (-8.0 - (-6.0))  # ~ -22.31 per unit
        l_int = plateau - l_slope * (-6.0)
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            if -6.0 <= x <= 5.75:
                ys.append(plateau)
            elif 5.75 < x <= 8.0:
                ys.append(r_slope * x + r_int)
            elif -8.0 <= x < -6.0:
                ys.append(l_slope * x + l_int)
            else:
                ys.append(a * x * x + b * x + c)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
