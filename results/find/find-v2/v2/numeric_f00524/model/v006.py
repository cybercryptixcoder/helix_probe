import math

def predict(probe):
    # f(x) = ceil(x) on the nonzero region [E4, E6]
    # Left boundary: -4 inclusive (ceil(-4)=-4), -4.5->0 [E4]
    # Right boundary: 4.35->5, 4.36->0 [E8], so region ends between 4.35 and 4.36
    # Outside region: 0 [E1,E3,E5,E7]
    # f(x)=ceil(x) throughout interior [E4,E6,E8]
    out = []
    for x in probe["x"]:
        try:
            if -4.0 <= x <= 4.35:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
