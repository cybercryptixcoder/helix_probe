def predict(probe):
    # f is exactly -84.3663 on a wide central interval [E1, E2, E3]
    # E3 shows flat up to at least |x|=40 on both sides [E3]
    # E1 shows growth by |x|=64; transition lies between 40 and 64 [E1, E3]
    # Growth is asymmetric: f(64)=15971, f(-64)=44757 [E1]
    # f(128)=258084, f(-128)=326550 [E1]
    # Hypothesis: flat for |x|<=T, then smooth growth; T somewhere in (40,64) ?
    import math
    c = -84.3663
    T = 48.0  # ? transition midpoint guess between 40 and 64
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax <= T:
                out.append(c)
            else:
                if x < 0:
                    y64, y128 = 44756.7193, 326549.8085
                else:
                    y64, y128 = 15971.2842, 258083.9783
                d1 = y64 - c
                d2 = y128 - c
                # y = c + a*(ax-T)^p, fit from (64,128)
                r = (128.0 - T) / (64.0 - T)
                p = math.log(d2 / d1) / math.log(r)
                a = d1 / ((64.0 - T) ** p)
                out.append(c + a * ((ax - T) ** p))
        except Exception:
            out.append(None)
    return {"y": out}
