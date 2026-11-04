import math

def predict(probe):
    # Outputs are bounded roughly in [-0.26, 0.26] [E1, E2, E3]
    # Repeated x give different y => stochastic, not a deterministic function of x [E2]
    # No reproducible dependence on x: same x (0, -24) gave different y in E3 [E3]
    # Values look like uniform noise independent of x [E1, E2, E3]
    # Best model: f(x) = uniform(-0.26, 0.26), independent of x [E1, E2, E3]
    import random
    return {"y": [round(random.uniform(-0.26, 0.26), 4) for _ in probe["x"]]}
