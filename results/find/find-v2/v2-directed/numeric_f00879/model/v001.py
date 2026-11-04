import random

def predict(probe):
    # Observations:
    # - Outputs are noisy/random-looking: same x gives different y [E2]
    # - Range roughly [-2, 3], centered near 0.5 [E1, E2]
    # - No clear deterministic structure detectable [E1, E2]
    # Best guess: f(x) = random noise, roughly uniform in [-2, 3] (?)
    # We cannot predict exact values; return a fixed mid estimate.
    return {"y": [0.5 for _ in probe["x"]]}
