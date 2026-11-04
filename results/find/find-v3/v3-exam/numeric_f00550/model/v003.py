import math

def predict(probe):
    # f(x) = -1.7 + 1.8x - 3.3x^2 for |x| < 0.85 (boundary in (0.8,0.9), guessed 0.85) [E2,E4]
    # f(x) = 0 for |x| >= 0.85 [E1,E2,E3,E4]
    out = []
    for x in probe["x"]:
        if abs(x) < 0.85:
            out.append(-1.7 + 1.8*x - 3.3*x*x)
        else:
            out.append(-0.0)
    return {"y": out}
