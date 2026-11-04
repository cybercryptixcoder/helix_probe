def predict(probe):
    # Model of the black box f(x).
    #
    # Observations and inferred rules:
    # - Negative x: 8.8 for x < -4.0; 9.8 for -4.0 <= x < 0 [E2,E4,E6]
    # - x = 0 exactly: 1548.92 (single spike) [E2]
    # - Positive x: -11.4 for small x, -12.4 for large x [E1,E3,E4,E5,E7]
    # - Positive boundary: E8 shows 1.2..4.0 ALL -> -11.4, so boundary is
    #   above 4.0. E1 had 2.9 -> -11.4 (consistent). E4: 4.5 -> -12.4.
    #   So boundary is between 4.0 and 4.5. Guess 4.5? [E4: 4.5 -> -12.4]
    #   Actually E4 shows 4.5 -> -12.4, so boundary <= 4.5. E8 shows 4.0 -> -11.4.
    #   Boundary in (4.0, 4.5]. Guess 4.5 (inclusive -> -12.4).
    # - Recheck E1: 2.9 -> -11.4 (yes, <4.5). 21.3 -> -12.4 (yes). Good.
    # - E3: 1.2 -> -11.4 (yes). Good.
    # - E5: 28.4 -> -12.4 (yes). Good.
    # - E7: 12.5 -> -12.4 (yes). Good.
    #
    # Model:
    #   if x == 0: 1548.92
    #   elif x < 0: 9.8 if x >= -4.0 else 8.8
    #   else (x > 0): -11.4 if x < 4.5 else -12.4

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
                if x < 4.5:
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
