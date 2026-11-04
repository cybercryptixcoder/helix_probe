def predict(probe):
    # Central linear region: f(x) = 5.2 - 2.5*x on [-2.1, 2.1], else 0 [E4, E6, E8]
    # Noisy band: nonzero random-looking values for x in [-88, -78] [E10,E12,E14,E16,E18]
    #   E18: nonzero at -88.0 and -78.0 (both edges inclusive)
    #   E14: nonzero at -88.2 (0.1083), zero at -88.5 -> left edge ~ -88.2
    #   E12: nonzero at -78.5 (0.0971), zero at -77.5 -> right edge ~ -78.0..-78.5
    #   E14: nonzero at -77.8 (0.193)! so right edge extends to at least -77.8
    #   E10: zero at -78.0? no, -78.0 gave 0.2709 (nonzero). zero at -75.
    #   So band roughly [-88.2, -77.8]; values random in ~[-0.2, 0.32]
    #   Cannot predict exact value; return deterministic pseudo-random per x.
    import math
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -88.2 <= x <= -77.8:
            h = math.sin(x * 12.9898) * 43758.5453
            frac = h - math.floor(h)
            out.append(-0.2 + 0.52 * frac)
        else:
            out.append(0.0)
    return {"y": out}
