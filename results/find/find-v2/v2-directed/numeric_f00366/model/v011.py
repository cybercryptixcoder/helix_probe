def predict(probe):
    # Negative side: x < -4.105 -> 8.8 ; x >= -4.105 -> 9.8 [E5,E6,E7,E8,E9,E10,E12]
    #   E12: -4.1055..-4.1025 all -> 8.8, so boundary is at or below -4.1025
    #   E9: -4.104,-4.102 -> 8.8 ; -4.1 -> 9.8, so boundary in (-4.102, -4.1]
    #   E10: -4.101..-4.111 all -> 8.8 ; E8: -4.105 -> 8.8, -4.1 -> 9.8
    #   => boundary between -4.102 and -4.1; use -4.101 (matches E10's -4.101 -> 8.8)
    # Positive side: x < 4.101 -> -11.4 ; x >= 4.101 -> -12.4 [E9,E10,E12]
    #   E12: 4.1015..4.105 all -> -12.4 ; E10: 4.101 -> -12.4 ; 4.09 -> -11.4
    #   => boundary between 4.09 and 4.101; use 4.101
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
            ys.append(8.8 if xv < -4.101 else 9.8)
        else:
            ys.append(-11.4 if xv < 4.101 else -12.4)
    return {"y": ys}
