import math

def predict(probe):
    # Beliefs:
    # - Outputs are ~uniform in [-1,1] for almost all x, looking pseudorandom [E1-E9]
    # - Rapid change over 0.1 steps shows high-frequency / hash-like behavior [E6, E8]
    # - x=0 gives a huge outlier 475.5144, so 0 is a special point [E2]
    # - No visible smooth structure; model as deterministic hash of x plus special 0
    xs = probe["x"]
    ys = []
    for x in xs:
        if x == 0:
            ys.append(475.5144)
        else:
            # hash-like pseudorandom in [-1,1]
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(frac * 2.0 - 1.0)
    return {"y": ys}
