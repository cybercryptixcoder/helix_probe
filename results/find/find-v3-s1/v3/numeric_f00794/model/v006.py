import math

def predict(probe):
    # Beliefs:
    # - For |x| >= ~1, output is pseudorandom in [-1,1], no smooth structure [E1,E3-E9,E11-E13]
    # - Near x in (0,1): outputs are large (~12-14), not in [-1,1] [E14]
    # - At x=0: huge outlier 475.5144 [E2]
    # - For x in [1,5]: ordinary pseudorandom in [-1,1] [E14]
    # - So there is a special region roughly (0,1) where f blows up; boundary near x=1 [E14]
    # - Hash-like deterministic function elsewhere
    xs = probe["x"]
    ys = []
    for x in xs:
        if x == 0:
            ys.append(475.5144)
        elif 0 < x < 1:
            # special region: large values, roughly 12-14, pseudorandom [E14]
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(12.0 + 2.0 * frac)
        else:
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(frac * 2.0 - 1.0)
    return {"y": ys}
