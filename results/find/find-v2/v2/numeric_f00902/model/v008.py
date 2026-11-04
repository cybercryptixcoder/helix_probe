def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the flat band [E1,E2,E13,E15]
    # Flat band: constant ~7773 (noisy) for x in [97.55, 117.75) [E16,E12,E10]
    #   E16: 97.5 cubic, 97.55 flat => left edge in (97.5, 97.55], use 97.55
    #   E12: 117.74 cubic, 117.75 flat => right edge in (117.74, 117.75], use 117.75
    #   E10: 117.7 flat, 117.75 cubic (conflicts E12; E12 denser => trust E12)
    #   E14: 97.68..98.3 all flat (consistent with left edge <= 97.55)
    out = []
    for x in probe["x"]:
        if 97.55 <= x < 117.75:
            out.append(7772.95)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
