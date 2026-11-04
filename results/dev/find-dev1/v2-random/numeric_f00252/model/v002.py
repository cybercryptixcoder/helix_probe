import math

def predict(probe):
    # Rules (evidence):
    # - Undefined for x < 0 (all negatives null) [E1, E2]
    # - Defined for x >= 0 [E1, E2]
    # - Output rises with x, saturating near ~1000 as x grows [E1, E2]
    # - Shape looks like a saturating curve, not quadratic: 
    #     x=1.2 -> 38.2, x=2.9 -> 217.8, x=21.3 -> 623.7, x=30.3 -> 695.4
    #     x=65.5 -> 852.3, x=66 -> 853.9, x=72.7 -> 873.6, x=79.4 -> 891.5
    #     x=88.2 -> 912.9, x=103 -> 944.5, x=104.5 -> 947.4, x=104.9 -> 948.2
    #     x=123.6 -> 981.6
    # - Looks like y = A * (1 - exp(-x/tau)) or similar saturating form.
    #   Try y = A * x / (x + k)  (Michaelis-Menten) or A*(1-exp(-x/tau)).
    #   Check: at x=1.2, y=38.2; x=2.9, y=217.8 -> steep rise near 0.
    #   Ratio y/x: 1.2->31.8, 2.9->75.1, 21.3->29.3, 65.5->13.0, 123.6->7.94
    #   Not Michaelis-Menten (that would have y/x decreasing monotonically from start).
    #   The rise from 1.2 to 2.9 is very steep, then flattens. Suggests something
    #   like y = A*(1 - exp(-x/tau)) with small tau? At x=1.2: 38.2/A; x=2.9: 217.8/A.
    #   If A~1000: 1-exp(-1.2/tau)=0.0382 -> tau~31; 1-exp(-2.9/tau)=0.2178 -> tau~12.
    #   Inconsistent. Try y = A*(1 - exp(-(x/tau)^p)) (Weibull/ stretched exp).
    #   Alternatively maybe y = A * erf-like or sigmoid.
    #   Let's fit y = A*(1 - exp(-(x/tau)^p)) numerically.
    # - Also check: maybe y = A * (1 - exp(-x/tau))^p or logistic.
    #   Let's just fit a flexible saturating form.

    xs = probe.get("x", [])
    out = []

    # Data from E1, E2
    data = [
        (1.2, 38.2108), (2.9, 217.8175), (21.3, 623.6874), (30.3, 695.4253),
        (65.5, 852.3393), (66.0, 853.8872), (72.7, 873.5674), (79.4, 891.5114),
        (88.2, 912.9058), (103.0, 944.4803), (104.5, 947.4231), (104.9, 948.2008),
        (123.6, 981.5911),
    ]

    # Fit y = A * (1 - exp(-(x/tau)^p)) via grid + refine on p, tau, A
    # Use log-space least squares on 1 - y/A = exp(-(x/tau)^p)
    # => -ln(1 - y/A) = (x/tau)^p
    # => ln(-ln(1-y/A)) = p*ln(x) - p*ln(tau)
    # Linear in (p, p*ln(tau)) given A.
    best = None
    for A in [990, 995, 1000, 1005, 1010, 1020, 1050, 1100]:
        pts = []
        ok = True
        for x, y in data:
            r = 1.0 - y/A
            if r <= 0 or r >= 1:
                ok = False
                break
            pts.append((math.log(x), math.log(-math.log(r))))
        if not ok:
            continue
        n = len(pts)
        sx = sum(p[0] for p in pts)
        sy = sum(p[1] for p in pts)
        sxx = sum(p[0]*p[0] for p in pts)
        sxy = sum(p[0]*p[1] for p in pts)
        denom = n*sxx - sx*sx
        if abs(denom) < 1e-12:
            continue
        p = (n*sxy - sx*sy)/denom
        b = (sy - p*sx)/n  # = -p*ln(tau)
        tau = math.exp(-b/p) if p != 0 else 1.0
        # compute SSE
        sse = 0.0
        for x, y in data:
            pred = A*(1 - math.exp(-((x/tau)**p)))
            sse += (pred - y)**2
        if best is None or sse < best[0]:
            best = (sse, A, tau, p)

    if best is None:
        # fallback
        A, tau, p = 1000.0, 10.0, 1.0
    else:
        _, A, tau, p = best

    for x in xs:
        try:
            if x is None:
                out.append(None)
            elif x < 0:
                out.append(None)
            else:
                val = A*(1 - math.exp(-((x/tau)**p)))
                out.append(val)
        except Exception:
            out.append(None)
    return {"y": out}
