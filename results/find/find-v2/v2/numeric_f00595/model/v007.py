def predict(probe):
    # f(x) = floor(x)+1 for x>0, floor(x)-1 for x<=0 [E1-E17,E19-E21]
    # Anomalous interval: 33.3 < x <= 41.5 returns small negative values in [-0.75,-0.29] [E16,E18,E22]
    #   E22: 33.3 normal(34); 33.3001 anomalous; 41.5 anomalous(-0.7443); 41.5001 anomalous(-0.5312);
    #        41.6,41.75,42.0 anomalous too -> upper bound is NOT 41.5, extends further
    #   E22 shows 41.5001, 41.6, 41.75, 42.0 all anomalous -> upper boundary is higher than 41.5
    #   Interior is hash-like/jumpy, not smooth [E18,E22]
    #   Mechanism unknown; approximate with deterministic pseudo-random in [-0.75,-0.29] "?"
    import math
    out = []
    for x in probe["x"]:
        if 33.3 < x <= 42.0:
            h = math.sin(x * 12.9898) * 43758.5453
            frac = h - math.floor(h)
            out.append(round(-0.75 + 0.46 * frac, 4))
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
