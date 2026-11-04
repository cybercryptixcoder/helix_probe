def predict(probe):
    # Base rule: y = floor(x) + sign(x) [E1-E7, E9]
    #   x > 0: y = floor(x) + 1
    #   x < 0: y = floor(x) - 1
    #   x = 0: y = 0 (?)
    # Exception interval: for x in (40, 42) the output is a small negative
    #   fractional value instead of the base rule. [E8: 40.1 -> -0.4153,
    #   E10: 41.0 -> -0.3385]. Both values are negative and near -0.4/-0.34,
    #   consistent with something like -1/(x-40+something) or a smooth curve.
    #   Boundaries unknown (?). Outside this interval base rule holds
    #   (e.g. 28.9->29, 43.0->44 in E4, 47.1->48 in E3).
    import math
    out = []
    for x in probe["x"]:
        try:
            s = 1 if x > 0 else (-1 if x < 0 else 0)
            base = float(math.floor(x) + s)
            # ? special interval around x in (40, 42)
            if 40.0 < x < 42.0:
                base = -1.0 / (x - 40.0 + 1.0) - 0.0  # ? rough guess
            out.append(base)
        except Exception:
            out.append(None)
    return {"y": out}
