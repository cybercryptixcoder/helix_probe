import math

def predict(probe):
    # Model hypothesis:
    # - For x != 0: f(x) = sin(x) (radians), rounded to 4 dp [E1, E2 all nonzero points].
    # - At x = 0: f(0) = 475.3502, a special spike [E2]. Not sin(0)=0.
    #   The interval of different behavior appears to be the single point x=0.
    #   (Only one sample at 0 so far; treat as a point exception.)
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                out.append(475.3502)
            else:
                out.append(round(math.sin(x), 4))
        except Exception:
            out.append(None)
    return {"y": out}
