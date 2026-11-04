import math

def predict(probe):
    # f(x) is a deterministic pseudo-random value in [-1,1] for x != 0 [E1,E2,E3]
    # f(0) = 473.8752, a special spike [E2]
    # Values look hash-like, not smooth; no clear structure found [E1,E2,E3]
    # ? Best guess: hash-like function of x; use a common hash-style formula
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                out.append(473.8752)
            else:
                # hash-like: fractional part of sin(x)*large, mapped to [-1,1]
                v = math.sin(x) * 10000.0
                v = v - math.floor(v)
                out.append(round(v * 2 - 1, 4))
        except Exception:
            out.append(None)
    return {"y": out}
