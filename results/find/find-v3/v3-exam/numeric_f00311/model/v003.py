import math

def predict(probe):
    # f(x) = 8 - 9.6*x for x >= -9.3 [E2, E3, E4, E5, E6]
    # f(x) ≈ 8 + noise for x < -9.3 [E1, E2, E4, E5, E6]
    # Boundary: x=-9.55 -> small (8.05), x=-9.3 -> linear (97.28) [E6]
    # So switch is in (-9.55, -9.3]; use x < -9.3 -> small, else linear.
    # Small branch is 8 plus small noise (std ~0.1) [E6]; predict mean 8.
    out = []
    for x in probe["x"]:
        if x < -9.3:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}
