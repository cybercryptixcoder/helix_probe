import math

def predict(probe):
    # Observations are small (~0.05-0.25), irregular in sign, not odd [E2].
    # f(-x) != -f(x): f(88.2)=-0.0513 vs f(-88.2)=0.0067 [E2].
    # No obvious periodicity from the arithmetic sweep [E4].
    # Values look like a bounded, roughly random-looking oscillation in [-0.25,0.25].
    # Best guess: high-frequency oscillation with slowly varying envelope.
    # Use product of two incommensurate sinusoids as placeholder hypothesis.
    out = []
    for x in probe.get("x", []):
        try:
            v = 0.15 * math.sin(x * 1.3 + 0.5) * math.cos(x * 0.37 + 1.1)
        except Exception:
            v = None
        out.append(v)
    return {"y": out}
