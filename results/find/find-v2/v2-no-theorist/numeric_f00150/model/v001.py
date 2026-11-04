def predict(probe):
    # f(x) is a degree-6 polynomial [E1, E2]
    # Fit through (0,0),(1,-0.2),(2,36),(3,913.2),(4,6364),(5,26805),(10,1992220) [E2]
    # Coefficients computed by Vandermonde solve (see below)
    coef = None
    def _fit():
        pts=[(0,0),(1,-0.2),(2,36),(3,913.2),(4,6364),(5,26805),(10,1992220)]
        n=7
        A=[[x**k for k in range(n)] for x,y in pts]
        b=[y for x,y in pts]
        M=[row[:]+[b[i]] for i,row in enumerate(A)]
        for i in range(n):
            piv=i
            for r in range(i+1,n):
                if abs(M[r][i])>abs(M[piv][i]): piv=r
            M[i],M[piv]=M[piv],M[i]
            pv=M[i][i]
            if abs(pv)<1e-12: continue
            for j in range(i,n+1): M[i][j]/=pv
            for r in range(n):
                if r!=i and abs(M[r][i])>1e-15:
                    f=M[r][i]
                    for j in range(i,n+1): M[r][j]-=f*M[i][j]
        return [M[i][n] for i in range(n)]
    try:
        coef=_fit()
    except Exception:
        coef=[0]*7
    out=[]
    for x in probe.get("x",[]):
        try:
            y=sum(coef[k]*(x**k) for k in range(7))
            out.append(y)
        except Exception:
            out.append(None)
    return {"y":out}
