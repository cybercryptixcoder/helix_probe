def predict(probe):
    # Model of the black box f(x).
    #
    # Rules (each cited to evidence):
    # - x < -4.1: 8.8 [E2,E4,E6,E7,E9,E12,E14,E15,E17]
    # - -4.1 <= x < 0: 9.8 [E2,E4,E6,E12,E14,E16]
    #   Boundary between -4.12 (8.8) and -4.1 (9.8) [E18]. Use -4.1.
    # - x == 0 exactly: 1548.92 (single spike) [E2,E16]
    # - 0 < x < 4.12: -11.4 [E1,E3,E8,E10,E11,E14,E16,E18]
    # - x >= 4.12: -12.4 [E4,E5,E7,E9,E10,E11,E14,E15,E17,E18]
    #   Boundary between 4.1 (-11.4) and 4.12 (-12.4) [E18]. Use 4.12.
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
                if x >= -4.1:
                    ys.append(9.8)
                else:
                    ys.append(8.8)
            else:  # x > 0
                if x < 4.12:
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
