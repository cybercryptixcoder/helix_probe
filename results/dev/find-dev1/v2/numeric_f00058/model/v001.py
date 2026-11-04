def predict(probe):
    # f is a constant -84.3663 for |x| <= 32 [E1]
    # f grows sharply for |x| > 32, asymmetric: f(64)=15971, f(-64)=44757 [E1]
    # f(128)=258084, f(-128)=326550 [E1]
    # Looks like a smooth function of |x| active only outside a dead zone.
    # Hypothesis: f(x) = c + a*(|x|-32)^p for |x|>32, else c.
    # Fit with two points per side. Use power law.
    import math
    c = -84.3663
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax <= 32:
                out.append(c)
            else:
                # fit p and a from (64,44757) and (128,326550) on negative side
                # and (64,15971),(128,258084) on positive side
                if x < 0:
                    y64, y128 = 44756.7193, 326549.8085
                else:
                    y64, y128 = 15971.2842, 258083.9783
                # y = c + a*(ax-32)^p ; solve
                d1 = y64 - c
                d2 = y128 - c
                # (96/32)^p = d2/d1 -> 3^p = d2/d1
                p = math.log(d2/d1)/math.log(3.0)
                a = d1/(32.0**p)
                out.append(c + a*((ax-32.0)**p))
        except Exception:
            out.append(None)
    return {"y": out}
