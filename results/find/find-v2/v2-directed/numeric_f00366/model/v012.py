def predict(probe):
    # Negative side: x < -4.1005 -> 8.8 ; x >= -4.1005 -> 9.8 [E13: -4.1005->8.8, -4.0995->9.8]
    # Positive side: x < 4.1005 -> -11.4 ; x >= 4.1005 -> -12.4 [E13: 4.0995->-11.4, 4.1005->-12.4]
    # x = 0 -> 1548.92 [E1,E8,E11]; isolated to exactly 0 [E11]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xv = float(x)
        except Exception:
            ys.append(None)
            continue
        if xv == 0:
            ys.append(1548.92)
        elif xv < 0:
            ys.append(8.8 if xv < -4.1005 else 9.8)
        else:
            ys.append(-11.4 if xv < 4.1005 else -12.4)
    return {"y": ys}
