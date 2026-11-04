import math

def predict(probe):
    # f(x) = -1.7 + 1.8x - 3.3x^2 for |x| < 0.8 [E2,E4]
    # f(x) = 0 for |x| >= 0.8 [E1,E2,E3,E4,E5,E6]
    # Boundary is at |x| = 0.8: x=0.8 gives -2.372 (nonzero), x=0.82 gives 0 [E6]
    out = []
    for x in probe["x"]:
        if abs(x) < 0.8:
            out.append(-1.7 + 1.8*x - 3.3*x*x)
        else:
            out.append(-0.0)
    return {"y": out}
