def predict(probe):
    # Outputs are discrete: 8.8, 9.8 (x<0); -11.4, -12.4 (x>0); 1548.92 at x=0.
    # Negative side: x < -4.105 -> 8.8 ; x >= -4.105 -> 9.8 [E5,E6,E7,E8,E9,E10]
    #   -4.108,-4.106,-4.104,-4.102 -> 8.8 ; -4.1 -> 9.8 [E9]
    #   -4.11 -> 8.8, -4.09 -> 9.8 [E9]; -4.105 -> 8.8 [E8]
    #   -4.101..-4.111 all -> 8.8 [E10]
    # Positive side: x < 4.101 -> -11.4 ; x >= 4.101 -> -12.4 [E9,E10]
    #   4.09 -> -11.4 ; 4.101,4.104,4.107,4.109,4.111 -> -12.4 [E10]
    #   4.11,4.12 -> -12.4 [E8]; 4.1 -> -11.4 [E7]
    # x = 0 -> 1548.92 [E1,E8]
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
            ys.append(8.8 if xv < -4.105 else 9.8)
        else:
            ys.append(-11.4 if xv < 4.101 else -12.4)
    return {"y": ys}
