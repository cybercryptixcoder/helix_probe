import math

def predict(probe):
    # f(x) = ceil(x) on the nonzero region [E2,E4,E6]
    # Nonzero region is roughly [-4, 4.4] on the right [E6: 4.35->5, 4.4->0; E4: 4.1->5, 4.5->0]
    # Left boundary: -4 inclusive (ceil(-4)=-4), -4.5->0 [E4]
    # Outside region: 0 [E1,E3,E5]
    # Right boundary between 4.35 and 4.4 (4.35->5, 4.4->0) [E6]
    # Note: 4.05->5 [E6] confirms ceil continues past 4
    out = []
    for x in probe["x"]:
        try:
            if -4.0 <= x < 4.4:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
