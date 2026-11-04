def predict(probe):
    # Piecewise-constant with a spike at 0.
    # Regions (from evidence):
    #   x <= -4.1  -> 8.8    [E2: -4.9->8.8; E4: -4.2->8.8, -4.0->9.8; E5: -4.15->8.8, -4.1->9.8; E6: -4.105->8.8, -4.095->9.8]
    #   -4.1 < x < 0 -> 9.8  [E1..E6]
    #   x == 0     -> 1548.92 [E1]
    #   0 < x <= 4.3 -> -11.4 [E4: 4.3->-11.4, 4.5->-12.4; E5: 4.35->-12.4; E6: 4.305->-12.4]
    #   x > 4.3    -> -12.4  [E2..E6]
    # Boundary left in (-4.105,-4.095]; right in (4.3,4.305]. Use -4.1 and 4.3025 as best guesses.
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                y = 1548.92
            elif x <= -4.1:
                y = 8.8
            elif x < 0:
                y = 9.8
            elif x <= 4.3025:
                y = -11.4
            else:
                y = -12.4
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
