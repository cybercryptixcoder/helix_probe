import math

def predict(probe):
    # f(x) = ceil(x) on the nonzero region [-4.1, 4.35] [E4, E6, E8, E10, E12]
    # Left boundary: -4.5 -> 0, -4.1 -> -4, so region starts at -4.1 (inclusive) [E12]
    # Right boundary: 4.35 -> 5, 4.36 -> 0, so region ends at 4.35 (inclusive) [E8, E10]
    # Outside region: 0 [E1, E3, E5, E7, E9, E11]
    # f(x)=ceil(x) throughout interior [E2, E4, E6, E8, E10, E12]
    out = []
    for x in probe["x"]:
        try:
            if -4.1 <= x <= 4.35:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
