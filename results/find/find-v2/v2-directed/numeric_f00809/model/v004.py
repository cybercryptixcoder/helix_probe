import random

def predict(probe):
    # Outputs are bounded roughly in [-0.26, 0.26], occasionally a bit beyond [E1,E15,E20]
    # Repeated x give different y => stochastic, not deterministic [E2,E13,E14,E15,E16,E17,E18,E19,E23]
    # Per-x means over repeats are near zero and not clearly different across x [E16,E17,E18,E19,E21,E22,E23]
    # No reproducible dependence on x found anywhere in [-128,128] [E1-E23]
    # E23 at x=0: 20 samples spread ~[-0.13,0.22], mean ~0.01, consistent with uniform noise
    # Best model: f(x) = uniform noise on roughly [-0.26,0.26], independent of x [E1-E23]
    # Slight widening: E15 saw 0.3587, E20 saw 0.3154, E22 saw 0.2618, so use ~[-0.30,0.30] (?)
    return {"y": [round(random.uniform(-0.30, 0.30), 4) for _ in probe["x"]]}
