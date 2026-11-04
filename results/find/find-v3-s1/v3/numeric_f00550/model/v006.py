import math

def predict(probe):
    # Support: nonzero only for |x| < ~0.81 [E6, E8, E10]
    #   positive side ends between 0.79 and 0.805 [E8]
    #   negative side ends between -0.795 and -0.805 [E10]
    # f(0) = -1.7 [E2]
    # Positive side: local min near x~0.28 (-1.4547), then decreases [E4, E8]
    # Negative side: monotone decreasing, steeper than positive [E4, E6, E10]
    # Piecewise-linear interpolation over measured points.

    pos_pts = [
        (0.0, -1.7),
        (0.05, -1.6182),
        (0.1, -1.553),
        (0.15, -1.5042),
        (0.2, -1.472),
        (0.22, -1.4637),
        (0.24, -1.4581),
        (0.25, -1.4562),
        (0.26, -1.4551),
        (0.28, -1.4547),
        (0.3, -1.457),
        (0.35, -1.4742),
        (0.4, -1.508),
        (0.42, -1.5261),
        (0.45, -1.5582),
        (0.47, -1.583),
        (0.48, -1.5963),
        (0.49, -1.6103),
        (0.5, -1.625),
        (0.51, -1.6403),
        (0.52, -1.6563),
        (0.53, -1.673),
        (0.55, -1.7083),
        (0.57, -1.7462),
        (0.6, -1.808),
        (0.62, -1.8525),
        (0.65, -1.9242),
        (0.67, -1.9754),
        (0.7, -2.057),
        (0.72, -2.1147),
        (0.75, -2.2062),
        (0.77, -2.2706),
        (0.79, -2.3375),
    ]
    neg_pts = [
        (-0.795, -5.2167),
        (-0.79, -5.1815),
        (-0.78, -5.1117),
        (-0.75, -4.9062),
        (-0.72, -4.7067),
        (-0.7, -4.577),
        (-0.67, -4.3874),
        (-0.62, -4.0845),
        (-0.6, -3.968),
        (-0.57, -3.7982),
        (-0.52, -3.5283),
        (-0.5, -3.425),
        (-0.49, -3.3743),
        (-0.47, -3.275),
        (-0.42, -3.0381),
        (-0.4, -2.948),
        (-0.35, -2.7342),
        (-0.3, -2.537),
        (-0.28, -2.4627),
        (-0.25, -2.3563),
        (-0.22, -2.2557),
        (-0.2, -2.192),
        (-0.15, -2.0442),
        (-0.1, -1.913),
        (-0.05, -1.7982),
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

    POS_BOUND = 0.80
    NEG_BOUND = 0.80

    out = []
    for x in probe["x"]:
        x = float(x)
        if x > POS_BOUND or x < -NEG_BOUND:
            out.append(-0.0)
        elif x >= 0:
            out.append(interp(pos_pts, x))
        else:
            out.append(interp(neg_pts, x))
    return {"y": out}
