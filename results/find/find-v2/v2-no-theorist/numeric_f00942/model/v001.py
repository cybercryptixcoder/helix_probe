def predict(probe):
    # f(x) looks like a cubic-ish / polynomial: y grows fast with |x| and sign follows x
    # Check: x=88.2 -> -35805 (negative!), x=66 -> -26832 (negative), x=-20.3 -> +708 (positive)
    # So sign is OPPOSITE to x for large |x|. Looks like y ≈ -a*x^3 + b*x^2 ... let's fit.
    # x=88.2: -35805.24 ; x^3=686128 ; -35805/686128 ≈ -0.0522
    # x=66: -26832 ; 66^3=287496 ; -26832/287496 ≈ -0.0933  (not pure cubic)
    # x=72.7: -29540 ; 72.7^3=384240 ; -29540/384240 ≈ -0.0769
    # x=-61.7: +2186.8 ; -61.7^3=-234885 ; 2186.8/-234885 ≈ -0.0093 (small)
    # Hmm not clean cubic. Try quadratic: x=88.2, x^2=7779 -> -35805/7779=-4.6
    # x=66, x^2=4356 -> -26832/4356=-6.16
    # Try y = a*x^2 + b*x + c with sign flip... let's just fit a cubic through points.
    # Use three points to solve cubic a*x^3+b*x^2+c*x+d.
    # Points: (88.2,-35805.24),(66,-26832),(-20.3,708.016)
    # Also (2.9,-1326.98) small x gives large negative -> constant term negative?
    # At x=2.9, y=-1326.98. At x=-6, y=197.22. At x=21.3, y=-8764.26.
    # Try y = -a*x^3 + ... Let's guess y = -x^3/... no.
    # Let's try y = a*x^3 + b*x^2 + c*x + d via least squares mentally is hard.
    # Alternative: y = -k*x^2*sign(x)? x=88.2: -k*7779=-35805 -> k=4.6; x=66:-k*4356=-26832->k=6.16 no.
    # Try y = a*x^3 with a varying... 
    # Look: x=2.9 -> -1326.98. x^3=24.4. ratio -54. x=-6->197.22, x^3=-216, ratio -0.91.
    # Maybe y = -x^3/... plus something. Let's fit cubic exactly with 4 points.
    # (2.9,-1326.98),(66,-26832),(88.2,-35805.24),(-20.3,708.016)
    # Solve: a*2.9^3+b*2.9^2+c*2.9+d=-1326.98
    # a*66^3+b*66^2+c*66+d=-26832
    # a*88.2^3+b*88.2^2+c*88.2+d=-35805.24
    # a*(-20.3)^3+b*(-20.3)^2+c*(-20.3)+d=708.016
    # This is getting complex; let me just implement a cubic fit numerically at runtime.
    import math
    pts = [(88.2,-35805.24),(66.0,-26832.0),(-20.3,708.016),(-61.7,2186.824),
           (2.9,-1326.98),(-24.3,850.896),(72.7,-29540.14),(-50.4,1783.188),
           (-6.0,197.22),(21.3,-8764.26)]
    # Fit cubic via normal equations
    n=len(pts)
    # basis [x^3,x^2,x,1]
    import itertools
    def solve(A,b):
        m=len(A)
        M=[row[:]+[b[i]] for i,row in enumerate(A)]
        for col in range(m):
            piv=col
            for r in range(col,m):
                if abs(M[r][col])>abs(M[piv][col]): piv=r
            M[col],M[piv]=M[piv],M[col]
            if abs(M[col][col])<1e-12: continue
            for r in range(m):
                if r!=col:
                    f=M[r][col]/M[col][col]
                    for cc in range(col,m+1):
                        M[r][cc]-=f*M[col][cc]
        return [M[i][m]/M[i][i] if abs(M[i][i])>1e-12 else 0 for i in range(m)]
    # normal equations for cubic
    def basis(x): return [x**3,x**2,x,1.0]
    ATA=[[0.0]*4 for _ in range(4)]
    ATb=[0.0]*4
    for x,y in pts:
        bv=basis(x)
        for i in range(4):
            ATb[i]+=bv[i]*y
            for j in range(4):
                ATA[i][j]+=bv[i]*bv[j]
    coef=solve(ATA,ATb)
    def f(x):
        return coef[0]*x**3+coef[1]*x**2+coef[2]*x+coef[3]
    return {"y":[f(x) for x in probe["x"]]}
