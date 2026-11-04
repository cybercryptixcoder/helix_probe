def predict(probe):
    # f(x) = floor(x) + 1 for x > 0 [E1, E2, E3, E4, E5]
    # f(x) = floor(x) - 1 for x <= 0 [E1, E2, E3, E4, E5]
    # EXCEPTION: at x = 33.5 the output is -0.4681, not 34 [E5]
    #   This suggests a special interval near x=33.5 where behavior differs.
    #   Only one data point so far; treat as a narrow anomaly region around 33.5.
    #   ? Unknown boundaries; guess a small interval [33, 34) or exactly 33.5.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x == 33.5:
            out.append(-0.4681)
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
