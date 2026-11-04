import math

def predict(probe):
    # Two linear regimes blended by a logistic near x=0 [E1,E2,E3,E4,E5,E6]:
    #   left  L(x) = -6.7601*x + 2.3937   (x<0 far)
    #   right R(x) = -16.9002*x + 11.2218 (x>0 far)
    # Smooth transition: y = L + (R-L)*sigmoid(4.0*(x-0.15)) [E4,E6]
    # (not a sharp break at 0; blend centered near x=0.15, width ~0.25)
    xs = probe["x"]
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        L = -6.7601 * x + 2.3937
        R = -16.9002 * x + 11.2218
        s = 1.0 / (1.0 + math.exp(-4.0 * (x - 0.15)))
        ys.append(L + (R - L) * s)
    return {"y": ys}
