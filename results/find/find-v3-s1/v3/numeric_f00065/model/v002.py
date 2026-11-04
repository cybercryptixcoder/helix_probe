import math

def predict(probe):
    # Model: f is a smooth, monotone-decreasing function of x on [-128,128].
    # E2: y decreases monotonically as x increases (215.8 at -128 down to -328.4 at 128).
    # E1: same monotone-decreasing pattern (x=-120.7 -> 203, x=88.9 -> -230.7).
    # The function is NOT odd: y(0) = -8.67, not 0. It's roughly linear with a
    #   gentle curvature; slope ~ (215.8 - (-328.4))/256 = 2.126 per unit x.
    # Fit a smooth curve through E2's 19 points. It looks close to linear with
    #   slight downward curvature (concave). Use piecewise-linear interpolation
    #   over the E2 anchor points, which are dense enough across the domain.
    # Anchors from E2 (ground truth):
    anchors = [
        (-128, 215.7687), (-96, 159.678), (-64, 103.5874), (-48, 75.5447),
        (-32, 47.4895), (-24, 33.4554), (-16, 19.4414), (-8, 5.4165),
        (-4, -1.6258), (0, -8.6723), (4, -18.5846), (8, -28.5786),
        (16, -48.5665), (24, -68.5545), (32, -88.5424), (48, -128.5184),
        (64, -168.4943), (96, -248.4648), (128, -328.4446),
    ]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        # clamp to domain
        xc = max(-128.0, min(128.0, float(x)))
        # piecewise linear interpolation
        if xc <= anchors[0][0]:
            y = anchors[0][1]
        elif xc >= anchors[-1][0]:
            y = anchors[-1][1]
        else:
            for i in range(len(anchors) - 1):
                x0, y0 = anchors[i]
                x1, y1 = anchors[i + 1]
                if x0 <= xc <= x1:
                    t = (xc - x0) / (x1 - x0)
                    y = y0 + t * (y1 - y0)
                    break
        ys.append(round(y, 4))
    return {"y": ys}
