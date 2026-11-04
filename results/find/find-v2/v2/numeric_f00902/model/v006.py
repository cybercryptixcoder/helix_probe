def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the flat band [E1-E12]
    # Flat band: constant ~7772.9 (noise) for x in (97.75, 117.75) [E8,E10,E12]
    #   E12: 97.74 flat, 97.75 flat, 97.76 flat  => left edge <= 97.74 (flat)
    #   E12: 117.74 cubic, 117.75 cubic, 117.76 cubic => right edge <= 117.74 (cubic)
    #   E10: 97.74 flat, 97.76 flat, 97.75 cubic (conflict w/ E12 97.75 flat -> noise at edge)
    #   E10: 117.7 flat, 117.75 cubic, 117.76 cubic
    #   E8: 97.75 flat, 117.75 cubic
    #   Best fit: band = [97.74, 117.74) with edge noise; use 97.74 <= x < 117.74
    out = []
    for x in probe["x"]:
        if 97.74 <= x < 117.74:
            out.append(7772.95)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
