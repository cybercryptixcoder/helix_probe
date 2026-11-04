def predict(probe):
    # Observations:
    # - f(0) = 106.05 [E2]
    # - Asymmetric: f(-x) != f(x) [E2]
    # - For x>=0: smooth quadratic, y = a*x^2 + b*x + c with a~0.9, b~111, c~106 [E1,E2,E3,E5]
    # - For x<=-1.5: quadratic in x (far region), matches large |x| [E2,E3,E5]
    # - For -1.5 < x < 0: NOT quadratic. E6 shows a sharp V with vertex near x=-1.1:
    #   f(-1.1)=6.436 min, rising steeply toward 0: f(-0.05)=100.48, f(-0.5)=50.34, f(-1.0)=6.85
    #   and rising toward -1.5: f(-1.5)=13.66, f(-1.9)=24.09
    #   Slope from -1.0 to -0.05: ~(100.48-6.85)/0.95 ~ 98.6 per unit (linear!)
    #   Check: f(-0.5)-f(-1.0)=43.49 over 0.5 -> 87; f(-0.05)-f(-0.5)=50.14 over 0.45 -> 111
    #   Roughly linear on the right branch. Left branch: f(-1.5)-f(-1.1)=7.23 over 0.4 -> 18
    #   f(-1.9)-f(-1.5)=10.43 over 0.4 -> 26. So V with vertex ~-1.1, left slope ~22, right slope ~100
    # - For -1.5 < x < 0: V-shape, y = m*|x - v| + k, v~-1.1, k~6.4
    #   Right branch (x>-1.1): slope ~100; left branch (x<-1.1): slope ~22
    # - For x < -1.5: quadratic in x [E2,E3,E5]
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
         (-5,104.9133),(-4,78.8416),(-3.5,65.8058),(-2.5,39.7341),(-2,26.6982),
         (-1.9,24.0911),(-1.8,21.4839),(-1.7,18.8767),(-1.6,16.2696),(-1.5,13.6624)]
    cn,bn,an=fit(neg)
    # V-shape region: -1.5 < x < 0
    # vertex v, k; left slope ml (for x<v), right slope mr (for x>v)
    # Use E6 points: fit V with vertex near -1.1
    # Right branch points (x > -1.1): (-1.0,6.8494),(-0.9,10.6298),(-0.8,18.223),
    #   (-0.7,28.0616),(-0.6,39.1961),(-0.5,50.3388),(-0.4,61.4816),(-0.3,72.6244),
    #   (-0.2,83.7672),(-0.1,94.91),(-0.05,100.4814)
    # Left branch points (x < -1.1): (-1.2,7.4701),(-1.3,9.0565),(-1.4,11.2441),(-1.5,13.6624)
    # Fit right branch: y = mr*x + br
    rpts=[(-1.0,6.8494),(-0.9,10.6298),(-0.8,18.223),(-0.7,28.0616),(-0.6,39.1961),
          (-0.5,50.3388),(-0.4,61.4816),(-0.3,72.6244),(-0.2,83.7672),(-0.1,94.91),(-0.05,100.4814)]
    n=len(rpts)
    sx=sum(p[0] for p in rpts); sy=sum(p[1] for p in rpts)
    sxx=sum(p[0]*p[0] for p in rpts); sxy=sum(p[0]*p[1] for p in rpts)
    mr=(n*sxy-sx*sy)/(n*sxx-sx*sx)
    br=(sy-mr*sx)/n
    # Left branch: y = ml*x + bl
    lpts=[(-1.2,7.4701),(-1.3,9.0565),(-1.4,11.2441),(-1.5,13.6624)]
    n=len(lpts)
    sx=sum(p[0] for p in lpts); sy=sum(p[1] for p in lpts)
    sxx=sum(p[0]*p[0] for p in lpts); sxy=sum(p[0]*p[1] for p in lpts)
    ml=(n*sxy-sx*sy)/(n*sxx-sx*sx)
    bl=(sy-ml*sx)/n
    # Vertex: intersection of the two lines
    vx=(bl-br)/(mr-ml)
    def predict_one(x):
        if x>=0:
            return ap*x*x+bp*x+cp
        elif x<=-1.5:
            return an*x*x+bn*x+cn
        else:
            # V-shape region
            if x>=vx:
                return mr*x+br
            else:
                return ml*x+bl
    return {"y":[predict_one(x) for x in probe["x"]]}
