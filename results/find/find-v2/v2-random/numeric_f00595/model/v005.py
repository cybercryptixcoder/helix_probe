def predict(probe):
    # Base rule: y = floor(x) + sign(x) [E1-E7, E9, E11]
    #   x > 0: y = floor(x) + 1
    #   x < 0: y = floor(x) - 1
    #   x = 0: y = 0 (?)
    # Exception interval: for x in (33, 42) the output is a small negative
    #   fractional value instead of the base rule.
    #   [E8: 40.1 -> -0.4153, E10: 41.0 -> -0.3385, E12: 34.6 -> -0.431]
    #   Outside this interval base rule holds (e.g. 28.9->29, 43.0->44,
    #   46.2->47, 50.6->51).
    #   The values look like -1/(x - c) for some c: at x=40.1, -0.4153
    #   => x-c ~ 2.408 => c ~ 37.69; at x=41.0, -0.3385 => x-c ~ 2.954
    #   => c ~ 38.05; at x=34.6, -0.431 => x-c ~ 2.320 => c ~ 32.28.
    #   Not a simple pole. Try -1/(x - 33 + something)? Let's fit a smooth
    #   curve. Values: (34.6,-0.431),(40.1,-0.4153),(41.0,-0.3385).
    #   These are all near -0.4. Perhaps the interval is where floor(x)+sign
    #   would be replaced by a small negative constant-ish value.
    #   Best guess: a smooth function like -1/(x-33) fails (at 34.6 gives
    #   -0.625). Try -(x-33)/... no. Let's just interpolate: use a
    #   quadratic through the three points as a rough guess (?).
    import math
    out = []
    for x in probe["x"]:
        try:
            s = 1 if x > 0 else (-1 if x < 0 else 0)
            base = float(math.floor(x) + s)
            # ? special interval roughly (33, 42)
            if 33.0 < x < 42.0:
                # ? quadratic fit through (34.6,-0.431),(40.1,-0.4153),(41.0,-0.3385)
                base = (-0.431 * (x-40.1)*(x-41.0)/((34.6-40.1)*(34.6-41.0))
                        + -0.4153 * (x-34.6)*(x-41.0)/((40.1-34.6)*(40.1-41.0))
                        + -0.3385 * (x-34.6)*(x-40.1)/((41.0-34.6)*(41.0-40.1)))
            out.append(base)
        except Exception:
            out.append(None)
    return {"y": out}
