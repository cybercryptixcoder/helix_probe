import math

def predict(probe):
    # Beliefs (evidence):
    # - Undefined for x < 0 (all negatives null) [E1-E15]
    # - Defined for x >= 0, monotone increasing, saturating near ~1000 [all]
    # - f(0) = 0 (assumed anchor) [?]
    # - Near x=0 the curve is NOT steep-positive: f(0.9) = -20.3, so f dips
    #   slightly negative just above 0 before rising [E15]
    # - Model: monotone cubic (PCHIP) through sampled points; linear
    #   extrapolation outside [0, 123.6] [all]
    xs = probe.get("x", [])
    data = [
        (0.0, 0.0),
        (0.9, -20.3457),
        (1.2, 38.2108), (2.0, 142.1873), (2.9, 217.8175), (12.1, 508.5818),
        (13.1, 524.7448), (17.3, 581.3497), (21.3, 623.6874), (28.4, 682.2439),
        (30.3, 695.4253), (43.0, 766.677), (47.1, 785.2145), (52.9, 808.8524),
        (56.2, 821.1696), (58.8, 830.375), (65.5, 852.3393), (66.0, 853.8872),
        (72.7, 873.5674), (77.6, 886.8439), (78.1, 888.1512), (79.4, 891.5114),
        (83.2, 901.0269), (88.2, 912.9058), (93.5, 924.7836), (94.1, 926.0856),
        (94.8, 927.5942), (102.1, 942.6939), (103.0, 944.4803), (104.5, 947.4231),
        (104.9, 948.2008), (105.7, 949.7472), (110.8, 959.3387), (119.5, 974.7246),
        (119.7, 975.065), (123.6, 981.5911),
    ]
    n = len(data)
    xk = [d[0] for d in data]
    yk = [d[1] for d in data]
    h = [xk[i+1]-xk[i] for i in range(n-1)]
    delta = [(yk[i+1]-yk[i])/h[i] for i in range(n-1)]
    m = [0.0]*n
    m[0] = delta[0]
    m[n-1] = delta[n-2]
    for i in range(1, n-1):
        if delta[i-1]*delta[i] <= 0:
            m[i] = 0.0
        else:
            w1 = 2*h[i]+h[i-1]
            w2 = h[i]+2*h[i-1]
            m[i] = (w1+w2)/(w1/delta[i-1]+w2/delta[i])

    def interp(x):
        if x <= xk[0]:
            return yk[0] + m[0]*(x-xk[0])
        if x >= xk[-1]:
            return yk[-1] + m[-1]*(x-xk[-1])
        lo, hi = 0, n-1
        while hi-lo > 1:
            mid = (lo+hi)//2
            if xk[mid] <= x:
                lo = mid
            else:
                hi = mid
        i = lo
        t = (x-xk[i])/h[i]
        h00 = 2*t**3-3*t**2+1
        h10 = t**3-2*t**2+t
        h01 = -2*t**3+3*t**2
        h11 = t**3-t**2
        return h00*yk[i]+h10*h[i]*m[i]+h01*yk[i+1]+h11*h[i]*m[i+1]

    out = []
    for x in xs:
        try:
            if x is None or x < 0:
                out.append(None)
            else:
                out.append(interp(float(x)))
        except Exception:
            out.append(None)
    return {"y": out}
