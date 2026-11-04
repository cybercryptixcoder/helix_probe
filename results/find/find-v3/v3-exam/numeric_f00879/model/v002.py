import math

def predict(probe):
    # Observations are noisy; outputs roughly in [-3.5, 4.5], irregular [E1-E7]
    # No clean periodicity; sin/cos/tan fits fail [E2, E4, E6]
    # Values look like a smooth-ish function of x with noise ~0.5-1.0
    # Best guess: f(x) = sin(x) + noise? No — E6 at x=0 gives 0.41, x=0.5 gives 3.58
    # Try: f(x) = sin(x) + sin(2x) + small offset? E2 x=0 -> 0.90, x=1 -> 3.04
    # Actually looks like f(x) ≈ sin(x) + sin(2x) + 0.5 with heavy noise
    # Given noise dominates, predict the mean-ish trend
    out = []
    for x in probe["x"]:
        try:
            v = math.sin(x) + math.sin(2*x) + 0.5
        except Exception:
            v = None
        out.append(v)
    return {"y": out}
