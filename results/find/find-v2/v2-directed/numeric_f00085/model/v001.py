import math

def predict(probe):
    # Observations from E1:
    # - For x <= -8: y is large positive and grows with |x| (roughly quadratic-ish).
    # - For -8 < x < 8 (specifically -4..4 sampled): y is constant -22.8021.
    # - At x=8: y=132.19, x=16: 857.05, x=64: 14110.97, x=128: 50592.64.
    # - Symmetric-looking: f(-128)=51222.6 ~ f(128)=50592.6; f(-16)=1012.6 ~ f(16)=857.0.
    # Hypothesis: f(x) = g(|x|) where g is ~quadratic for |x|>=8, and a flat plateau
    # -22.8021 for |x| < 8 (a "dead zone" / clamp region).
    # Fit quadratic a*x^2 + b*x + c on outer points.
    # Use points: (8,132.1905),(16,857.0481),(64,14110.9665),(128,50592.6368)
    # Solve least squares roughly.
    pts = [(8,132.1905),(16,857.0481),(64,14110.9665),(128,50592.6368)]
    # Fit y = a*x^2 + b*x + c
    # Normal equations
    S0=len(pts); S1=sum(p[0] for p in pts); S2=sum(p[0]**2 for p in pts)
    S3=sum(p[0]**3 for p in pts); S4=sum(p[0]**4 for p in pts)
    T0=sum(p[1] for p in pts); T1=sum(p[0]*p[1] for p in pts); T2=sum(p[0]**2*p[1] for p in pts)
    # matrix [[S4,S3,S2],[S3,S2,S1],[S2,S1,S0]] [a,b,c] = [T2,T1,T0]
    import itertools
    M=[[S4,S3,S2],[S3,S2,S1],[S2,S1,S0]]
    V=[T2,T1,T0]
    # Gaussian elimination
    def solve(M,V):
        n=3
        A=[row[:]+[V[i]] for i,row in enumerate(M)]
        for i in range(n):
            piv=i
            for r in range(i+1,n):
                if abs(A[r][i])>abs(A[piv][i]): piv=r
            A[i],A[piv]=A[piv],A[i]
            if abs(A[i][i])<1e-12: return None
            for r in range(i+1,n):
                f=A[r][i]/A[i][i]
                for c in range(i,n+1): A[r][c]-=f*A[i][c]
        x=[0]*n
        for i in range(n-1,-1,-1):
            s=A[i][n]-sum(A[i][j]*x[j] for j in range(i+1,n))
            x[i]=s/A[i][i]
        return x
    sol=solve(M,V)
    if sol is None:
        a,b,c=3.0,0.0,-100.0
    else:
        a,b,c=sol
    def outer(x):
        return a*x*x+b*x+c
    out=[]
    for xv in probe.get("x",[]):
        try:
            xv=float(xv)
        except Exception:
            out.append(None); continue
        ax=abs(xv)
        if ax<8.0:
            out.append(-22.8021)
        else:
            out.append(outer(ax))
    return {"y":out}
