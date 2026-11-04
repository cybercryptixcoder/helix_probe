import math

def predict(probe):
    # Observed: outputs are tiny (~1e-3 to 1e-4) for |x| large, but 0.1552 at x=-1.2.
    # Hypothesis: a narrow bump/peak near x=0, decaying to ~0 elsewhere.
    # E1 shows peak near -1.2, small values at |x|>=12.9. Shape unknown; guess Gaussian bump.
    # Amplitude ~0.155, center ~ -1.2, width unknown. Use Gaussian with sigma ~2 (?).
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            y = 0.155 * math.exp(-((x + 1.2) ** 2) / (2 * 2.0 ** 2))
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
