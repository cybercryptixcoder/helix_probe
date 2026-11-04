import math

def predict(probe):
    # Model hypothesis:
    # - f is a deterministic pseudo-random-looking function of x, not a smooth sine [E1, E2, E3]
    # - Values are in roughly [-1, 1] for ordinary x [E1, E2, E3]
    # - There is a special spike at x=0 giving ~475.5 [E2]
    # - The spike is narrow: at x=±16 values are ordinary [E2]
    # - No simple sinusoid fits; treat ordinary part as effectively unpredictable noise.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        # Spike near 0 (only evidence: f(0)=475.5144, f(±16) ordinary)
        # Assume narrow width ~ a few units; exact shape unknown.
        spike = 475.5144 * math.exp(-(x * x) / (2.0 * 3.0 * 3.0))
        # Ordinary part: appears noise-like, no reliable structure found.
        # Best guess: small pseudo-random value in [-1,1] derived from x.
        h = math.sin(x * 12.9898) * 43758.5453
        noise = (h - math.floor(h)) * 2.0 - 1.0
        out.append(spike + noise)
    return {"y": out}
