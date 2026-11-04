import math

def predict(probe):
    # f(x) is hash-like/pseudo-random in [-1,1] for x >= 1 [E1,E2,E3,E4]
    # f(0) = 473.8752, a special spike [E2]
    # For 0 < x < 1, f is large and smooth-ish: f(0.1)=14.48, f(0.2)=13.87, f(0.5)=13.36 [E4]
    #   -> looks like ~14.5 - x-ish, a distinct small-interval regime [E4]
    # Negative x: ordinary hash-like values in [-1,1] [E1,E2]
    # No simple periodic structure in integer part; values look hashed [E4]
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                out.append(473.8752)
            elif 0 < x < 1:
                # small positive interval: large values, roughly linear decreasing
                out.append(round(14.5 - 2.3 * x, 4))
            else:
                v = math.sin(x) * 10000.0
                v = v - math.floor(v)
                out.append(round(v * 2 - 1, 4))
        except Exception:
            out.append(None)
    return {"y": out}
