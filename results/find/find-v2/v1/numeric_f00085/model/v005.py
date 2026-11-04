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
        # left ramp: through f(-8)=21.8213 and f(-7.5)=-12.9955 -> slope -69.6336
        l_slope = (-12.9955 - 21.8213) / (-7.5 - (-8.0))  # ~ -69.6336
        l_int = 21.8213 - l_slope * (-8.0)
        # left ramp meets plateau where l_slope*x + l_int = plateau
        left_edge = (plateau - l_int) / l_slope  # ~ -7.19
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            if left_edge <= x <= 5.75:
                ys.append(plateau)
            elif 5.75 < x <= 8.0:
                ys.append(r_slope * x + r_int)
            elif -8.0 <= x < left_edge:
                ys.append(l_slope * x + l_int)
            else:
                ys.append(a * x * x + b * x + c)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
