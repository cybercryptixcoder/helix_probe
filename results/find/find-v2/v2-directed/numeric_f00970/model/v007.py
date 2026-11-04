import math

def predict(probe):
    # Beliefs:
    # - Two-region function: plateau for |x| < ~3.06, near-zero tail for |x| > ~3.06 [E13-E19]
    # - Plateau mean ~12.0, noise sd ~1.1; flat, no systematic shape [E16,E17,E19]
    # - Tail mean ~0, noise sd ~1.0 [E1-E6,E10,E13,E14,E16,E19]
    # - Threshold ~3.06 (3.05 still plateau, 3.08 tail) [E18,E19]
    # - Output is noisy; predict the mean of each region [E11,E12,E16,E17]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(12.0 if abs(x) < 3.06 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}
