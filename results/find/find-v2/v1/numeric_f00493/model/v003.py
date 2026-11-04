import math

# Outer power-law fit data (|x|>=2)
data = [
    (-128,-2230774482035.2),(-112,-1003257061016.0),(-96,-398978558294.4),
    (-80,-134146940488.0),(-64,-35377519980.8),(-48,-6360821035.2),
    (-32,-570243664.0),(-24,-89441546.4),(-20,-29631878.0),(-16,-9525262.4),
    (-12,-1336525.2),(-10,-442789.0),(-8,-171815.2),(-6,-20683.8),
    (-5,-7119.5),(-4,-3534.8),(-3,-722.7),(-2.5,-310.5656),(-2,-67.0),
    (-1.5,-6.4313),(-1,6.1),(-0.5,6.2406),(0,0.0),
    (0.5,-0.0),(1,-4.3),(1.5,-11.8031),(2,-60.2),(2.5,-137.0188),
    (3,-427.5),(5,-7119.5),(6,-20683.8),(8,-115148.0),(10,-442789.0),
    (12,-1336525.2),(16,-7655972.8),(20,-29631878.0),(24,-89441546.4),
    (32,-570243664.0),(40,-1963909756.0),(48,-5902660872.0),
    (64,-33445938630.4),(128,-2168936181440.0)
]

pts = [(math.log(abs(x)), abs(x), math.log(abs(y))) for x,y in data if abs(x)>=2 and y!=0]
M=[[0.0]*3 for _ in range(3)]
T=[0.0]*3
for lx,ax,ly in pts:
    row=[1.0,lx,ax]
    for i in range(3):
        T[i]+=row[i]*ly
        for j in range(3):
            M[i][j]+=row[i]*row[j]

def solveN(M,T,n):
    A=[M[i][:]+[T[i]] for i in range(n)]
    for c in range(n):
        piv=max(range(c,n),key=lambda r:abs(A[r][c]))
        A[c],A[piv]=A[piv],A[c]
        if abs(A[c][c])<1e-12: return [0.0]*n
        for r in range(n):
            if r!=c:
                f=A[r][c]/A[c][c]
                for kk in range(c,n+1): A[r][kk]-=f*A[c][kk]
    return [A[i][n]/A[i][i] for i in range(n)]

coef=solveN(M,T,3)
lnA,p,k=coef
A=math.exp(lnA)

def outer(x):
    ax=abs(x)
    val=A*(ax**p)*math.exp(k*ax)
    return math.copysign(val,x)

# Inner region: piecewise-linear interpolation through observed points.
# Positive side (0,2): exactly 0 until 0.9, then rises to ~-30 near 2.
pos_pts = [
    (0.0, 0.0),
    (0.9, 0.0),
    (1.2, -6.4027),
    (1.4, -9.6501),
    (1.7, -17.4207),
    (1.9, -25.2065),
    (1.99, -29.5769),
    (1.999, -30.0473),
    (2.0, -60.2),
]
# Negative side (-2,0): f(-x) not equal -f(x); use observed values.
neg_pts = [
    (-2.0, -67.0),
    (-1.9, -49.9606),
    (-1.7, -23.8769),
    (-1.5, -6.4313),
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
        x0,y0=pts[i]; x1,y1=pts[i+1]
        if x0 <= x <= x1:
            if x1==x0: return y0
            t=(x-x0)/(x1-x0)
            return y0+t*(y1-y0)
    return pts[-1][1]

def predict(probe):
    xs = probe.get("x", [])
    out=[]
    for x in xs:
        try:
            if x is None:
                out.append(None); continue
            x=float(x)
            ax=abs(x)
            if ax >= 2.0:
                out.append(outer(x))
            elif x >= 0:
                out.append(interp(pos_pts, x))
            else:
                out.append(interp(neg_pts, x))
        except Exception:
            out.append(None)
    return {"y":out}
