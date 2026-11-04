def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the flat band [E1-E14]
    # Flat band: constant ~7772.9 (noise) for x in [97.68, 117.74) [E4,E6,E12,E14]
    #   E14: 97.68..98.3 all flat => left edge <= 97.68
    #   E12: 97.70,97.72,97.74 flat; 117.74 cubic => right edge <= 117.74
    #   E10: 117.7 flat, 117.75 cubic; 97.74 flat
    #   E8: 97.75 flat, 117.75 cubic
    #   Left edge: <= 97.68 (E14); right edge: <= 117.74 (E12), > 117.7 (E10)
    #   Use [97.68, 117.74) as best estimate; exact left edge uncertain (?)
    out = []
    for x in probe["x"]:
        if 97.68 <= x < 117.74:
            out.append(7772.95)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
