import math

def predict(probe):
    # f(x) is hash-like/pseudo-random in [-1,1] for x >= 1 [E1,E2,E3,E4]
    # f(x) is hash-like/pseudo-random in [-1,1] for x < 0 [E1,E2,E5]
    # f(0) = 473.8752, a special spike [E2]
    # For 0 < x < 0.85: large values ~13-14.5, noisy, roughly flat [E4,E6]
    # For 0.85 <= x < 1: hash-like in [-1,1] (E6 shows 0.85 already hash-like) [E6]
    #   boundary between regimes is somewhere in (0.75, 0.85] [E6]
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                out.append(473.8752)
            elif 0 < x < 0.8:
                # small positive interval: large noisy values around 13.5
                out.append(round(13.5, 4))
            else:
                v = math.sin(x) * 10000.0
                v = v - math.floor(v)
                out.append(round(v * 2 - 1, 4))
        except Exception:
            out.append(None)
    return {"y": out}
