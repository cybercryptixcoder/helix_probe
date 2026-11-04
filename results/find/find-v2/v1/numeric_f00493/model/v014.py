import math

# Positive-side outer magnitudes (|x|, |f(x)|) from E1, E7, E10, E15, E16
outer_data = [
    (2.1,71.5566),(2.2,84.6838),(2.3,99.8034),(2.5,137.0188),
    (2.7,185.4403),(3,427.5),(3.5,826.6969),(4,2004.4),(4.5,3457.0875),
    (5,7119.5),(6,20683.8),(8,115148.0),(10,442789.0),(12,1336525.2),
    (16,7655972.8),(20,29631878.0),(24,89441546.4),(30,345196467.0),
    (32,509990115.2),(40,1963909756.0),(48,5902660872.0),(64,33445938630.4),
    (80,128250953912.0),(96,384305743324.8),(100,491312155389.9999),
    (104,622074715714.3999),(112,971541093275.1998),
    (120,1471243673268.0),(124,1791959945256.4001),
    (128,2168936181440.0)
]

# Fit log|f| = lnA + p*ln|x| + k*|x| on large-|x| points only (>=8) for asymptotic law
big = [(ax, ay) for ax, ay in outer_data if ax >= 8]
pts = [(math.log(ax), ax, math.log(ay)) for ax, ay in big]
M = [[0.0]*3 for _ in range(3)]
T = [0.0]*3
for lx, ax, ly in pts:
    row = [1.0, lx, ax]
    for i in range(3):
        T[i] += row[i]*ly
        for j in range(3):
            M[i][j] += row[i]*row[j]

def solveN(M, T, n):
    A = [M[i][:] + [T[i]] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[piv] = A[piv], A[c]
        if abs(A[c][c]) < 1e-12:
            return [0.0]*n
        for r in range(n):
            if r != c:
                f = A[r][c]/A[c][c]
                for kk in range(c, n+1):
                    A[r][kk] -= f*A[c][kk]
    return [A[i][n]/A[i][i] for i in range(n)]

coef = solveN(M, T, 3)
lnA, p, k = coef
A = math.exp(lnA)

def outer_base(ax):
    return A*(ax**p)*math.exp(k*ax)

# Positive-side near-boundary correction ratio = observed / outer_base
corr_pts = []
for ax, ay in outer_data:
    if ax <= 4.5:
        b = outer_base(ax)
        if b > 0:
            corr_pts.append((ax, ay/b))

def corr_factor(ax):
    if ax <= corr_pts[0][0]:
        return corr_pts[0][1]
    if ax >= corr_pts[-1][0]:
        return 1.0
    for i in range(len(corr_pts)-1):
        x0, y0 = corr_pts[i]
        x1, y1 = corr_pts[i+1]
        if x0 <= ax <= x1:
            t = (ax-x0)/(x1-x0)
            return y0 + t*(y1-y0)
    return 1.0

def pos_magnitude(ax):
    val = outer_base(ax)
    if ax < 4.5:
        val *= corr_factor(ax)
    return val

# Negative-side ratio r(ax) = |f(-ax)| / |f(ax)|, from E10/E14/E16
# At 2.5: 310.5656/137.0188=2.267; 3:722.7/427.5=1.691; 4:3534.8/2004.4=1.763;
# 5:12155.5/7119.5=1.707; 6:33683.4/20683.8=1.629; 8:171815.2/115148=1.492;
# 10:618311/442789=1.396; 12:1776726/1336525=1.329; 16:9525262.4/7655972.8=1.244;
# 20:35356522/29631878=1.193; 24:103713256.8/89441546.4=1.160; 30:570243664/345196467=1.652?? 
# Note E16 shows 32:570243664/509990115.2=1.118; 48:6360821035.2/5902660872=1.078;
# 64:35377519980.8/33445938630.4=1.058; 96:398978558294.4/384305743324.8=1.038;
# 128:2230774482035.2/2168936181440=1.028
ratio_pts = [
    (2.5, 2.267),(3.0, 1.691),(4.0, 1.763),(5.0, 1.707),(6.0, 1.629),
    (8.0, 1.492),(10.0, 1.396),(12.0, 1.329),(16.0, 1.244),
    (20.0, 1.193),(24.0, 1.160),(32.0, 1.118),(48.0, 1.078),
    (64.0, 1.058),(96.0, 1.038),(128.0, 1.028)
]

def neg_ratio(ax):
    if ax <= ratio_pts[0][0]:
        return ratio_pts[0][1]
    if ax >= ratio_pts[-1][0]:
        return ratio_pts[-1][1]
    for i in range(len(ratio_pts)-1):
        x0, y0 = ratio_pts[i]
        x1, y1 = ratio_pts[i+1]
        if x0 <= ax <= x1:
            t = (ax-x0)/(x1-x0)
            return y0 + t*(y1-y0)
    return 1.0

def outer(x):
    ax = abs(x)
    m = pos_magnitude(ax)
    if x < 0:
        m *= neg_ratio(ax)
        return m
    else:
        return -m

pos_pts = [
    (1.0, -4.3),
    (1.001, -4.3081),
    (1.002, -4.3162),
    (1.005, -4.3408),
    (1.01, -4.3821),
    (1.02, -4.4665),
    (1.05, -4.7333),
    (1.1, -5.2257),
    (1.15, -5.7808),
    (1.2, -6.4027),
    (1.25, -7.0958),
    (1.3, -7.8647),
    (1.35, -8.7143),
    (1.4, -9.6501),
    (1.45, -10.6776),
    (1.5, -11.8031),
    (1.55, -13.033),
    (1.6, -14.3742),
    (1.65, -15.8342),
    (1.7, -17.4207),
    (1.75, -19.1421),
    (1.8, -21.0072),
    (1.85, -23.0254),
    (1.9, -25.2065),
    (1.95, -27.561),
    (1.97, -28.5539),
    (1.98, -29.0616),
    (1.985, -29.3183),
    (1.99, -29.5769),
    (1.995, -29.8375),
    (1.999, -30.0473),
    (1.9995, -30.0737),
    (1.9999, -30.0947),
]

neg_pts = [
    (-2.0, -67.0),
    (-1.99, -65.1615),
    (-1.98, -63.3539),
    (-1.97, -61.5768),
    (-1.96, -59.8298),
    (-1.95, -58.1125),
    (-1.94, -56.4247),
    (-1.93, -54.7659),
    (-1.92, -53.1359),
    (-1.91, -51.5342),
    (-1.9, -49.9606),
    (-1.85, -42.5014),
    (-1.8, -35.6938),
    (-1.75, -29.4982),
    (-1.7, -23.8769),
    (-1.6, -14.2134),
    (-1.5, -6.4313),
    (-1.45, -3.1671),
    (-1.42, -1.3923),
    (-1.4, -0.2819),
    (-1.2, 8.0016),
    (-0.9, 6.5864),
    (-0.7, 6.7646),
    (-0.4, 5.8254),
    (-0.2, 4.8616),
    (-0.1, 4.3688),
    (0.0, 0.0),
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
            if x1 == x0:
                return y0
            t = (x-x0)/(x1-x0)
            return y0 + t*(y1-y0)
    return pts[-1][1]

def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            ax = abs(x)
            if ax >= 2.0:
                if x == 2.0:
                    out.append(-60.2)
                elif x == -2.0:
                    out.append(-67.0)
                else:
                    out.append(outer(x))
            elif x >= 1.0:
                out.append(interp(pos_pts, x))
            elif x >= 0.0:
                out.append(0.0)
            else:
                out.append(interp(neg_pts, x))
        except Exception:
            out.append(None)
    return {"y": out}
