import math

def predict(probe):
    # Beliefs:
    # - Output is max(g(x), floor) with floor = -20.4469 [E1, E2, E3]
    # - Floor region roughly -22 < x < 2 [E2]
    # - g is smooth, roughly quadratic-ish but not a clean parabola [E1, E2, E3]
    # - Positive side: g(5)=48.39, g(10)=650.48, g(15)=1281.06, g(30)=3458.11,
    #   g(66)=12950.84, g(72.7)=15366.07, g(88.2)=21854.21 [E1, E2, E3]
    # - Negative side: g(-22)=54.04, g(-30)=548.25, g(-55)=3783.05,
    #   g(-70)=6954.39, g(-100)=15882.92, g(-128)=24838.95 [E2]
    # - E3 shows positive side: g(65.5)=12779.96, g(79.4)=18061.83,
    #   g(103)=28232.31, g(104.5)=28878.74, g(104.9)=29051.12, g(123.6)=37109.93
    # - E3 negative: g(-55.8)=3927.93, g(-63.9)=5554.33
    # Fit g as a*x^2 + b*x + c separately per side (least squares).

    floor = -20.4469

    pos = [(5,48.3879),(10,650.4807),(15,1281.0582),(21.3,2091.9289),
           (30,3458.112),(65.5,12779.9647),(66.0,12950.8364),(72.7,15366.0691),
           (79.4,18061.8252),(88.2,21854.2087),(103.0,28232.3081),
           (104.5,28878.7371),(104.9,29051.1182),(123.6,37109.9331)]
    neg = [(-22,54.0378),(-24.3,166.2134),(-27,334.5351),(-30,548.2541),
           (-35,989.5128),(-45,2179.6225),(-50.4,2995.4039),(-55,3783.0537),
           (-55.8,3927.9297),(-61.7,5086.1272),(-63.9,5554.3344),
           (-70,6954.3912),(-80,9582.0843),(-100,15882.924),(-128,24838.9457)]

    def lsq_quad(pts):
        Sx4=Sx3=Sx2=Sx1=Sx0=0.0
        Sx2y=Sxy=Sy=0.0
        for x,y in pts:
            x2=x*x
            Sx4+=x2*x2; Sx3+=x2*x; Sx2+=x2; Sx1+=x; Sx0+=1
            Sx2y+=x2*y; Sxy+=x*y; Sy+=y
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
