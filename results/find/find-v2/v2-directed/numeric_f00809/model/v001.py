import random

def predict(probe):
    # Outputs look like random noise in ~[-0.26, 0.26] [E1, E2]
    # Repeated x give different y => stochastic, no dependence on x [E2]
    # Range of |y| < 0.3 across all x in [-128,128] [E1, E2]
    # Best guess: f(x) = uniform(-0.3, 0.3) independent of x [E1, E2]
    return {"y": [round(random.uniform(-0.3, 0.3), 4) for _ in probe["x"]]}
