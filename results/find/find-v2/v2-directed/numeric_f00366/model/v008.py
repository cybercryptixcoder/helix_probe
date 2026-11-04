def predict(probe):
    # Outputs take discrete values: 8.8, 9.8, -11.4, -12.4, and 1548.92 at x=0.
    # Negative side (x < 0):
    #   x < -4.11 -> 8.8 ; -4.11 <= x < 0 -> 9.8
    #   Boundary between -4.12 (8.8) and -4.11 (9.8) [E7]; -4.115->8.8, -4.105->9.8 [E6]
    #   So threshold ~ -4.11 (x < -4.11 -> 8.8, else 9.8). [E5,E6,E7]
    # Positive side (x > 0):
    #   small positive -> -11.4 ; larger -> -12.4
    #   Boundary between 4.1 (-11.4) and 4.15 (-12.4) [E7]; 4.305->-12.4 [E6]
    #   So threshold ~ 4.125 (x < 4.125 -> -11.4, else -12.4). [E7]
    # x = 0 -> 1548.92 [E1]
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
            ys.append(8.8 if xv < -4.11 else 9.8)
        else:
            ys.append(-11.4 if xv < 4.125 else -12.4)
    return {"y": ys}
