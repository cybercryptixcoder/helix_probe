def predict(probe):
    # Observations:
    # - f(0) = 106.05, not 0 [E2]
    # - f is asymmetric: f(-x) != f(x) [E2]
    #   f(-88.2)=2274 vs f(88.2)=9934; f(-1)=6.85 vs f(1)=217.5
    # - For x>0, roughly quadratic-ish but with offset [E1,E2]
    # - For x<0, much smaller magnitude, also quadratic-ish [E2]
    # - Small |x|: f(-0.5)=50.3, f(0.5)=161.8, f(0)=106 -> smooth, offset ~106
    # - Looks like: y = a*x^2 + b*x + c with different behavior... 
    #   Actually try: y = A*(x - x0)^2 + c? Let's fit piecewise.
    # - Try y = alpha*x^2 + beta*x + gamma for x>=0 and x<0 separately.
    # Fit x>=0: points (0,106.05),(0.5,161.77),(1,217.48),(3,440.34),(5,663.19),
    #   (10,1220.33),(30,3448.89),(50.4,5722.01),(66,7460.29),(72.7,8206.85),(88.2,9933.99)
    # Fit x<0: (0,106.05),(-0.5,50.34),(-1,6.85),(-3,52.77),(-10,235.27),
    #   (-30,756.71),(-50.4,1288.57),(-66,1695.29),(-72.7,1869.97),(-88.2,2274.08)
    import math
    # Least squares quadratic fit helper
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
    pos=[(0,106.0528),(0.5,161.7667),(1,217.4806),(3,440.3362),(5,663.1918),
         (10,1220.3309),(30,3448.8872),(50.4,5722.0146),(66,7460.2885),
         (72.7,8206.8548),(88.2,9933.9859)]
    neg=[(0,106.0528),(-0.5,50.3388),(-1,6.8494),(-3,52.7699),(-10,235.2718),
         (-30,756.7057),(-50.4,1288.5682),(-66,1695.2867),(-72.7,1869.967),
         (-88.2,2274.0783)]
    cp,bp,ap=fit(pos)
    cn,bn,an=fit(neg)
    def predict_one(x):
        if x>=0:
            return ap*x*x+bp*x+cp
        else:
            return an*x*x+bn*x+cn
    return {"y":[predict_one(x) for x in probe["x"]]}
