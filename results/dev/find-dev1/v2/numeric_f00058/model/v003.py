def predict(probe):
    # f is exactly -84.3663 on a flat central region |x| <= ~40 [E1,E2,E3,E4]
    # Growth begins just past 40 on both sides; onset differs by sign [E4]
    #   positive side: f(40.5)=1853.9 already large -> onset ~40.2 [E4]
    #   negative side: f(-40.5)=-84.37 flat, f(-41)=-84.37, f(-42)=-84.37,
    #                  f(-44)=-84.37, f(-46)=-84.37, f(-48)=-84.37 [E4]
    #   so negative onset is beyond 48; f(-52)=428.0, f(-56)=2090.6 [E4]
    # Growth is steep and asymmetric: f(64)=15971, f(-64)=44757 [E1]
    # f(128)=258084, f(-128)=326550 [E1]
    # Model growth as power law c + a*(|x|-T)^p per side, fit to two far points.
    import math
    c = -84.3663
    out = []
    for x in probe.get("x", []):
        try:
            if x is None:
                out.append(None); continue
            ax = abs(x)
            if x >= 0:
                T = 40.2
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
