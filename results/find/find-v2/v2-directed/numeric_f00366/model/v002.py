def predict(probe):
    # Piecewise-constant step function with a spike at x=0.
    # Regions (from evidence E1, E2):
    #   x <= -5:      8.8   [E1: -10,-5 -> 8.8; E2: -5.5,-5.1,-4.9 -> 8.8]
    #   -5 < x < 0:   9.8   [E1: -2,-1,-0.5 -> 9.8; E2: -2.1,-1.9,-0.6,-0.4,-0.1,-0.01 -> 9.8]
    #   x == 0:       1548.92 [E1]
    #   0 < x < 5:    -11.4 [E1: 0.5,1,2 -> -11.4; E2: 0.01,0.1,0.4,0.6,1.9,2.1,4.9 -> -11.4]
    #   x >= 5:       -12.4 [E1: 5,10,20,50,100 -> -12.4; E2: 5.1 -> -12.4]
    # Boundary at -5: -5 gives 8.8, so x<=-5 is 8.8 [?].
    # Boundary at 5: 4.9 -> -11.4, 5 -> -12.4, so x>=5 is -12.4 [?].
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                y = 1548.92
            elif x <= -5:
                y = 8.8
            elif x < 0:
                y = 9.8
            elif x < 5:
                y = -11.4
            else:
                y = -12.4
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
