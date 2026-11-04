def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside a flat band [E1, E2, E3, E5]
    # Flat band ~7772.9 for x in [98, 116] approx [E4, E6]: 97 -> cubic, 98 -> flat; 116 -> flat, 118 -> cubic
    # Band value ~7772.9, slight noise [E4, E6]
    out = []
    for x in probe["x"]:
        if 98.0 <= x <= 116.0:
            out.append(7772.93)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
