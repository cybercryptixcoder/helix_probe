def predict(probe):
    # f is a smooth decreasing sigmoid-like curve, saturating at both ends.
    # Left tail: linear slope ~-0.53 for x < ~-20 [E1,E4,E18,E19,E20,E21]
    # Right tail: linear slope ~-0.20 for x > ~45 [E2,E3,E4,E8,E9,E10]
    # Middle: steep transition around x~5-15 [E4,E6,E7,E9,E12,E15,E17,E21]
    # Left line L(x)=8.1-0.53x fits left tail well [E4 -124.4->74.2, E15 -117.9->70.7]
    # Right line R(x)=-46.3-0.2x fits right tail [E10 127->-70.9, E2 123.6->-70.3]
    # Transition is asymmetric: slower approach on right.
    # E23: x=7.3 obs -32.42 vs pred -29.34 (pred too high) -> need steeper drop near x~7
    # E23: x=55.6 obs -58.09 vs pred -57.42 (pred too high) -> R line slightly low
    # E21: x=7.1 obs -31.8, x=15.7 obs -41.2 -> steep then flattening
    # Refit: use m=3.0, w_left=3.5, w_right=6.5 to steepen near x=7 and flatten by x=15
    import math
    def f(x):
        L = 8.1 - 0.53*x
        R = -46.8 - 0.2*x
        if x < 3.0:
            s = 1.0/(1.0+math.exp(-(x-3.0)/3.5))
        else:
            s = 1.0/(1.0+math.exp(-(x-3.0)/6.5))
        return L*(1.0-s) + R*s
    out = []
    for x in probe.get("x", []):
        try:
            out.append(f(float(x)))
        except Exception:
            out.append(None)
    return {"y": out}
