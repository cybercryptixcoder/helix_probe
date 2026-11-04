import math

def predict(probe):
    # Beliefs:
    # - For |x| >= 1: output is pseudorandom in [-1,1], no smooth structure [E1,E3-E13]
    # - Special region is 0 < x < 1 (NOT |x|<1): large values ~12-14 [E14,E16]
    # - Negative side -1 < x < 0: moderate values ~6-7.5, NOT huge [E16]
    # - At x=0: huge outlier 475.5144 [E2]
    # - Boundary at x=1 and x=-1 sharp [E16]
    xs = probe["x"]
    ys = []
    for x in xs:
        if x == 0:
            ys.append(475.5144)
        elif 0 < x < 1:
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(12.0 + 2.0 * frac)
        elif -1 < x < 0:
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(6.0 + 1.5 * frac)
        else:
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(frac * 2.0 - 1.0)
    return {"y": ys}
