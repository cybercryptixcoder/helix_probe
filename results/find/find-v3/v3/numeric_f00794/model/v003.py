import math

def predict(probe):
    # Model hypothesis:
    # - f(x) = sin(x * pi/180) for all nonzero x (degrees), rounded to 4 dp [E8, E10, E11].
    # - At x = 0: a special spike, ~475 [E2, E8]. Value varies slightly (~474.94-475.35),
    #   so treat as a fixed approximate spike; exact value uncertain (?).
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                out.append(475.0)
            else:
                out.append(round(math.sin(x * math.pi / 180.0), 4))
        except Exception:
            out.append(None)
    return {"y": out}
