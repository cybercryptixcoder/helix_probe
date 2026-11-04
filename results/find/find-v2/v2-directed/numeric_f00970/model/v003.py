import math

def predict(probe):
    # Beliefs:
    # - Plateau region |x| < ~3.0: y ~ 12 with noise sd ~1.2 [E1-E6]
    # - Tail region |x| > ~3.0: y ~ 0 with noise sd ~1.0 [E1-E6]
    # - Boundary sharp between 3.0 and 3.05: x=3.0 -> 12.78, x=3.05 -> 11.37 (inside); x=3.1 -> -0.90 (outside) [E6]
    # - x=-3.05 -> 11.37 (inside), x=-3.1 -> 0.61 (outside) [E5]
    # - So threshold ~3.07; symmetric [E2, E5, E6]
    # - Predict region means (12 and 0); noise is irreducible
    out = []
    for x in probe.get("x", []):
        try:
            out.append(12.0 if abs(x) < 3.07 else 0.0)
        except Exception:
            out.append(None)
    return {"y": out}
