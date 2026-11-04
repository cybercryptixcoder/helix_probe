def predict(probe):
    # Far-left linear branch: y = -25.45 - 26.0717*x for x <= -1.5 [E1,E2,E3,E6]
    # Right linear branch: y = 106.0528 + 111.427*x for x >= -0.45 [E3,E4,E5,E6]
    # Between -1.5 and -0.45: smooth valley (MLP transition), min near x=-1.08 [E6,E7]
    # Valley is smooth, not piecewise linear; dense E7 points pin the shape [E7]
    # Valley points (x,y) from E6+E7, sorted:
    curve = [
        (-1.5, 13.6624), (-1.48, 13.141), (-1.45, 12.3588), (-1.42, 11.6851),
        (-1.4, 11.2441), (-1.38, 10.803), (-1.35, 10.1415), (-1.32, 9.4799),
        (-1.3, 9.0565), (-1.28, 8.6817), (-1.25, 8.2083), (-1.22, 7.7579),
        (-1.2, 7.4701), (-1.18, 7.2043), (-1.15, 6.8547), (-1.12, 6.5611),
        (-1.1, 6.436), (-1.08, 6.3684), (-1.05, 6.4189), (-1.02, 6.5888),
        (-1.0, 6.8494), (-0.98, 7.2943), (-0.95, 8.2994), (-0.92, 9.5811),
        (-0.9, 10.6298), (-0.88, 11.8704), (-0.85, 14.0401), (-0.82, 16.4569),
        (-0.8, 18.223), (-0.7, 28.0616), (-0.6, 39.1961), (-0.55, 44.7675),
        (-0.45, 55.9102),
    ]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x <= -1.5:
                y = -25.45 - 26.0717 * x
            elif x >= -0.45:
                y = 106.0528 + 111.427 * x
            else:
                y = None
                for i in range(len(curve) - 1):
                    x0, y0 = curve[i]
                    x1, y1 = curve[i + 1]
                    if x0 <= x <= x1:
                        t = (x - x0) / (x1 - x0)
                        y = y0 + t * (y1 - y0)
                        break
                if y is None:
                    y = 106.0528 + 111.427 * x
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
