import math

def predict(probe):
    # Beliefs (revised after E8):
    # - Central bump: peak ~0.3868 at x=0, asymmetric [E2,E4]
    #   f(1)=0.255, f(-1)=0.1972; f(2)=0.12, f(-2)=0.0575; f(0.5)=0.3225, f(-0.5)=0.3052
    #   f(1.8)=0.147, f(-1.8)=0.0739; f(2.5)=0.0642 [E4]
    # - Far field is NOT a damped oscillation in |x| — E8 shows it is monotone
    #   in |x| on each side, and ASYMMETRIC: right side has a sharp dip near
    #   x~12 (-0.0061) recovering to ~-0.0004 by x=25-50; left side is a
    #   smooth monotone ramp from ~-0.0005 at x=-12 to ~-0.0037 at x=-90 [E8].
    # - Right side far field [E8]: x=12 -> -0.0061, 15 -> -0.0043, 20 -> -0.0013,
    #   25..50 -> -0.0004 (flat). Also E1: 38.8,67.5,73.9,88.9 ~ -0.0002..-0.0004;
    #   102.8,114 ~ -0.0001 [E3]. So right side is ~-0.0004 for x>=25.
    # - Left side far field [E8]: -12:-0.0005, -15:-0.0008, -20:-0.0012,
    #   -25:-0.0017, -30:-0.0021, -35:-0.0026, -40:-0.003, -45..-50:-0.0032,
    #   -60:-0.0032, -70:-0.0034, -80:-0.0035, -90:-0.0037.
    #   E1: -62.7:-0.0032, -93.6:-0.0038, -104:-0.004, -120.7:-0.0043.
    #   E3: -127.5:-0.0044, -120.2:-0.0043, -69.4:-0.0033.
    #   E5: -121.5:-0.0043, -120.6:-0.0043, -72.6:-0.0034, -71.2:-0.0034.
    #   E7: -68.3,-68.9:-0.0033, -72:-0.0034, -53.8:-0.0032, -80.4:-0.0035,
    #   -122.5:-0.0043.
    #   So left ramps smoothly from ~0 at x~-8 to ~-0.0044 at x~-128.
    # - Left moderate region: -8:-0.0002, -6:0, -5:0.0027, -4:0.0053,
    #   -3.5:0.0066, -3:0.008 [E2,E6]; small positive bump near x~-3.5.
    # - Right moderate: 3.5:0.0185, 4:0.0099, 5:0.0012, 6:0.0001, 8:-0.0021,
    #   10:-0.0043 [E6]; secondary bump near x~3.5 then dip toward -0.0043 at 10.
    # - Noise ~0.001.

    xs = probe["x"]
    ys = []
    for x in xs:
        try:
            peak = 0.3868
            sigma = 1.55 if x >= 0 else 1.85
            main = peak * math.exp(-(x * x) / (2 * sigma * sigma))

            # secondary bumps
            right_bump = 0.0185 * math.exp(-((x - 3.5) ** 2) / (2 * 0.8 * 0.8))
            left_bump = 0.0066 * math.exp(-((x + 3.5) ** 2) / (2 * 1.0 * 1.0))

            if x >= 0:
                # right far field: dip near 12, recover to -0.0004 by 25+
                # anchor: 8:-0.0021, 10:-0.0043, 12:-0.0061, 15:-0.0043,
                #         20:-0.0013, 25:-0.0004, 30..50:-0.0004
                if x <= 25:
                    # piecewise smooth via interpolation on key points
                    pts = [(8, -0.0021), (10, -0.0043), (12, -0.0061),
                           (15, -0.0043), (20, -0.0013), (25, -0.0004)]
                    far = _interp(x, pts)
                else:
                    far = -0.0004
            else:
                ax = -x
                # left far field: smooth monotone ramp
                # anchor: 8:-0.0002, 10:-0.0004, 12:-0.0005, 15:-0.0008,
                #         20:-0.0012, 25:-0.0017, 30:-0.0021, 35:-0.0026,
                #         40:-0.003, 45:-0.0032, 50:-0.0032, 60:-0.0032,
                #         70:-0.0034, 80:-0.0035, 90:-0.0037, 104:-0.004,
                #         120:-0.0043, 128:-0.0044
                pts = [(8, -0.0002), (10, -0.0004), (12, -0.0005), (15, -0.0008),
                       (20, -0.0012), (25, -0.0017), (30, -0.0021), (35, -0.0026),
                       (40, -0.0030), (45, -0.0032), (50, -0.0032), (60, -0.0032),
                       (70, -0.0034), (80, -0.0035), (90, -0.0037), (104, -0.0040),
                       (120, -0.0043), (128, -0.0044)]
                far = _interp(ax, pts)

            val = main + right_bump + left_bump + far
            ys.append(val)
        except Exception:
            ys.append(None)
    return {"y": ys}


def _interp(x, pts):
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return pts[-1][1]
