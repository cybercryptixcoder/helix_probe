import math

def predict(probe):
    # Rules (evidence):
    # - Undefined for x < 0 (all negatives null) [E1, E2, E3, E4, E5, E6]
    # - Defined for x >= 0 [all]
    # - Monotone increasing, saturating near ~1000 [all]
    # - Shape: steep near 0, then gradual. Data points:
    #     x=1.2->38.2, 2.0->142.2, 2.9->217.8, 12.1->508.6, 13.1->524.7,
    #     17.3->581.3, 21.3->623.7, 28.4->682.2, 30.3->695.4, 43.0->766.7,
    #     47.1->785.2, 52.9->808.9, 56.2->821.2, 58.8->830.4, 65.5->852.3,
    #     66.0->853.9, 72.7->873.6, 77.6->886.8, 78.1->888.2, 79.4->891.5,
    #     83.2->901.0, 88.2->912.9, 93.5->924.8, 94.1->926.1, 94.8->927.6,
    #     102.1->942.7, 103.0->944.5, 104.5->947.4, 104.9->948.2,
    #     105.7->949.7, 110.8->959.3, 119.5->974.7, 119.7->975.1,
    #     123.6->981.6
    # - The curve looks like y = A*(1 - exp(-(x/tau)^p)) but the fit is off
    #   in the mid-range. Let's fit a more flexible form.
    # - Try y = A * (1 - exp(-x/tau))^p? Or y = A*tanh((x/tau)^p)?
    # - Actually the data looks very smooth; let's do a proper nonlinear fit
    #   over all points with a stretched exponential, refining A, tau, p.

    xs = probe.get("x", [])
    out = []

    data = [
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

    def model(A, tau, p, x):
        return A * (1.0 - math.exp(-((x / tau) ** p)))

    def sse_of(A, tau, p):
        s = 0.0
        for x, y in data:
            s += (model(A, tau, p, x) - y) ** 2
        return s

    # Coarse grid search then local refine
    best = (float('inf'), 1000.0, 10.0, 1.0)
    for A in [990, 995, 1000, 1005, 1010, 1015, 1020, 1030, 1050]:
        for tau in [5, 8, 10, 12, 15, 18, 20, 25, 30]:
            for p in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6]:
                s = sse_of(A, tau, p)
                if s < best[0]:
                    best = (s, A, tau, p)

    _, A, tau, p = best

    # Local coordinate descent refine
    step = {'A': 5.0, 'tau': 2.0, 'p': 0.1}
    for _ in range(200):
        improved = False
        for key in ('A', 'tau', 'p'):
            for sign in (1, -1):
                nA, ntau, np_ = A, tau, p
                if key == 'A':
                    nA = A + sign * step['A']
                elif key == 'tau':
                    ntau = tau + sign * step['tau']
                else:
                    np_ = p + sign * step['p']
                if nA <= 0 or ntau <= 0 or np_ <= 0:
                    continue
                s = sse_of(nA, ntau, np_)
                if s < best[0]:
                    best = (s, nA, ntau, np_)
                    A, tau, p = nA, ntau, np_
                    improved = True
        if not improved:
            step['A'] *= 0.5
            step['tau'] *= 0.5
            step['p'] *= 0.5
            if step['A'] < 1e-4:
                break

    for x in xs:
        try:
            if x is None or x < 0:
                out.append(None)
            else:
                out.append(model(A, tau, p, x))
        except Exception:
            out.append(None)
    return {"y": out}
