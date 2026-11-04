import math

def predict(probe):
    # Observations look like noise around 0 with occasional larger values.
    # No clear deterministic structure across E1/E2; magnitudes mostly < 0.35.
    # Best guess: f(x) = sin(x)*something? Check: sin(88.2)=-0.66, not -0.07.
    # Try sin(x)/x-ish? No consistent pattern.
    # E2 shows values not monotone, sign changes irregularly -> likely noisy.
    # Model as small pseudo-random noise seeded by x, mean 0.
    # Use a deterministic hash-like function of x to mimic noise.
    ys = []
    for x in probe["x"]:
        # deterministic pseudo-noise in roughly [-0.35, 0.35]
        h = math.sin(x * 12.9898 + 78.233) * 43758.5453
        frac = h - math.floor(h)
        ys.append(round((frac - 0.5) * 0.7, 4))
    return {"y": ys}
