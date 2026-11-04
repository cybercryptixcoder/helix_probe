def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x < -2.0:
            y = -2.5588 + (-0.57) * (x + 2.0)
        elif x <= 0.0:
            a = -8.8302
            b = -3.7714
            c = -0.31785
            y = a + b * x + c * x * x
        elif x <= 5.0:
            y = -8.8302 + (-3.317) * x
        else:
            knots = [
                (5.0, -25.4152),
                (5.5, -26.9386),
                (12.0, -38.0921),
                (15.0, -40.6313),
                (20.0, -44.7483),
                (30.0, -49.7259),
                (40.0, -53.5169),
                (50.0, -57.0789),
                (60.0, -58.8789),
                (75.0, -61.5789),
                (90.0, -64.279),
                (100.0, -66.079),
                (110.0, -67.8791),
                (120.0, -69.6791),
                (128.0, -71.1191),
            ]
            if x <= 5.5:
                y = -25.4152 + (-3.05) * (x - 5.0)
            elif x >= 128.0:
                y = -71.1191 + (-0.14) * (x - 128.0)
            else:
                y = None
                for i in range(len(knots) - 1):
                    x0, y0 = knots[i]
                    x1, y1 = knots[i + 1]
                    if x0 <= x <= x1:
                        y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
                        break
                if y is None:
                    y = -71.1191 + (-0.14) * (x - 128.0)
        out.append(y)
    return {"y": out}
