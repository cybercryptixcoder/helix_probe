import math

def predict(probe):
    # Beliefs:
    # - Two-region function: plateau for |x| < ~3.05, near-zero tail for |x| > ~3.05 [E1-E17]
    # - Plateau mean ~12.0 (not 11.6), noise sd ~1.1; flat, no systematic shape [E16,E17,E3,E7,E9]
    # - Tail mean ~0, noise sd ~1.0 [E1-E6,E10,E13,E14,E16]
    # - Threshold ~3.055, symmetric, sharp step [E13,E14,E15]
    # - Output is noisy; predict the mean of each region [E11,E12,E16,E17]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(12.0 if abs(x) < 3.055 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}
