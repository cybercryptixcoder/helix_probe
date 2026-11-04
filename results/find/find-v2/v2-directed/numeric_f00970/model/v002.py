import math

def predict(probe):
    # Beliefs:
    # - For |x| < ~2.9: y ~ 12 (noisy plateau) [E1, E2]
    # - For |x| > ~2.9: y ~ 0 (noisy tail) [E1, E2]
    # - Transition is symmetric, between 2.75 and 3.5 on both sides [E2]
    # - Boundary: x=-3 -> 10.94 (inside), x=-3.5 -> 0.95 (outside); x=3 -> 12.58 (inside), x=3.5 -> -0.33 (outside)
    # - So threshold is between 3 and 3.5; pick 3.2 (?)
    # - Noise present; predict the mean of each region.
    out = []
    for x in probe.get("x", []):
        try:
            if abs(x) < 3.2:
                out.append(12.0)
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
