def predict(probe):
    # Observations:
    # - f(0) = 106.05 [E2]
    # - Asymmetric: f(-x) != f(x) [E2]
    # - For x>=0: smooth quadratic-ish, y ~ a*x^2 + b*x + c [E1,E2,E3]
    # - For x<0: NOT quadratic. Values: f(-0.25)=78.2, f(-0.75)=22.9, f(-1.5)=13.7,
    #   f(-2)=26.7, f(-2.5)=39.7, f(-3.5)=65.8, f(-4)=78.8, f(-5)=104.9 [E4]
    #   This looks like a V-shape / |x| behavior: minimum near x=-1.5, rising both ways.
    #   Check: f(-1.5)=13.66, f(-0.75)=22.88, f(-0.25)=78.2 (rises toward 0)
    #          f(-2)=26.7, f(-3.5)=65.8, f(-5)=104.9 (rises away)
    #   So for x<0: y ~ A*|x - x0| + c with x0 ~ -1.5? Let's check linear in |x+1.5|:
    #   f(-0.25): |1.25|*k+c, f(-0.75): |0.75|*k+c, f(-2): |0.5|*k+c, f(-3.5):|2|*k+c
    #   From -0.25 and -0.75: (78.2-22.9)/(1.25-0.75)=110.6 per unit
    #   From -2 and -3.5: (65.8-26.7)/(2-0.5)=26.1 per unit -- not linear.
    #   Hmm. Try quadratic in (x+1.5)? f(-1.5)=13.66 min.
    #   Points relative to -1.5: d=0:13.66, d=0.75:22.88, d=1.25:78.2, d=0.5:26.7,
    #   d=1:39.7, d=2:65.8, d=2.5:78.8, d=3.5:104.9
    #   d=0.5->26.7, d=0.75->22.88 (decreasing!), d=1->39.7. Noisy/nonmonotone.
    #   Actually maybe x<0 is quadratic with a different vertex. Fit quad to x<0 pts.
    # - Large |x|: for x<0, y grows ~quadratically (f(-88.2)=2274) [E2]
    #   For x<0 small, V-shape near -1.5. So x<0 is piecewise: V near zero, quad far.
    # - Actually reconsider: maybe x<0 is quadratic with vertex at some x0<0.
    #   Fit quad through (-88.2,2274),(-50.4,1288.6),(-30,756.7),(-10,235.3):
    #   Let's just fit a quadratic to all x<0 points and see residuals.
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
    # x>=0 quadratic (well constrained, matches E1,E2,E3)
    pos=[(0,106.0528),(0.5,161.7667),(1,217.4806),(3,440.3362),(5,663.1918),
         (10,1220.3309),(30,3448.8872),(50.4,5722.0146),(66,7460.2885),
         (72.7,8206.8548),(88.2,9933.9859),(104.5,11750.2593),(123.6,13878.5306)]
    cp,bp,ap=fit(pos)
    # x<0: use far points for quadratic (small |x| deviates - V shape near -1.5)
    neg_far=[(-88.2,2274.0783),(-72.7,1869.967),(-66,1695.2867),(-50.4,1288.5682),
             (-30,756.7057),(-10,235.2718),(-7,157.0567),(-8,183.1284)]
    cn,bn,an=fit(neg_far)
    # Small x<0 near-zero region: V-shape with vertex near x=-1.5, min ~13.66
    # Points: (-0.25,78.2),(-0.75,22.88),(-1.5,13.66),(-2,26.7),(-2.5,39.7),
    #         (-3.5,65.8),(-4,78.8),(-5,104.9)
    # Model as quadratic in (x+1.5): y = q*(x+1.5)^2 + r*(x+1.5) + s
    # Fit these small-x points
    small=[(-0.25,78.1958),(-0.75,22.8773),(-1.5,13.6624),(-2,26.6982),
           (-2.5,39.7341),(-3.5,65.8058),(-4,78.8416),(-5,104.9133)]
    cs,bs,as_=fit(small)
    def predict_one(x):
        if x>=0:
            return ap*x*x+bp*x+cp
        else:
            # blend: near-zero V region vs far quadratic
            # transition around x=-6 to -8? At -7,-8 far quad fits. At -5 small fits.
            # Use small-region model for x>-6, far quad for x<=-6
            if x>-6:
                return as_*x*x+bs*x+cs
            else:
                return an*x*x+bn*x+cn
    return {"y":[predict_one(x) for x in probe["x"]]}
