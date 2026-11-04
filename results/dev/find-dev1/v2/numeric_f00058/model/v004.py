def predict(probe):
    # f is exactly -84.3663 on a flat central region |x| <= ~48 [E1,E2,E3,E4,E5]
    # Positive side: flat through 48, growth begins between 48 and 52 [E4,E5]
    #   f(52)=1853.94, f(56)=6838.99, f(60)=12306.92, f(64)=15971.28 [E4,E1]
    # Negative side: flat through -48, growth begins between -48 and -52 [E5]
    #   f(-52)=1853.94, f(-56)=12306.92, f(-60)=27779.38, f(-64)=44756.72 [E5,E1]
    # Both sides share the same onset ~50 and same shape near onset [E5]
    # Growth is steep; far values: f(128)=258084, f(-128)=326550 [E1]
    # Model growth as c + a*(|x|-T)^p per side, fit to far points.
    import math
    c = -84.3663
    out = []
    for x in probe.get("x", []):
        try:
            if x is None:
                out.append(None); continue
            ax = abs(x)
            if x >= 0:
                T = 50.0
                y64, y128 = 15971.2842, 258083.9783
            else:
                T = 50.0
                y64, y128 = 44756.7193, 326549.8085
            if ax <= T:
                out.append(c)
            else:
                d1 = y64 - c
                d2 = y128 - c
                r = (128.0 - T) / (64.0 - T)
                p = math.log(d2 / d1) / math.log(r)
                a = d1 / ((64.0 - T) ** p)
                out.append(c + a * ((ax - T) ** p))
        except Exception:
            out.append(None)
    return {"y": out}
