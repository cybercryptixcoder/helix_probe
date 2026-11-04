def predict(probe):
    # Observations:
    # - f(0) = 106.05 [E2]
    # - Asymmetric: f(-x) != f(x) [E2]
    # - For x>=0: smooth quadratic, y = a*x^2 + b*x + c with a~0.9, b~111, c~106 [E1,E2,E3,E5,E7]
    # - For x<=-1.5: quadratic in x (far region), matches large |x| [E2,E3,E5,E7]
    # - For -1.5 < x < 0: V-shape with vertex near x=-1.1, k~6.4 [E6,E8]
    #   E8 refines: vertex is near x=-1.05 (f(-1.05)=6.4189 < f(-1.1)=6.436)
    #   Right branch (x>-1.05): slope ~100, linear [E6,E8]
    #   Left branch (-1.5<x<-1.05): slope ~22, linear [E6,E8]
    #   Breakpoints: at x=-1.5 joins quadratic; at x=0 joins positive quadratic
    #   E8 shows f(-0.95)=8.2994, f(-0.9)=10.6298 -> slope ~46 near vertex, then ~100
    #   Actually right branch is NOT purely linear: near vertex it curves up.
    #   Fit right branch as quadratic through (-1.05,6.4189),(-0.95,8.2994),(-0.9,10.6298)
    #   and check against (-0.5,50.3388),(-0.1,94.91)
    import math
    def fit(pts):
        n=len(pts)
        Sx=sum(p[0] for p in pts); Sxx=sum(p[0]**2 for p in pts)
        Sxxx=sum(p[0]**3 for p in pts); Sxxxx=sum(p[0]**4 for p in pts)
        Sy=sum(p[1] for p in pts); Sxy=sum(p[0]*p[1] for p in pts)
        Sxxy=sum(p[0]**2*p[1] for p in pts)
        A=[[n,Sx,Sxx],[Sx,Sxx,Sxxx],[Sxx,Sxxx,Sxxxx]]
        B=[Sy,Sxy,Sxxy]
        for i in range(3):
            p=A[i][i]
            for j in range(i+1,3):
                f=A[j][i]/p
                for k in range(3): A[j][k]-=f*A[i][k]
                B[j]-=f*B[i]
        sol=[0,0,0]
        for i in range(2,-1,-1):
            s=B[i]-sum(A[i][k]*sol[k] for k in range(i+1,3))
            sol[i]=s/A[i][i]
        return sol  # c,b,a
    # x>=0 quadratic
    pos=[(0,106.0528),(0.5,161.7667),(1,217.4806),(3,440.3362),(5,663.1918),
         (10,1220.3309),(30,3448.8872),(50.4,5722.0146),(66,7460.2885),
         (72.7,8206.8548),(88.2,9933.9859),(104.5,11750.2593),(123.6,13878.5306)]
    cp,bp,ap=fit(pos)
    # x<=-1.5: quadratic in x (far region)
    neg=[(-88.2,2274.0783),(-72.7,1869.967),(-66,1695.2867),(-50.4,1288.5682),
         (-30,756.7057),(-10,235.2718),(-7,157.0567),(-8,183.1284),
         (-5,104.9133),(-4,78.8416),(-3.5,65.8058),(-2.5,39.7341),(-2.0,26.6982),
         (-1.9,24.0911),(-1.8,21.4839),(-1.7,18.8767),(-1.6,16.2696),(-1.5,13.6624)]
    cn,bn,an=fit(neg)
    # V-shape region: -1.5 < x < 0
    # Vertex near x=-1.05, k~6.4189
    # Right branch: fit quadratic through right-branch points
    rpts=[(-1.05,6.4189),(-1.0,6.8494),(-0.95,8.2994),(-0.9,10.6298),
          (-0.8,18.223),(-0.7,28.0616),(-0.6,39.1961),(-0.5,50.3388),
          (-0.4,61.4816),(-0.3,72.6244),(-0.2,83.7672),(-0.1,94.91),(-0.05,100.4814)]
    cr,br,ar=fit(rpts)
    # Left branch: linear through left points
    lpts=[(-1.1,6.436),(-1.15,6.8547),(-1.2,7.4701),(-1.3,9.0565),(-1.4,11.2441),(-1.5,13.6624)]
    n=len(lpts)
    sx=sum(p[0] for p in lpts); sy=sum(p[1] for p in lpts)
    sxx=sum(p[0]*p[0] for p in lpts); sxy=sum(p[0]*p[1] for p in lpts)
    ml=(n*sxy-sx*sy)/(n*sxx-sx*sx)
    bl=(sy-ml*sx)/n
    vx=-1.05
    def predict_one(x):
        if x>=0:
            return ap*x*x+bp*x+cp
        elif x<=-1.5:
            return an*x*x+bn*x+cn
        else:
            if x>=vx:
                return ar*x*x+br*x+cr
            else:
                return ml*x+bl
    return {"y":[predict_one(x) for x in probe["x"]]}
