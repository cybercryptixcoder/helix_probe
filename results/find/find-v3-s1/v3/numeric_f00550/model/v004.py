import math

def predict(probe):
    # f(x) = 0 for |x| >= ~0.81 [E2, E3, E5, E6]
    # Nonzero only on a small interval around 0; boundary between 0.8 and 0.82 [E6]
    #   positive: 0.8 -> -2.372, 0.82 -> 0 [E4, E6]
    #   negative: -0.8 -> -5.252, -0.82 -> 0 [E6]
    # Not symmetric: negative side is much steeper/more negative [E4, E6]
    #   -0.6 -> -3.968, -0.7 -> -4.577, -0.8 -> -5.252 [E6]
    #   positive: 0.6 -> -1.808, 0.65 -> -1.9242, 0.7 -> -2.057, 0.8 -> -2.372 [E4, E6]
    # At x=0: -1.7 [E2]
    # Positive side has a local min near x~0.25 (-1.4562) then decreases [E4]
    # Negative side decreases monotonically from 0 [E4, E6]
    # Looks like f(x) = -1.7 - c*|x|^p on each side with different c (and maybe p).
    # Fit: pos side at 0.8: -2.372 => c*0.8^p = 0.672; at 0.4: -1.508 => c*0.4^p=0.192
    #   ratio 0.672/0.192=3.5 = 2^p => p~1.807. But near 0.25 it dips up, so not pure power.
    # Use piecewise linear interpolation over known points; extrapolate to boundary.

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
        (0.65, -1.9242),
        (0.7, -2.057),
        (0.75, -2.2062),
        (0.8, -2.372),
        (0.81, -2.372),  # ? extrapolate flat to boundary
    ]
    neg_pts = [
        (-0.8, -5.252),
        (-0.7, -4.577),
        (-0.6, -3.968),
        (-0.5, -3.425),
        (-0.49, -3.3743),
        (-0.4, -2.948),
        (-0.3, -2.537),
        (-0.25, -2.3563),
        (-0.2, -2.192),
        (-0.1, -1.913),
        (0.0, -1.7),
    ]

    def interp(pts, x):
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

    BOUND = 0.81  # ? between 0.8 and 0.82 [E6]

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
