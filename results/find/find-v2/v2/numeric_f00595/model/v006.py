def predict(probe):
    # f(x) = floor(x)+1 for x>0, floor(x)-1 for x<=0 [E1-E13]
    # Anomalous interval: (33.3, 41.5] returns small negative values in [-0.7,-0.2] [E16,E18]
    #   E16: 33.3 normal(34), 33.4..41.0 anomalous, 41.5 anomalous(-0.1972)
    #   E18: 33.31..41.48 all anomalous; 41.5 also anomalous per E16
    #   Interior values look hash-like/jumpy, not smooth [E18]
    #   Mechanism unknown; approximate with deterministic pseudo-random in [-0.7,-0.2] "?"
    import math
    out = []
    for x in probe["x"]:
        if 33.3 < x <= 41.5:
            h = math.sin(x * 12.9898) * 43758.5453
            frac = h - math.floor(h)
            out.append(round(-0.7 + 0.5 * frac, 4))
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
