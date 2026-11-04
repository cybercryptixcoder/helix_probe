import math

# Outer branch data: (|x|, |f(x)|) from E1, E2, E7, E8, E10
outer_data = [
    (2.5,137.0188),(3,427.5),(4,2004.4),(5,7119.5),(6,20683.8),
    (8,115148.0),(10,442789.0),(12,1336525.2),(16,7655972.8),
    (20,29631878.0),(24,89441546.4),(30,345196467.0),(32,570243664.0),
    (40,1963909756.0),(48,5902660872.0),(64,33445938630.4),
    (80,128250953912.0),(96,384305743324.8),(100,491312155389.9999),
    (104,622074715714.3999),(112,971541093275.1998),
    (120,1471243673268.0),(124,1791959945256.4001),
    (128,2168936181440.0)
]

# Fit log|y| = lnA + p*ln|x| + k*|x|  (linear least squares in 3 params)
pts = [(math.log(ax), ax, math.log(ay)) for ax, ay in outer_data]
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

def outer(x):
    ax = abs(x)
    val = A*(ax**p)*math.exp(k*ax)
    return math.copysign(val, x)

# Positive inner side (1,2): smooth ramp from -4.3 at x=1 to ~-30 as x->2-
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
                # pin exact boundary values
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
