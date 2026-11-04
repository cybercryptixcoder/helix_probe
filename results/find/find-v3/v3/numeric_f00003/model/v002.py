import math

def predict(probe):
    # Observations:
    # - For x <= ~-22: smooth curve, roughly quadratic-ish but not a clean parabola [E1, E2]
    # - For -22 < x < ~2: constant floor = -20.4469 [E1, E2]
    # - For x >= ~2: smooth curve, roughly quadratic [E1, E2]
    # - The two branches are NOT the same quadratic (E1's fit failed badly on E2) [E2]
    # - At x=30 -> 3458.112, x=15 -> 1281.0582, x=10 -> 650.4807, x=5 -> 48.3879
    #   These don't fit a single quadratic through origin either; looks like
    #   something like a*x^2 + b*x + c with small c, or maybe |x|^p.
    # - Negative side: x=-22 -> 54.0378, x=-27 -> 334.5351, x=-30 -> 548.2541,
    #   x=-35 -> 989.5128, x=-45 -> 2179.6225, x=-55 -> 3783.0537,
    #   x=-70 -> 6954.3912, x=-80 -> 9582.0843, x=-100 -> 15882.924, x=-128 -> 24838.9457
    # Hypothesis: y = max(g(x), floor) where floor = -20.4469, and g is a smooth
    # function. Fit g separately on positive and negative sides using the data.
    # The floor region is roughly -22 < x < 2 (where g < floor).
    # Let's fit g(x) = a*x^2 + b*x + c on each side by least squares.

    floor = -20.4469

    # Positive side data (x>0, y>floor):
    pos = [(5,48.3879),(10,650.4807),(15,1281.0582),(21.3,2091.9289),
           (30,3458.112),(66.0,12950.8364),(72.7,15366.0691),(88.2,21854.2087)]
    # Negative side data (x<0, y>floor):
    neg = [(-22,54.0378),(-24.3,166.2134),(-27,334.5351),(-30,548.2541),
           (-35,989.5128),(-45,2179.6225),(-50.4,2995.4039),(-55,3783.0537),
           (-61.7,5086.1272),(-70,6954.3912),(-80,9582.0843),(-100,15882.924),
           (-128,24838.9457)]

    def lsq_quad(pts):
        # fit y = a x^2 + b x + c
        n = len(pts)
        Sx4=Sx3=Sx2=Sx1=Sx0=0.0
        Sx2y=Sxy=Sy=0.0
        for x,y in pts:
            x2=x*x
            Sx4+=x2*x2; Sx3+=x2*x; Sx2+=x2; Sx1+=x; Sx0+=1
            Sx2y+=x2*y; Sxy+=x*y; Sy+=y
        # normal equations
        A=[[Sx4,Sx3,Sx2],[Sx3,Sx2,Sx1],[Sx2,Sx1,Sx0]]
        b=[Sx2y,Sxy,Sy]
        M=[A[i][:]+[b[i]] for i in range(3)]
        for i in range(3):
            piv=M[i][i]
            if abs(piv)<1e-12:
                for j in range(i+1,3):
                    if abs(M[j][i])>1e-12:
                        M[i],M[j]=M[j],M[i]; piv=M[i][i]; break
            for j in range(i+1,3):
                f=M[j][i]/piv
                for k in range(i,4):
                    M[j][k]-=f*M[i][k]
        sol=[0,0,0]
        for i in range(2,-1,-1):
            s=M[i][3]
            for k in range(i+1,3):
                s-=M[i][k]*sol[k]
            sol[i]=s/M[i][i]
        return sol

    ap,bp,cp = lsq_quad(pos)
    an,bn,cn = lsq_quad(neg)

    def g(x):
        if x >= 0:
            return ap*x*x + bp*x + cp
        else:
            return an*x*x + bn*x + cn

    def f(x):
        return max(g(x), floor)

    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
