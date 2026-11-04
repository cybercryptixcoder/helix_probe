def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the flat band [E1,E2,E3,E5,E7]
    # Flat band: constant ~7772.9 (noise) for x in [97.75, 117.75] [E8]
    #   97.5 -> cubic, 97.75 -> flat; 117.75 -> flat, 118 -> cubic [E8]
    # Band value ~7772.9 with small noise; use ~7772.95 [E4,E6,E8]
    out = []
    for x in probe["x"]:
        if 97.75 <= x <= 117.75:
            out.append(7772.95)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
