def predict(probe):
    # Observations [E1]:
    #  x<=-5: y=8.8 ; -2<=x<=-0.5: y=9.8 ; x=0: y=1548.92 (huge spike)
    #  0.5<=x<=2: y=-11.4 ; x>=5: y=-12.4
    # The pattern looks like a step function with a narrow special region near 0.
    # Hypothesis: piecewise-constant with a spike at x=0.
    # Boundaries guessed from data: -5, -2, -0.5, 0, 2, 5.
    # The exact boundary behavior (open/closed) is uncertain [?].
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                y = 1548.92
            elif x < -5:
                y = 8.8
            elif x < -0.5:
                y = 9.8
            elif x < 0:
                y = 9.8
            elif x < 2:
                y = -11.4
            else:
                y = -12.4
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
