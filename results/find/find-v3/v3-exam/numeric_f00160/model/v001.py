def predict(probe):
    # f(x) = round(x - 39.5) [E1]
    # rounding appears to be round-half-up (26.5->27, -45.5->-45) [E1]
    # ? no evidence yet of a special region; assume uniform rule
    import math
    out = []
    for x in probe["x"]:
        v = x - 39.5
        # round half up
        r = math.floor(v + 0.5)
        out.append(float(r))
    return {"y": out}
