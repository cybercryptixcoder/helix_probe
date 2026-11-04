import math

def predict(probe):
    # Beliefs:
    # - Plateau region |x| < ~3.0: y ~ 12 with noise sd ~1.2 [E1-E12]
    # - Tail region |x| > ~3.0: y ~ 0 with noise sd ~1.0 [E1-E6, E10]
    # - Boundary sharp between 3.0 and 3.1: x=3.0 -> 12.78, x=3.05 -> 11.37 (inside); x=3.1 -> -0.90 (outside) [E6, E10]
    # - x=-3.05 -> 11.37 (inside), x=-3.1 -> 0.61 (outside) [E5, E10]
    # - Threshold ~3.07; symmetric [E2, E5, E6, E10]
    # - Interior mean: pooled repeated samples at 0, ±1.5, 2.5, 2.9 give ~11.5-11.7, slightly below 12 [E11, E12]
    # - No systematic shape detected across interior; treat as flat with mean ~11.6 [E3, E7, E8, E9, E11, E12]
    # - Predict region means (11.6 and 0); noise is irreducible
    out = []
    for x in probe.get("x", []):
        try:
            out.append(11.6 if abs(x) < 3.07 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}
