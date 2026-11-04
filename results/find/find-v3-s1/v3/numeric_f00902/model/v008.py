import math

def predict(probe):
    # Base formula: f(x) = 1.3*x^3 + 2.3*x^2 - 1.6*x - 48.6 [E2, E4, E10, E19, E21]
    # Plateau region: 97.5 < x < 117.55, value ~ 7772.93 (noisy constant) [E8, E12, E14, E18, E20, E22]
    # Lower boundary: E20 shows 97.5 -> normal, 97.52 -> plateau. E22 shows 97.505 -> plateau.
    #   So boundary is in (97.5, 97.505]. Use 97.5 < x.
    # Upper boundary: E20 shows 117.54 -> plateau, 117.56 -> normal. E22 shows 117.562 -> plateau,
    #   117.565 -> normal. So boundary in (117.562, 117.565]. Use x < 117.563.
    # Plateau value: mean ~7772.93, noise ~±0.2 [E18, E22]

    x = probe["x"]
    result = []
    for xi in x:
        if xi is None:
            result.append(None)
            continue
        if 97.5 < xi < 117.563:
            result.append(7772.93)
        else:
            y = 1.3 * xi**3 + 2.3 * xi**2 - 1.6 * xi - 48.6
            result.append(y)
    return {"y": result}
