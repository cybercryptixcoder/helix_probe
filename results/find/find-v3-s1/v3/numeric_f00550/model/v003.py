import math

def predict(probe):
    # f(x) = 0 outside a small interval around 0 [E1, E2, E3]
    # Inside the interval, f is nonzero and varies smoothly [E4]
    # Data points (x, y) from E2 and E4:
    #   x=0 -> -1.7
    #   x=0.5 -> -1.625, x=-0.5 -> -3.425
    #   x=0.1 -> -1.553, 0.2 -> -1.472, 0.25 -> -1.4562, 0.3 -> -1.457,
    #   0.4 -> -1.508, 0.45 -> -1.5582, 0.49 -> -1.6103, 0.51 -> -1.6403,
    #   0.55 -> -1.7083, 0.6 -> -1.808, 0.7 -> -2.057, 0.75 -> -2.2062,
    #   0.8 -> -2.372, 0.9 -> -0.0
    #   x=-0.1 -> -1.913, -0.2 -> -2.192, -0.25 -> -2.3563, -0.3 -> -2.537,
    #   -0.4 -> -2.948, -0.49 -> -3.3743
    #
    # Observations:
    # - At x=0.9 output is 0, so interval boundary is between 0.8 and 0.9.
    # - On positive side: dips to ~-1.456 near x=0.25, rises to -1.7 at 0,
    #   then decreases (more negative) as x grows toward 0.8.
    # - On negative side: at -0.1 -> -1.913, monotonically more negative
    #   toward -0.5 -> -3.425. Looks like a smooth curve.
    # - At x=0 value -1.7 doesn't fit a simple smooth curve through
    #   neighbors (0.1->-1.553, -0.1->-1.913); maybe there's a cusp or
    #   the function is |x|-based: e.g. f(x) = -1.7 - something.
    #
    # Try: f(x) = -1.7 - a*|x|^p for small |x|? At x=0.1: -1.553 means
    #   a*0.1^p = -0.147 -> negative a, so f rises. Hmm.
    #
    # Alternative: f(x) = -1.7 + g(x) where g is odd-ish? 
    #   g(0.1)=+0.147, g(-0.1)=-0.213. Not odd.
    #
    # Let's just interpolate. Use piecewise linear interpolation over
    # the known points, with boundary at |x| in [0, ~0.85].
    # Outside -> 0.
    #
    # Boundary guess: between 0.8 and 0.9. Use 0.85? Unknown. Mark with ?.
    # Also negative boundary: -0.49 nonzero, -0.5 -> -3.425 (nonzero).
    #   Need to find where negative side hits 0. Unknown; assume symmetric
    #   boundary ~0.85? But -0.5 is nonzero and -0.49 is -3.3743, so
    #   negative side extends at least to -0.5. Assume symmetric ~0.85.
    
    pos_pts = [
        (0.0, -1.7),
        (0.1, -1.553),
        (0.2, -1.472),
        (0.25, -1.4562),
        (0.3, -1.457),
        (0.4, -1.508),
        (0.45, -1.5582),
        (0.49, -1.6103),
        (0.5, -1.625),
        (0.51, -1.6403),
        (0.55, -1.7083),
        (0.6, -1.808),
        (0.7, -2.057),
        (0.75, -2.2062),
        (0.8, -2.372),
    ]
    neg_pts = [
        (0.0, -1.7),
        (-0.1, -1.913),
        (-0.2, -2.192),
        (-0.25, -2.3563),
        (-0.3, -2.537),
        (-0.4, -2.948),
        (-0.49, -3.3743),
        (-0.5, -3.425),
    ]
    
    def interp(pts, x):
        # pts sorted by x ascending
        if x <= pts[0][0]:
            return pts[0][1]
        if x >= pts[-1][0]:
            return pts[-1][1]
        for i in range(len(pts)-1):
            x0, y0 = pts[i]
            x1, y1 = pts[i+1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0
    
    # Boundary: positive side ends between 0.8 and 0.9 -> guess 0.85 [?]
    # Negative side: last known nonzero at -0.5; assume symmetric 0.85 [?]
    BOUND = 0.85
    
    out = []
    for x in probe["x"]:
        x = float(x)
        if x > BOUND or x < -BOUND:
            out.append(-0.0)
        elif x >= 0:
            out.append(interp(pos_pts, x))
        else:
            out.append(interp(neg_pts, x))
    return {"y": out}
