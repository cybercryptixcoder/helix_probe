import math

def predict(probe):
    # Beliefs:
    # - Two-region function: plateau for |x| < ~3.05, near-zero tail for |x| > ~3.05 [E1-E15]
    # - Plateau mean ~11.6, noise sd ~1.2; no systematic shape detected [E3,E7,E8,E9,E11,E12]
    # - Tail mean ~0, noise sd ~1.0 [E1-E6,E10,E13,E14]
    # - Threshold: E15 shows x=±3.05 inside, ±3.06 outside; E14 shows -3.05 inside, -3.06 outside
    #   E13 shows 3.04 inside, 3.06 outside; so threshold ~3.055, symmetric [E13,E14,E15]
    # - Sharp step, no taper [E13,E14,E15]
    out = []
    for x in probe.get("x", []):
        try:
            out.append(11.6 if abs(x) < 3.055 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}
