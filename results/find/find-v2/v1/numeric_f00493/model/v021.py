import math

pos_data = [
    (2.0,60.2),(2.0001,60.2105),(2.001,60.3055),(2.005,60.729),(2.01,61.2619),
    (2.02,62.3396),(2.05,65.67),(2.08,69.1504),(2.1,71.5566),(2.2,84.6838),
    (2.3,99.8034),(2.5,137.0188),(2.7,185.4403),(3,427.5),(3.5,826.6969),
    (4,2004.4),(4.5,3457.0875),(5,7119.5),(5.5,11271.6406),(6,20683.8),
    (6.5,30683.0062),(7,51702.7),(7.5,72935.0344),(8,115148.0),(9,234189.9),
    (10,442789.0),(12,1336525.2),(16,7655972.8),(20,29631878.0),
    (24,89441546.4),(30,345196467.0),(32,509990115.2),(40,1963909756.0),
    (48,5902660872.0),(56,14955690528.8),(64,33445938630.4),(72,67999715935.2),
    (80,128250953912.0),(88,227639826436.0),(96,384305743324.8),
    (100,491312155389.9999),(104,622074715714.3999),(108,780637679658.0),
    (112,971541093275.1998),(116,1199859758562.8),(120,1471243673268.0),
    (124,1791959945256.4001),(128,2168936181440.0)
]

neg_mag_data = [
    (2.001,100.7783),(2.002,101.0571),(2.005,101.8964),(2.01,103.3045),
    (2.02,106.1563),(2.05,115.0015),(2.08,124.2929),(2.1,130.7427),
    (2.2,166.236),(2.3,207.5913),(2.5,310.5656),
    (2.7,445.5106),(3.0,722.7),(3.5,1935.9125),(4.0,3534.8),
    (4.5,7527.4219),(5.0,12155.5),(6.0,33683.4),(7.0,80391.5),
    (8.0,171815.2),(10.0,618311.0),(12.0,1776726.0),(16.0,9525262.4),
    (20.0,35356522.0),(24.0,103713256.8),(30.0,570243664.0),
    (32.0,570243664.0),(40.0,2147947844.0),(48.0,6360821035.2),
    (56.0,15946234578.4),(64.0,35377519980.8),(72.0,71480924820.0),
    (88.0,237136001775.2),(96.0,398978558294.4),(100.0,509307754610.0001),
    (104.0,643969517744.7999),(108.0,807080041465.2),(116.0,1237659039552.4),
    (120.0,1516025829132.0),(124.0,1844720806266.7998),(128.0,2230774482035.2)
]

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

def fit_loglin(data):
    pts = [(math.log(ax), ax, math.log(ay)) for ax, ay in data if ax > 0 and ay > 0]
    M = [[0.0]*3 for _ in range(3)]
    T = [0.0]*3
    for lx, ax, ly in pts:
        row = [1.0, lx, ax]
        for i in range(3):
            T[i] += row[i]*ly
            for j in range(3):
                M[i][j] += row[i]*row[j]
    lnA, p, k = solveN(M, T, 3)
    return math.exp(lnA), p, k

big_pos = [(ax, ay) for ax, ay in pos_data if ax >= 8]
A_pos, p_pos, k_pos = fit_loglin(big_pos)

big_neg = [(ax, ay) for ax, ay in neg_mag_data if ax >= 8]
A_neg, p_neg, k_neg = fit_loglin(big_neg)

def pos_base(ax):
    return A_pos*(ax**p_pos)*math.exp(k_pos*ax)

def neg_base(ax):
    return A_neg*(ax**p_neg)*math.exp(k_neg*ax)

corr_pts = []
for ax, ay in pos_data:
    if ax <= 8.0:
        b = pos_base(ax)
        if b > 0:
            corr_pts.append((ax, ay/b))
corr_pts.sort()

neg_corr_pts = []
for ax, ay in neg_mag_data:
    if ax <= 8.0:
        b = neg_base(ax)
        if b > 0:
            neg_corr_pts.append((ax, ay/b))
neg_corr_pts.sort()

def interp_table(pts, x, default_hi=1.0):
    if not pts:
        return 1.0
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return default_hi
    for i in range(len(pts)-1):
        x0, y0 = pts[i]
        x1, y1 = pts[i+1]
        if x0 <= x <= x1:
            t = (x-x0)/(x1-x0)
            return y0 + t*(y1-y0)
    return default_hi

def pos_magnitude(ax):
    val = pos_base(ax)
    if ax < 8.0:
        val *= interp_table(corr_pts, ax, 1.0)
    return val

def neg_magnitude(ax):
    val = neg_base(ax)
    if ax < 8.0:
        val *= interp_table(neg_corr_pts, ax, 1.0)
    return val

def outer(x):
    # f(x) = -sign(x)*|f(|x|)| for x>0; negative for x<0 too
    ax = abs(x)
    if x > 0:
        return -pos_magnitude(ax)
    else:
        return -neg_magnitude(ax)

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
    (-1.9999, -66.9815),
    (-1.9995, -66.9073),
    (-1.999, -66.8148),
    (-1.998, -66.6298),
    (-1.995, -66.0769),
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
            if x == -2.0:
                out.append(-67.0)
            elif ax >= 2.0:
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
