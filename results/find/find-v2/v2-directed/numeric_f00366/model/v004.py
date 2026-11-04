def predict(probe):
    # Piecewise-constant with a spike at 0.
    # Regions (from evidence):
    #   x <= -4.1  -> 8.8   [E1,E2,E3,E4: -4.2->8.8, -4.0->9.8; boundary in (-4.2,-4.0]]
    #   -4.1 < x < 0 -> 9.8  [E1,E2,E3,E4]
    #   x == 0     -> 1548.92 [E1]
    #   0 < x < 4.4 -> -11.4 [E1,E2,E3,E4: 4.3->-11.4, 4.5->-12.4; boundary in (4.3,4.5]]
    #   x >= 4.4   -> -12.4  [E1,E2,E3,E4]
    # Boundaries uncertain within the bracketing intervals; use -4.1 and 4.4 as best guesses.
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                y = 1548.92
            elif x <= -4.1:
                y = 8.8
            elif x < 0:
                y = 9.8
            elif x < 4.4:
                y = -11.4
            else:
                y = -12.4
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
