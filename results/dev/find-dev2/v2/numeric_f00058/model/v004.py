import math

# Beliefs:
# - The box is f(x) = g(|x|) for |x| above a threshold, and a constant -84.3663 near 0.
# - Dead zone: |x| < ~32 gives -84.3663 [E1, E3, E4, E7, E9].
# - Just outside the dead zone (|x| ~ 32 to ~48) still -84.3663 [E2, E4, E5, E6, E8].
# - At |x| ~ 48-50 it starts rising; below ~48 flat [E8, E10, E11, E12].
# - From ~50 upward, g grows roughly like a smooth increasing convex function of |x|,
#   symmetric in sign; values at 64, 96, 120, 128 match a power-ish curve [E1, E2, E11].
# - The curve looks like ~ (|x|-48)^p scaled, but the exact shape is approximated by an MLP;
#   I'll fit a smooth monotone function through the observed positive-side points.
# - Negative side mirrors positive side exactly [E1, E2, E11].
# - Output is deterministic (repeated values identical) [E10 vs E12].

# Fit data on positive side (|x| >= 50), from evidence:
# x -> y
_pts = [
    (50, 0.0),          # boundary, y ~ -84.3663 just below; treat onset near 50
    (51, 12.4118),
    (51.25, 116.3204),
    (51.5, 220.2289),
    (52, 428.046),
    (52.5, 635.8631),
    (53, 843.6803),
    (54, 1259.3145),
    (55, 1674.9487),
    (56, 2090.5829),
    (57, 3230.3677),
    (58, 4433.2432),
    (59, 5636.1187),
    (60, 6838.9942),
    (61, 8041.8696),
    (62, 10136.592),
    (63, 13053.9381),
    (64, 15971.2842),
    (65, 18888.6303),
    (66, 21805.9764),
    (68, 28208.669),
    (70, 35110.0497),
    (72, 42011.4303),
    (74, 49565.7195),
    (76, 57288.6179),
    (78, 65011.5164),
    (80, 72734.4149),
    (82, 80457.3134),
    (84, 88180.2118),
    (96, 134517.6027),
    (100, 149963.3997),
    (104, 220877.4),   # wait check: E2 has 104->220877.4? yes
    (112, 256101.5362),
    (120, 291325.6723),
    (128, 258083.9783), # hmm 128 lower than 120? E1: 120->227192.3844, 128->258083.9783
]
# Correction: E1 values: 96->134517.6027, 120->227192.3844, 128->258083.9783
# E2: 104->220877.4, 112->256101.5362, 120->291325.6723 (conflict with E1's 120!)
# E1 120 = 227192.3844, E2 120 = 291325.6723 -> contradiction!
# Re-read: E1 x list ends ...64,96,120,128 -> y ...15971,134517,227192,258083
# E2 x list: -120,-112,-104,-100,-80,-72,-48,-40,-36,-34,-33,33,34,36,40,48,72,80,100,112
#   y: 291325,256101,220877,203265,115204,79980,-84,-84,-84,-84,-84,-84,-84,-84,-84,-84,42011,72734,149963,196300
# So E2's 112 -> 196300.7905 (not 256101). 100->149963.3997, 80->72734.4149, 72->42011.4303.
# E2 negative: -120->291325.6723, -112->256101.5362, -104->220877.4, -100->203265.332,
#   -80->115204.9916, -72->79980.8555.
# E1: -128->326549.8085, -96->185653.2639, -64->44756.7193, 64->15971.2842, 96->134517.6027,
#   120->227192.3844, 128->258083.9783.
# So positive 120->227192, 128->258083; negative -120->291325, -128->326549.
# NOT symmetric! Negative side is larger in magnitude.

# Let's tabulate properly.
_pos = {
    51:12.4118, 51.25:116.3204, 51.5:220.2289, 52:428.046, 52.5:635.8631, 53:843.6803,
    54:1259.3145, 55:1674.9487, 56:2090.5829, 57:3230.3677, 58:4433.2432, 59:5636.1187,
    60:6838.9942, 61:8041.8696, 62:10136.592, 63:13053.9381, 64:15971.2842, 65:18888.6303,
    66:21805.9764, 68:28208.669, 70:35110.0497, 72:42011.4303, 74:49565.7195, 76:57288.6179,
    78:65011.5164, 80:72734.4149, 82:80457.3134, 84:88180.2118, 96:134517.6027,
    100:149963.3997, 120:227192.3844, 128:258083.9783,
}
_neg = {
    51.5:547.3193, 52.5:3160.5633, 53:4467.1854, 54:7080.4295, 55:9693.6736, 57:15637.21,
    58:19684.5999, 60:27779.3796, 62:35950.6853, 66:53562.7534, 72:79980.8555,
    80:115204.9916, 100:203265.332, 104:220877.4, 112:256101.5362, 120:291325.6723,
    128:326549.8085,
}

# Looks like negative side is shifted: g(-a) ~ g(a + delta) with delta ~ 4? 
# Check: neg 120 = 291325, pos 128 = 258083 (not equal). neg 104=220877, pos 96=134517.
# Try neg(a) vs pos(a+8)? neg 120 vs pos 128: 291325 vs 258083 no.
# Try neg(a) vs pos(a*1.1)? neg 120 vs pos 132 (extrapolate ~ 265000) no.
# Maybe negative side is steeper. Let's just interpolate each side separately.

def _interp(table, x):
    xs = sorted(table.keys())
    if x <= xs[0]:
        # extrapolate linearly from first two
        if len(xs) < 2:
            return table[xs[0]]
        x0, x1 = xs[0], xs[1]
        y0, y1 = table[x0], table[x1]
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    if x >= xs[-1]:
        x0, x1 = xs[-2], xs[-1]
        y0, y1 = table[x0], table[x1]
        return y1 + (y1 - y0) * (x - x1) / (x1 - x0)
    # find bracket
    lo, hi = 0, len(xs) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if xs[mid] <= x:
            lo = mid
        else:
            hi = mid
    x0, x1 = xs[lo], xs[hi]
    y0, y1 = table[x0], table[x1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

DEAD = -84.3663
ONSET = 50.0  # below this, dead zone

def predict(probe):
    try:
        xs = probe["x"]
        out = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                out.append(None)
                continue
            ax = abs(x)
            if ax < ONSET:
                out.append(DEAD)
            else:
                # onset: at exactly 50, value ~ -84.3663 (E12 49.5 dead, 50 dead, 51 tiny)
                if ax < 50.5:
                    # blend from dead to first point
                    if ax <= 50.0:
                        out.append(DEAD)
                    else:
                        t = (ax - 50.0) / 0.5
                        out.append(DEAD + t * (12.4118 - DEAD))
                elif x > 0:
                    out.append(_interp(_pos, ax))
                else:
                    out.append(_interp(_neg, ax))
        return {"y": out}
    except Exception:
        return {"y": []}
