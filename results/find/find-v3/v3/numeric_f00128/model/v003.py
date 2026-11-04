def predict(probe):
    # f is a smooth MLP approximating a function. Structure inferred:
    # - f(0) ≈ 5.42 [E2,E4]
    # - Positive side: cubic-like, f(x) ≈ -0.00168*x^3 - ... ; f(100)=-1678.8 [E2]
    # - Negative side: cubic-like with smaller magnitude; f(-100)=678.4 [E2]
    # - Near zero, both sides are smooth and nearly linear-ish, NOT the cubic
    #   extrapolation. The cubic only takes over for larger |x|. [E4,E6]
    # - E6 shows: positive side at x=0.6..3.8 is much LESS negative than cubic
    #   (cubic overpredicts magnitude near 0). Negative side near 0 is close to
    #   cubic but slightly off. So there's a smooth transition region.
    # Model: f(x) = base(x) + cubic_correction(x) where correction ramps in
    # with |x| via a smooth gate. Fit base as low-order poly near 0, cubic far.
    import math

    # Positive-side cubic fit (from far points) and near-zero behavior.
    # Use a blend: near-zero quadratic/cubic fit vs far cubic, gated by tanh.
    # Positive far points:
    pos_far = [(4.0,-56.3287),(8.0,-124.0066),(12.0,-191.6061),(16.0,-259.2056),
               (30.0,-495.8039),(45.0,-749.3021),(100.0,-1678.7955)]
    neg_far = [(-8.0,56.4747),(-12.0,83.515),(-16.0,110.5554),(-30.0,205.1965),
               (-45.0,306.5977),(-100.0,678.4023)]
    # Positive near-zero points (E4,E6):
    pos_near = [(0.0,5.4186),(0.1,5.1041),(0.2,4.6858),(0.3,4.0718),(0.5,2.1182),
                (0.6,0.8742),(0.8,-2.1698),(1.0,-5.3245),(1.3,-10.2661),(1.8,-19.1557),
                (2.0,-22.6804),(2.2,-26.0969),(2.8,-36.1281),(3.2,-42.8451),(3.8,-52.9578)]
    neg_near = [(0.0,5.4186),(-0.1,5.704),(-0.2,5.9894),(-0.3,6.2748),(-0.5,6.8447),
                (-0.6,7.1978),(-0.8,8.1725),(-1.0,9.3469),(-1.3,11.2171),(-1.8,14.5622),
                (-2.0,15.9142),(-2.2,17.2662),(-2.8,21.3223),(-3.5,26.0543),(-5.0,36.1945)]

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

    # Near-zero fits (cubic in x) and far cubic fits, blended by a gate.
    pn = fit(pos_near, 4)
    nn = fit(neg_near, 4)
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
        # gate: near-zero behavior dominates for |x| < ~2, far cubic for |x| > ~6
        g = 0.5*(1.0 + math.tanh((abs(x)-4.0)/2.0))
        return near*(1.0-g) + far*g

    return {"y":[f(x) for x in probe["x"]]}
