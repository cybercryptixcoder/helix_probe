import math

def predict(probe):
    # Beliefs (one line each, citing evidence):
    # - There is a flat "dead zone" around 0 where output is constant -20.4469 [E2, E10]
    # - The dead zone is roughly x in (-20.0, 4.0); at x=4 output is -12.9234 (already leaving) [E10, E12]
    # - Just outside the dead zone the curve is smooth and monotone, not a hard jump [E12]
    # - For x >= ~4, output grows like a smooth convex curve; small x gives small values [E8, E12]
    # - For x <= ~-20, output grows again symmetrically-ish but the left side is much steeper [E6]
    # - Large |x| gives large positive outputs, roughly quadratic-ish at large scale [E1, E3, E9]
    # - f is essentially even in magnitude behavior? No: left side reaches 12684 at -90, right side 19182 at 82 [E6, E4]
    # - The MLP approximates something like max(0, |x|-a)^2-ish outside a dead zone, with different scales per side [E6, E8]
    # - Exact values at many points are given; fit a smooth piecewise model through them [E4, E8, E12]
    # - The dead zone value is -20.4469 exactly [E2, E10]
    # - Left boundary: at x=-20.0 still -20.4469, at -20.2 it's -19.49, at -20.6 it's -3.53 [E6]
    # - Right boundary: at x=4.0 it's -12.9234, 3.8 -> -20.16, 4.2 -> -5.69 [E12]
    # - So dead zone is about [-20.0, 3.9] with smooth transitions [E6, E12]

    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            out.append(_f(float(v)))
        except Exception:
            out.append(None)
    return {"y": out}


def _f(x):
    # Dead zone
    if -20.0 <= x <= 3.9:
        return -20.4469

    # Right side (x > 3.9): smooth convex increasing curve.
    # Anchor points from evidence (x, y):
    # 4.0 -12.9234, 4.2 -5.6859, 4.4 6.1095, 4.5 13.1559, 4.6 20.2023,
    # 4.7 27.2487, 4.8 34.2951, 5.0 48.3879, 5.5 95.9038, 6.0 146.0188,
    # 7.0 272.1343, 8.0 398.2498, 9.0 524.3653, 10 650.4807, 11 776.5962,
    # 13 1028.8272, 16 1407.1737, 19 1785.5202, 21 2050.9231, 24 2460.9815,
    # 28 3102.7698, 33 4024.1817, 40 5505.5302, 50 8005.6264, 62 11605.9694,
    # 65 12609.0929, 67 13300.1269, 72 15106.2647, 77 17027.5388, 82 19182.3021
    if x > 3.9:
        return _right(x)

    # Left side (x < -20.0)
    # Anchors: -20.2 -19.4911, -20.4 -11.7551, -20.6 -3.531, -22 54.0378,
    # -25 204.0128, -28 401.1526, -32 711.7673, -40 1531.8654, -45 2179.6225,
    # -48.6 2710.6724, -50.4 2995.4039, -55.8 3927.9297, -61.3 5003.1218,
    # -61.7 5086.1272, -63.9 5554.3344, -65.6 5926.6267, -66.9 6224.5127,
    # -70 6954.3912, -79.1 9329.3859, -90 12684.3448, -100.1 15914.9098,
    # -102.2 16586.6114, -107.4 18249.8726, -124.4 23687.4572,
    # -127.7 24742.9884
    return _left(x)


# Right-side anchor table, sorted by x
_RIGHT = [
    (4.0, -12.9234), (4.2, -5.6859), (4.4, 6.1095), (4.5, 13.1559),
    (4.6, 20.2023), (4.7, 27.2487), (4.8, 34.2951), (5.0, 48.3879),
    (5.5, 95.9038), (6.0, 146.0188), (7.0, 272.1343), (8.0, 398.2498),
    (9.0, 524.3653), (10.0, 650.4807), (11.0, 776.5962), (13.0, 1028.8272),
    (16.0, 1407.1737), (19.0, 1785.5202), (21.0, 2050.9231), (24.0, 2460.9815),
    (28.0, 3102.7698), (33.0, 4024.1817), (40.0, 5505.5302), (50.0, 8005.6264),
    (62.0, 11605.9694), (65.0, 12609.0929), (67.0, 13300.1269),
    (72.0, 15106.2647), (77.0, 17027.5388), (82.0, 19182.3021),
    (88.2, 21854.2087), (93.5, 24138.2578), (94.1, 24396.8294),
    (94.8, 24698.4963), (102.1, 27844.4507), (103.0, 28232.3081),
    (104.5, 28878.7371), (104.9, 29051.1182), (105.7, 29395.8803),
    (110.8, 31593.7389), (119.5, 35343.0271), (119.7, 35429.2177),
    (123.6, 37109.9331),
]

# Left-side anchor table (x negative), sorted by x ascending (most negative first)
_LEFT = [
    (-127.7, 24742.9884), (-124.4, 23687.4572), (-107.4, 18249.8726),
    (-102.2, 16586.6114), (-100.1, 15914.9098), (-90.0, 12684.3448),
    (-79.1, 9329.3859), (-70.0, 6954.3912), (-66.9, 6224.5127),
    (-65.6, 5926.6267), (-63.9, 5554.3344), (-61.7, 5086.1272),
    (-61.3, 5003.1218), (-55.8, 3927.9297), (-50.4, 2995.4039),
    (-48.6, 2710.6724), (-45.0, 2179.6225), (-40.0, 1531.8654),
    (-32.0, 711.7673), (-28.0, 401.1526), (-25.0, 204.0128),
    (-22.0, 54.0378), (-20.6, -3.531), (-20.4, -11.7551), (-20.2, -19.4911),
]


def _interp(table, x):
    # table sorted by x ascending
    if x <= table[0][0]:
        # extrapolate linearly using first two
        (x0, y0), (x1, y1) = table[0], table[1]
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    if x >= table[-1][0]:
        (x0, y0), (x1, y1) = table[-2], table[-1]
        return y1 + (y1 - y0) * (x - x1) / (x1 - x0)
    # binary search
    lo, hi = 0, len(table) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if table[mid][0] <= x:
            lo = mid
        else:
            hi = mid
    x0, y0 = table[lo]
    x1, y1 = table[hi]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def _right(x):
    if x > 123.6:
        # extrapolate: roughly quadratic; use last slope
        (x0, y0), (x1, y1) = _RIGHT[-2], _RIGHT[-1]
        slope = (y1 - y0) / (x1 - x0)
        return y1 + slope * (x - x1)
    return _interp(_RIGHT, x)


def _left(x):
    if x < -127.7:
        (x0, y0), (x1, y1) = _LEFT[0], _LEFT[1]
        slope = (y1 - y0) / (x1 - x0)
        return y0 + slope * (x - x0)
    return _interp(_LEFT, x)
