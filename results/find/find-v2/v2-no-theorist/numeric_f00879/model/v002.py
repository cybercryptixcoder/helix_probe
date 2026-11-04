import math

def predict(probe):
    # Observations:
    # - Outputs are small, roughly in [-3, 3] [E1, E2, E3].
    # - No obvious monotonic trend; looks oscillatory/noisy [E2].
    # - E2 dense sweep shows irregular sign changes, no clear period [E2].
    # - Values look like a sum of a few sinusoids with incommensurate freqs [E1-E3].
    # - Hard to fit precisely; use a smooth oscillatory guess.
    # ? True mechanism unknown; this is a rough multi-sine guess.
    out = []
    for x in probe.get("x", []):
        try:
            v = (1.5*math.sin(0.05*x + 0.7)
                 + 1.0*math.sin(0.11*x + 2.1)
                 + 0.6*math.cos(0.23*x + 0.4))
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}
