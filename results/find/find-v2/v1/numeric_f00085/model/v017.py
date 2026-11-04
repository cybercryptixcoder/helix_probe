def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        plateau = -22.8021
        # shared quadratic part
        qa2 = 3.0
        qd1 = -2.5
        qc0 = -22.8021
        # negative-side extra quartic term
        na4 = 1.80e-4
        r_slope = (132.1905 - (-22.6269)) / (8.0 - 5.8)
        r_int = -22.6269 - r_slope * 5.8
        l_slope = (-22.8021 - 21.8213) / (-7.25 - (-8.0))
        l_int = 21.8213 - l_slope * (-8.0)
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            if -7.25 <= x <= 5.75:
                ys.append(plateau)
            elif 5.75 < x <= 8.0:
                ys.append(r_slope * x + r_int)
            elif -8.0 <= x < -7.25:
                ys.append(l_slope * x + l_int)
            elif x > 8.0:
                ys.append(qa2 * x * x + qd1 * x + qc0)
            else:
                ys.append(na4 * x**4 + qa2 * x * x + qd1 * x + qc0)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
