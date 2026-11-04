import math

# Data from E1 and E2
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

# Fit ln|y| = lnA + p*ln|x| + k*|x| using |x|>=2 (odd region)
pts = [(math.log(abs(x)), abs(x), math.log(abs(y))) for x,y in data if abs(x)>=2 and y!=0]
M=[[0.0]*3 for _ in range(3)]
T=[0.0]*3
for lx,ax,ly in pts:
    row=[1.0,lx,ax]
    for i in range(3):
        T[i]+=row[i]*ly
        for j in range(3):
            M[i][j]+=row[i]*row[j]

def solve3(M,T):
    A=[row[:]+[T[i]] for i,row in enumerate(M)]
    for c in range(3):
        piv=max(range(c,3),key=lambda r:abs(A[r][c]))
        A[c],A[piv]=A[piv],A[c]
        if abs(A[c][c])<1e-12: return [0.0,0.0,0.0]
        for r in range(3):
            if r!=c:
                f=A[r][c]/A[c][c]
                for k in range(c,4): A[r][k]-=f*A[c][k]
    return [A[i][3]/A[i][i] for i in range(3)]

coef=solve3(M,T)
lnA,p,k=coef
A=math.exp(lnA)

# Inner interval |x|<2: fit a polynomial to the small-x data
# Points: (-1.5,-6.4313),(-1,6.1),(-0.5,6.2406),(0,0),(0.5,-0.0),(1,-4.3),(1.5,-11.8031)
inner = [(-1.5,-6.4313),(-1,6.1),(-0.5,6.2406),(0,0.0),(0.5,-0.0),(1,-4.3),(1.5,-11.8031)]
# Fit cubic a*x^3+b*x^2+c*x+d
Mi=[[0.0]*4 for _ in range(4)]
Ti=[0.0]*4
for x,y in inner:
    row=[x**3,x**2,x,1.0]
    for i in range(4):
        Ti[i]+=row[i]*y
        for j in range(4):
            Mi[i][j]+=row[i]*row[j]

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

ic=solveN(Mi,Ti,4)  # [a3,a2,a1,a0]

def predict(probe):
    xs = probe.get("x", [])
    out=[]
    for x in xs:
        try:
            if x is None:
                out.append(None); continue
            x=float(x)
            ax=abs(x)
            if ax < 2.0:
                a3,a2,a1,a0=ic
                v=a3*x**3+a2*x**2+a1*x+a0
                out.append(v)
            elif x==0:
                out.append(0.0)
            else:
                val=A*(ax**p)*math.exp(k*ax)
                out.append(math.copysign(val,x))
        except Exception:
            out.append(None)
    return {"y":out}
