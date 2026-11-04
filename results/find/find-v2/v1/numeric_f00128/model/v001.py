def predict(probe):
    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            # cubic-dominant fit matching E1: f(x) ≈ a*x^3 + b*x + c
            # Using f(128)≈-2152, f(64)≈-1070, f(0)≈5.4
            # a*128^3 + b*128 + c = -2152
            # a*64^3  + b*64  + c = -1070
            # c = 5.4
            # 2097152a + 128b = -2157.4
            # 262144a  + 64b  = -1075.4
            # Solve: from second, 64b = -1075.4 - 262144a -> b = -16.803 - 4096a
            # 2097152a + 128(-16.803 - 4096a) = -2157.4
            # 2097152a - 2150.8 - 524288a = -2157.4
            # 1572864a = -6.6 -> a = -4.196e-6
            # b = -16.803 - 4096*(-4.196e-6) = -16.803 + 0.01719 = -16.786
            a = -4.196e-6
            b = -16.786
            c = 5.4
            ys.append(a * x**3 + b * x + c)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
