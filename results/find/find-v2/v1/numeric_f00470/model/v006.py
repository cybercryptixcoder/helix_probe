def predict(probe):
    """f(x) = x^3 + 2^x + 22 everywhere except a negative bump on (0,1).
    Endpoints x=0 and x=1 match the base formula. On (0,1) we model the
    observed dip with a smooth bump that is zero at 0 and 1."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                base = x**3 + 2.0**x + 22.0
                if 0 < x < 1:
                    # Observed: f(0.25)=-3.2851, f(0.5)=-21.9553, f(0.6)=-22.6466,
                    # f(0.75)=-14.0279, f(0.9)=25.9947 (base at 0.9 ~ 25.99)
                    # Fit a smooth bump B(x) = k * x*(1-x) * (something) that is
                    # negative in the middle. Use a quartic bump through the data.
                    # Try B(x) = -A * x*(1-x) * exp(-((x-0.55)/0.25)^2) style;
                    # simpler: fit cubic-in-bump via three anchor points.
                    # Use quadratic bump: B(x) = a*x*(1-x) + b*x*(1-x)*(x-0.5)
                    # Anchors: at x=0.25 base=22.28+... let's compute base:
                    bx = base
                    # We want f = base + B. Data: B(0.25)=-3.2851-bx(0.25)
                    # bx(0.25)=0.015625+2^0.25+22 = 0.015625+1.189207+22=23.204832
                    # B(0.25)=-26.489932
                    # bx(0.5)=0.125+1.414214+22=23.539214; B(0.5)=-45.494514
                    # bx(0.75)=0.421875+1.681793+22=24.103668; B(0.75)=-38.131568
                    # Fit B(x)=c0*x*(1-x)+c1*x*(1-x)*(x-0.5)+c2*x*(1-x)*(x-0.5)^2
                    # Solve 3x3 quickly with known values.
                    import math
                    def bump(xx):
                        # basis
                        u = xx*(1-xx)
                        v = u*(xx-0.5)
                        w = u*(xx-0.5)**2
                        return c0*u + c1*v + c2*w
                    # Solve linear system for c0,c1,c2 using anchors
                    pts = [(0.25,-26.489932),(0.5,-45.494514),(0.75,-38.131568)]
                    A = []
                    for (xx,_) in pts:
                        u = xx*(1-xx); v=u*(xx-0.5); w=u*(xx-0.5)**2
                        A.append([u,v,w])
                    bvec = [p[1] for p in pts]
                    # Gaussian elimination
                    M = [row[:]+[bvec[i]] for i,row in enumerate(A)]
                    for i in range(3):
                        piv = M[i][i]
                        if abs(piv) < 1e-12:
                            piv = 1e-12
                        for j in range(i,4):
                            M[i][j] /= piv
                        for k in range(3):
                            if k != i:
                                fac = M[k][i]
                                for j in range(i,4):
                                    M[k][j] -= fac*M[i][j]
                    c0,c1,c2 = M[0][3],M[1][3],M[2][3]
                    y = base + bump(x)
                else:
                    y = base
            except Exception:
                y = None
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}
