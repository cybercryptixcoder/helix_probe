def predict(probe):
    # f(x) = floor(x) + 1 for x > 0 [E1, E2, E3, E4, E5]
    # f(x) = floor(x) - 1 for x <= 0 [E1, E2, E3, E4, E5]
    # EXCEPTION: for x in [33.4, 34.0) the output is a small negative number
    #   (roughly -0.3 to -0.7), not the floor rule [E5, E6].
    #   Boundaries: 33.25 still normal (34), 33.4 anomalous; 33.99 anomalous,
    #   34.0 normal (35). So the anomalous interval is approximately [33.4, 34.0).
    #   ? Exact left boundary unknown between 33.25 and 33.4; using 33.4.
    #   ? The anomalous values look noisy/irregular; approximate with a constant.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif 33.4 <= x < 34.0:
            out.append(-0.4)
        elif x > 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
