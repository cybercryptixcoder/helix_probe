import math

def predict(probe):
    # Beliefs:
    # The function is smooth everywhere; no separate oscillatory region. [E2,E4,E6]
    # Left outer (x <= -14): linear, slope ~ -0.00029, from (-128,0.0479) to (-14,0.0142) [E2,E4]
    # Right outer (x >= 26): linear, slope ~ +0.00029, from (26,0.0014) to (128,0.0565) [E6]
    # Interior [-14,26]: smooth curve with a broad peak ~0.0784 near x=-2 and a sharp dip
    #   reaching ~-0.0932 near x=1.1. [E8,E10,E14]
    # The peak is flat-topped: ~0.0775-0.0784 across x in [-2.4,-0.9]. [E14]
    # The dip minimum is near x=1.1 (~-0.0932), slightly right of x=1. [E14]
    # Curve is smooth (MLP-like); use dense anchors + cubic-ish interpolation. [E14]

    anchors = [
        (-14.0, 0.0142),
        (-13.0, 0.0156),
        (-12.0, 0.0187),
        (-11.0, 0.0218),
        (-10.0, 0.0249),
        (-9.0, 0.0280),
        (-8.0, 0.0310),
        (-7.0, 0.0389),
        (-6.0, 0.0471),
        (-5.0, 0.0550),
        (-4.0, 0.0628),
        (-3.0, 0.0706),
        (-2.5, 0.0745),
        (-2.4, 0.0753),
        (-2.2, 0.0768),
        (-2.0, 0.0784),
        (-1.9, 0.0784),
        (-1.7, 0.0782),
        (-1.5, 0.0780),
        (-1.3, 0.0778),
        (-1.1, 0.0777),
        (-1.0, 0.0776),
        (-0.9, 0.0775),
        (-0.7, 0.0704),
        (-0.5, 0.0490),
        (-0.3, 0.0277),
        (-0.1, 0.0087),
        (0.0, -0.0008),
        (0.1, -0.0104),
        (0.3, -0.0294),
        (0.5, -0.0484),
        (0.7, -0.0758),
        (0.9, -0.0928),
        (1.0, -0.0951),
        (1.1, -0.0932),
        (1.3, -0.0858),
        (1.5, -0.0782),
        (1.7, -0.0705),
        (1.9, -0.0629),
        (2.0, -0.0595),
        (2.2, -0.0560),
        (2.4, -0.0525),
        (2.5, -0.0507),
        (3.0, -0.0466),
        (4.0, -0.0438),
        (6.0, -0.0371),
        (8.0, -0.0300),
        (10.0, -0.0249),
        (11.0, -0.0228),
        (12.0, -0.0208),
        (13.0, -0.0187),
        (14.0, -0.0167),
        (15.0, -0.0146),
        (16.0, -0.0126),
        (17.0, -0.0105),
        (18.0, -0.0084),
        (19.0, -0.0064),
        (20.0, -0.0043),
        (21.0, -0.0023),
        (22.0, -0.0008),
        (23.0, -0.0002),
        (24.0, 0.0003),
        (25.0, 0.0009),
        (26.0, 0.0014),
    ]

    def interp(x):
        # Catmull-Rom style cubic interpolation through anchors for smoothness
        n = len(anchors)
        # find segment
        lo, hi = 0, n - 1
        if x <= anchors[0][0]:
            return anchors[0][1]
        if x >= anchors[-1][0]:
            return anchors[-1][1]
        for i in range(n - 1):
            if anchors[i][0] <= x <= anchors[i + 1][0]:
                lo, hi = i, i + 1
                break
        x0, y0 = anchors[lo]
        x1, y1 = anchors[hi]
        # neighbors for tangents
        if lo > 0:
            xm, ym = anchors[lo - 1]
        else:
            xm, ym = x0 - (x1 - x0), y0
        if hi < n - 1:
            xp, yp = anchors[hi + 1]
        else:
            xp, yp = x1 + (x1 - x0), y1
        # tangents (finite difference)
        m0 = (y1 - ym) / (x1 - xm) if x1 != xm else 0.0
        m1 = (yp - y0) / (xp - x0) if xp != x0 else 0.0
        h = x1 - x0
        t = (x - x0) / h
        t2 = t * t
        t3 = t2 * t
        h00 = 2 * t3 - 3 * t2 + 1
        h10 = t3 - 2 * t2 + t
        h01 = -2 * t3 + 3 * t2
        h11 = t3 - t2
        return h00 * y0 + h10 * h * m0 + h01 * y1 + h11 * h * m1

    out = []
    for x in probe["x"]:
        try:
            if x <= -14.0:
                y = 0.0142 + (x + 14.0) * (0.0479 - 0.0142) / (-128.0 + 14.0)
            elif x >= 26.0:
                y = 0.0014 + (x - 26.0) * (0.0565 - 0.0014) / (128.0 - 26.0)
            else:
                y = interp(x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
