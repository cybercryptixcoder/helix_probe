def predict(probe):
    # Model of the black box f(x).
    #
    # Rules (each cited to evidence):
    # - Negative x, x < -4.0: 8.8 [E2,E4,E6,E7,E9]
    # - Negative x, -4.0 <= x < 0: 9.8 [E2,E4,E6]
    # - x == 0 exactly: 1548.92 (single spike) [E2]
    # - Positive x, 0 < x < ~4.15: -11.4 [E1,E3,E8,E10]
    # - Positive x, x >= ~4.15: -12.4 [E4,E5,E7,E9,E10]
    #   Boundary is between 4.1 (-11.4) and 4.2 (-12.4) [E10]. Guess 4.15 (?).
    #   E8 showed 4.0 -> -11.4, consistent. E4: 4.5 -> -12.4, consistent.
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            if x == 0.0:
                ys.append(1548.92)
            elif x < 0:
                if x >= -4.0:
                    ys.append(9.8)
                else:
                    ys.append(8.8)
            else:  # x > 0
                if x < 4.15:
                    ys.append(-11.4)
                else:
                    ys.append(-12.4)
        return {"y": ys}
    except Exception:
        try:
            n = len(probe.get("x", []))
        except Exception:
            n = 0
        return {"y": [None] * n}
