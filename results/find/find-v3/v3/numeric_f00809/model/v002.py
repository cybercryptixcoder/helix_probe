import math

def predict(probe):
    # Observations: outputs are small, mostly |y|<0.35, irregular sign changes [E1-E4].
    # No smooth trend across x; looks like deterministic pseudo-noise [E2,E4].
    # Magnitude tends to shrink for large |x| (e.g. |x|>80 gives |y|<0.01) [E2,E4].
    # Near x=0 outputs are also small [E2].
    # Best guess: y = noise(x) * envelope(x), envelope peaks mid-range.
    ys = []
    for x in probe["x"]:
        # pseudo-noise from x
        h = math.sin(x * 12.9898 + 78.233) * 43758.5453
        frac = h - math.floor(h)
        noise = (frac - 0.5) * 0.7
        # envelope: small near 0 and at large |x|, larger in mid range
        env = 1.0
        ax = abs(x)
        if ax < 1:
            env = 0.3 + 0.7 * ax
        elif ax > 80:
            env = max(0.05, 1.0 - (ax - 80) / 60.0)
        ys.append(round(noise * env, 4))
    return {"y": ys}
