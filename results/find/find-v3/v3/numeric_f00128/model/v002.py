def predict(probe):
    # f is an MLP approximating a smooth function. Observations show:
    # - f(0) ≈ 5.42 (not 0) [E2]
    # - f is NOT odd: f(-x) ≠ -f(x). E.g. f(-2)=15.91 vs f(2)=-22.68 [E2]
    # - f(-x) ≈ f(x) + something? f(-2)-f(2)=38.6, f(-1)-f(1)=14.67, f(-0.5)-f(0.5)=4.73
    #   Looks like f(-x) - f(x) ≈ 2*(something like a smooth odd-ish term)
    # - Large |x|: f(100)=-1678.8, f(-100)=678.4. f(45)=-749.3, f(-45)=306.6.
    #   f(30)=-495.8, f(-30)=205.2. f(16)=-259.2, f(-16)=110.6.
    #   f(12)=-191.6, f(-12)=83.5. f(8)=-124.0, f(-8)=56.5. f(4)=-56.3, f(-4)=?
    #   Negative side grows like ~ -0.00168*x^3? 100^3*-1.68e-3=-1680. yes.
    #   Positive side: 100^3*6.78e-4=678. yes.
    # So f(x) ≈ a*x^3 + b*x + c with different cubic coeff per sign? But smooth MLP...
    # Actually: f(x) = A*x^3 + B*x + C + D*tanh-like? Let's fit piecewise.
    # Try: f(x) = p*x^3 + q*x + r for x>=0, and s*x^3 + t*x + u for x<0.
    # Positive side points: (0,5.4186),(0.5,2.1182),(1,-5.3245),(2,-22.6804),(4,-56.3287),
    #   (8,-124.0066),(12,-191.6061),(16,-259.2056),(30,-495.8039),(45,-749.3021),(100,-1678.7955)
    # Negative side: (-0.5,6.8447),(-1,9.3469),(-2,15.9142),(-8,56.4747),(-12,83.515),
    #   (-16,110.5554),(-30,205.1965),(-45,306.5977),(-100,678.4023)
    # Fit each side as cubic in x (using x itself, not |x|).
    import math
    def fit(pts):
        n=4
        A=[[0.0]*n for _ in range(n)]
        B=[0.0]*n
        for x,y in pts:
            p=[x**k for k in range(n)]
            for i in range(n):
                B[i]+=p[i]*y
                for j in range(n):
                    A[i][j]+=p[i]*p[j]
        M=[row[:]+[B[i]] for i,row in enumerate(A)]
        for i in range(n):
            piv=M[i][i]
            if abs(piv)<1e-12: continue
            for j in range(i+1,n):
                f=M[j][i]/piv
                for k in range(i,n+1):
                    M[j][k]-=f*M[i][k]
        coef=[0.0]*n
        for i in range(n-1,-1,-1):
            s=M[i][n]
            for j in range(i+1,n):
                s-=M[i][j]*coef[j]
            coef[i]=s/M[i][i] if abs(M[i][i])>1e-12 else 0.0
        return coef
    pos=[(0.0,5.4186),(0.5,2.1182),(1.0,-5.3245),(2.0,-22.6804),(4.0,-56.3287),
         (8.0,-124.0066),(12.0,-191.6061),(16.0,-259.2056),(30.0,-495.8039),
         (45.0,-749.3021),(100.0,-1678.7955)]
    neg=[(-0.5,6.8447),(-1.0,9.3469),(-2.0,15.9142),(-8.0,56.4747),(-12.0,83.515),
         (-16.0,110.5554),(-30.0,205.1965),(-45.0,306.5977),(-100.0,678.4023)]
    cp=fit(pos)
    cn=fit(neg)
    def f(x):
        c=cp if x>=0 else cn
        return sum(c[k]*x**k for k in range(4))
    return {"y":[f(x) for x in probe["x"]]}
