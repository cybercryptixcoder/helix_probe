def predict(probe):
    # Outputs take only two values: -12.4 and 8.8 [E1]
    # Sign pattern: negative x -> 8.8, positive x -> -12.4, with exceptions [E1]
    # x=2.9 -> -11.4 (not -12.4), suggesting a special region near small positive x [E1]
    # Hypothesis: f(x) = 8.8 if x < 0 else -12.4, except a small interval near 0
    #   where value is -11.4. Boundary unknown; guess |x| < ~5 region differs [E1]
    # ? Exact boundaries and the -11.4 region are uncertain.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x < 0:
            out.append(8.8)
        elif -5 <= x <= 5:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}
