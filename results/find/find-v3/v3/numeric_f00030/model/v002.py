def predict(probe):
    # y is a smooth function of x, roughly -1.62 + tilt, with a sharp dip near x=0 [E1,E2,E3,E4]
    # Far from 0: y rises with x (tilt ~ +0.0009*x) [E2,E3]
    # Near x=0: sharp dip to about -1.81 at |x|~0.5-1, width ~2 [E4]
    # Dip shape: symmetric-ish, deepest around |x|=0.5-1.2, returns to baseline by |x|~2.5 [E4]
    import math
    xs = probe["x"]
    ys = []
    for x in xs:
        # baseline: gentle tilt, higher x -> higher y
        base = -1.62 + 0.0009 * x
        # dip near 0: gaussian well centered at 0 with width ~0.9, depth ~0.19
        dip = -0.19 * math.exp(-(x / 0.9) ** 2)
        ys.append(base + dip)
    return {"y": ys}
