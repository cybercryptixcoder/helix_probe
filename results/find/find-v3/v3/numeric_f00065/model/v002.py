import math

def predict(probe):
    # Piecewise linear with a kink at x=0. [E1, E2]
    # f(0) = -8.6723 (nonzero intercept). [E2]
    # Slope for x>0 is ~-2.498; slope for x<=0 is ~-1.754. [E1, E2]
    # Not odd: f(88.2)=-228.97 but f(-88.2)=146.0. [E2]
    # Monotonically decreasing everywhere. [E1, E2]
    xs = probe.get("x", [])
    ys = []
    b = -8.6723
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        if x > 0:
            y = b - 2.4977 * x
        else:
            y = b - 1.7537 * x
        ys.append(y)
    return {"y": ys}
