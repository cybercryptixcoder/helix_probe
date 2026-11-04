import math

def predict(probe):
    # Beliefs:
    # - Two-region function: plateau for |x| < ~3.055, near-zero tail for |x| > ~3.055 [E13-E20]
    # - Boundary is sharp: 3.05 plateau, 3.06 tail [E18,E19,E20]
    # - Plateau mean ~11.9, noise sd ~1.1; flat, no systematic shape [E16,E17,E19,E21]
    # - Tail mean ~0, noise sd ~1.0 [E1-E6,E10,E13,E14,E16,E19]
    # - Output is noisy; predict the mean of each region [E11,E12,E16,E17]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(11.9 if abs(x) < 3.055 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}
