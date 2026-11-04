import math

def predict(probe):
    # Beliefs:
    # - For |x| >= 1: output is pseudorandom in [-1,1], no smooth structure [E1,E3-E13]
    # - Special region is 0 < x < 1 (NOT |x|<1): large values ~12-14 [E14,E16]
    # - Negative side -1 < x < 0: moderate values ~6-7.5, NOT huge [E16]
    # - At x=0: huge outlier 475.5144 [E2]
    # - Boundary at x=1 and x=-1 sharp [E16]
    # - E18: interior of (-1,0) and (0,1) is pseudorandom too, not smooth [E18]
    #   -0.95,-0.85 give ~-0.4,-0.17 (small, near boundary); -0.7..-0.05 give 6-7.6
    #   0.05..0.7 give 12-14.4; 0.85,0.95 give ~0.57,0.64 (small, near boundary)
    #   So the special band does NOT extend all the way to |x|=1: it shrinks near edges.
    #   Actually: -0.85 -> -0.17, -0.95 -> -0.43 (small); 0.85 -> 0.57, 0.95 -> 0.64 (small)
    #   So special region is roughly |x| < 0.8, with |x| in [0.8,1) being ordinary pseudorandom.
    xs = probe["x"]
    ys = []
    for x in xs:
        h = math.sin(x * 12.9898 + 78.233) * 43758.5453
        frac = h - math.floor(h)
        if x == 0:
            ys.append(475.5144)
        elif 0 < x < 0.8:
            ys.append(12.0 + 2.0 * frac)
        elif -0.8 < x < 0:
            ys.append(6.0 + 1.5 * frac)
        else:
            ys.append(frac * 2.0 - 1.0)
    return {"y": ys}
