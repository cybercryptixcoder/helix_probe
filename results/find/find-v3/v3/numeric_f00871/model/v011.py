def predict(probe):
    # f(x) = 5.2 - 2.5*x for x in [-2.1, 2.1] [E4, E6, E8]
    # Elsewhere: 0 [E2, E5, E7, E11, E13]
    # Second active region: noisy band spanning roughly [-80.5, -78.0],
    #   values ~0 to 0.3, no clear trend, mean ~0.13 [E10, E12, E14, E15, E16]
    #   E16 shows nonzero readings from -80.5 through -78.0, then clean 0 at -77.8.
    #   E14 shows nonzero at -79.9..-79.35 and -78.62..-78.2.
    #   E15: -79.5 nonzero, -80.2 nonzero.
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -80.5 <= x <= -78.0:
            # ? noisy band; predict mean ~0.13
            out.append(0.13)
        else:
            out.append(0.0)
    return {"y": out}
