def predict(probe):
    # f is a smooth MLP approximating a function. Structure inferred:
    # - f(0) ≈ 5.42 [E2,E4,E10]
    # - Positive side: cubic-like for |x|>~3.5; f(100)=-1678.8 [E2,E6,E8]
    # - Negative side: cubic-like for |x|>~3.5; f(-100)=678.4 [E2,E8]
    # - Near zero (|x|<~3): distinct low-order polynomial per sign, asymmetric
    #   (positive drops steeply, negative rises gently) [E4,E6,E10]
    # - Far cubic already matches down to |x|~3.5 [E8]; near poly matches below ~2
    # - Transition is smooth; gate centered ~3 [E8]
    import math

    pos_far = [(4.0,-56.3287),(8.0,-124.0066),(12.0,-191.6061),(16.0,-259.2056),
               (30.0,-495.8039),(45.0,-749.3021),(100.0,-1678.7955)]
    neg_far = [(-8.0,56.4747),(-12.0,83.515),(-16.0,110.5554),(-30.0,205.1965),
               (-45.0,306.5977),(-100.0,678.4023)]
    # Dense near-zero data (E2,E4,E6,E10)
    pos_near = [(0.0,5.4186),(0.1,5.1041),(0.15,4.9028),(0.2,4.6858),(0.25,4.4171),
                (0.3,4.0718),(0.35,3.6502),(0.45,2.6897),(0.5,2.1182),(0.55,1.5026),
                (0.6,0.8742),(0.65,0.1665),(0.7,-0.5835),(0.75,-1.3675),(0.8,-2.1698),
                (0.85,-2.9733),(0.9,-3.757),(0.95,-4.5408),(1.0,-5.3245),(1.1,-6.9174),
                (1.2,-8.5666),(1.3,-10.2661),(1.4,-11.9849),(1.5,-13.7572),(1.6,-15.5714),
                (1.7,-17.3742),(1.8,-19.1557),(1.9,-20.9273),(2.0,-22.6804),(2.2,-26.0969),
                (2.5,-31.1292),(2.8,-36.1281),(3.0,-39.4742)]
    neg_near = [(0.0,5.4186),(-0.1,5.704),(-0.15,5.8467),(-0.2,5.9894),(-0.25,6.1321),
                (-0.3,6.2748),(-0.35,6.4175),(-0.45,6.6992),(-0.5,6.8447),(-0.55,7.0144),
                (-0.6,7.1978),(-0.7,7.6317),(-0.8,8.1725),(-0.9,8.7466),(-1.0,9.3469),
                (-1.3,11.2171),(-1.5,12.5417),(-1.8,14.5622),(-2.0,15.9142),(-2.2,17.2662),
                (-2.5,19.2942),(-2.8,21.3223),(-3.0,22.6743)]

    def fit(pts, n):
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
                fac=M[j][i]/piv
                for k in range(i,n+1):
                    M[j][k]-=fac*M[i][k]
        coef=[0.0]*n
        for i in range(n-1,-1,-1):
            s=M[i][n]
            for j in range(i+1,n):
                s-=M[i][j]*coef[j]
            coef[i]=s/M[i][i] if abs(M[i][i])>1e-12 else 0.0
        return coef

    pn = fit(pos_near, 5)
    nn = fit(neg_near, 5)
    pf = fit(pos_far, 4)
    nf = fit(neg_far, 4)

    def poly(c, x):
        return sum(c[k]*x**k for k in range(len(c)))

    def f(x):
        if x >= 0:
            near = poly(pn, x)
            far = poly(pf, x)
        else:
            near = poly(nn, x)
            far = poly(nf, x)
        # sharper gate: near poly dominates below ~2, far cubic above ~4
        g = 0.5*(1.0 + math.tanh((abs(x)-3.0)/1.0))
        return near*(1.0-g) + far*g

    return {"y":[f(x) for x in probe["x"]]}
