import math

def predict(probe):
    # Outputs are bounded roughly in [-0.26, 0.26], occasionally a bit beyond [E1,E15,E20]
    # Repeated x give different y => stochastic, not deterministic [E2,E13,E14,E15,E16,E17,E18,E19]
    # Per-x means over 10 repeats are near zero and not clearly different across x [E16,E17,E18,E19]
    # No reproducible dependence on x found anywhere in [-128,128] [E1-E20]
    # Best model: f(x) = uniform noise on roughly [-0.26,0.26], independent of x [E1-E20]
    # Slight widening: E15 saw 0.3587 and E20 saw 0.3154, so use ~[-0.30,0.30] (?)
    import random
    return {"y": [round(random.uniform(-0.30, 0.30), 4) for _ in probe["x"]]}
