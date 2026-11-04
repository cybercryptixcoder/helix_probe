def predict(probe):
    # Piecewise-constant with a spike at 0.
    # Regions (from evidence):
    #   x <= -4.15 -> 8.8   [E1,E2,E3,E4,E5: -4.15->8.8, -4.1->9.8; boundary in (-4.15,-4.1]]
    #   -4.15 < x < 0 -> 9.8 [E1,E2,E3,E4,E5]
    #   x == 0     -> 1548.92 [E1]
    #   0 < x < 4.35 -> -11.4 [E1,E2,E3,E4,E5: 4.35->-12.4, 4.3->-11.4; boundary in (4.3,4.35]]
    #   x >= 4.35  -> -12.4  [E1,E2,E3,E4,E5]
    # Boundaries uncertain within bracketing intervals; use -4.125 and 4.325 as best guesses.
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                y = 1548.92
            elif x <= -4.125:
                y = 8.8
            elif x < 0:
                y = 9.8
            elif x < 4.325:
                y = -11.4
            else:
                y = -12.4
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
