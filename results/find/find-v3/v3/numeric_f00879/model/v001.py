import math

def predict(probe):
    # Beliefs:
    # - f has a strong oscillatory (trig-like) component with period ~? [E1-E5]
    # - There is also a linear/offset component [E2]
    # - Values look like a*sin(b*x+c)+d*x+e with noise
    # Let's try fitting a simple form: y = A*sin(w*x+p) + B*x + C
    # From E2: at x=0, y=-0.9235; at x=1, y=0.3397; at x=2, y=2.3379
    # The oscillation is fast. Look at E2 spacing of 20: values vary a lot.
    # Try w such that period ~ some value. Between x=-1 and 1 (y 0.13 to 0.34) not clear.
    # Look at E5: x=-7.1 -> -1.19, x=-16.9 -> -1.31, x=28.4 -> 0.07
    # Hard to pin down. Let's guess a combination.
    # Actually examine: E2 x=-1 y=0.1304, x=0 y=-0.9235, x=1 y=0.3397, x=2 y=2.3379
    # Differences: -1.05, 1.26, 2.0. Not linear.
    # Try: maybe sin with period ~ 2*pi/k. 
    # x=-2 y=0.4785, x=-1 y=0.1304, x=0 y=-0.9235, x=1 y=0.3397, x=2 y=2.3379
    # Looks like oscillation with period maybe ~4-5?
    # x=-5 y=-0.8991, x=-2 y=0.4785, x=1 y=0.3397, x=2 y=2.3379, x=5 y=-0.1059
    # Let's try to fit numerically in code with a few candidate frequencies.
    # We'll do a least-squares-ish grid search over w, then solve linear for A,B,C,p via sin/cos.
    xs = []
    ys = []
    data = [
        (88.2,0.6165),(66.0,0.4877),(-20.3,-2.847),(-61.7,-1.6112),(2.9,2.069),
        (-24.3,-0.3558),(72.7,1.424),(-50.4,-0.9324),(-6.0,-0.5598),(21.3,2.0717),
        (-100.0,-0.3062),(-80.0,-0.2432),(-60.0,0.5693),(-40.0,0.0026),(-20.0,-1.0684),
        (-10.0,-2.129),(-5.0,-0.8991),(-2.0,0.4785),(-1.0,0.1304),(0.0,-0.9235),
        (1.0,0.3397),(2.0,2.3379),(5.0,-0.1059),(10.0,1.0399),(20.0,0.867),
        (40.0,1.2781),(60.0,0.7221),(80.0,1.2217),(100.0,0.9102),(128.0,2.5818),
        (104.5,0.1223),(1.2,2.9398),(-55.8,-0.3847),(65.5,2.0627),(30.3,0.7268),
        (-63.9,-2.1967),(104.9,0.3148),(123.6,0.3213),(79.4,0.6904),(103.0,0.384),
        (-90.0,-1.8521),(-70.0,-0.1952),(-50.0,-2.7373),(-30.0,-0.3303),(-15.0,-2.1433),
        (-7.0,-1.6018),(-3.0,0.9731),(-1.5,-0.8829),(0.5,2.1084),(1.5,1.0495),
        (3.0,1.0168),(7.0,1.8491),(15.0,1.4391),(30.0,-0.516),(50.0,1.2144),
        (70.0,-1.2018),(90.0,0.4975),(110.0,-2.033),(120.0,-0.2488),(127.0,1.2028),
        (-48.6,-1.1807),(58.8,1.3402),(102.1,0.1198),(47.1,0.6372),(-7.1,-1.1901),
        (-102.2,-2.8633),(-16.9,-1.3146),(28.4,0.0732),(105.7,0.9567),(119.5,1.062),
    ]
    for x,y in data:
        xs.append(x); ys.append(y)
    n = len(xs)
    # Fit y = a*sin(w*x) + b*cos(w*x) + c*x + d
    best = None
    # grid search w
    for i in range(1, 2000):
        w = i * 0.01
        # build normal equations for [sin(wx), cos(wx), x, 1]
        import math as m
        S = [[0.0]*4 for _ in range(4)]
        T = [0.0]*4
        for x,y in zip(xs,ys):
            f = [m.sin(w*x), m.cos(w*x), x, 1.0]
            for r in range(4):
                for c in range(4):
                    S[r][c] += f[r]*f[c]
                T[r] += f[r]*y
        # solve 4x4
        try:
            # gaussian elimination
            M = [row[:] + [T[r]] for r,row in enumerate(S)]
            for col in range(4):
                piv = max(range(col,4), key=lambda r: abs(M[r][col]))
                if abs(M[piv][col]) < 1e-12:
                    raise ValueError
                M[col],M[piv] = M[piv],M[col]
                pv = M[col][col]
                for c in range(col,5):
                    M[col][c] /= pv
                for r in range(4):
                    if r != col:
                        fac = M[r][col]
                        for c in range(col,5):
                            M[r][c] -= fac*M[col][c]
            coef = [M[r][4] for r in range(4)]
        except Exception:
            continue
        # compute residual
        err = 0.0
        for x,y in zip(xs,ys):
            pred = coef[0]*m.sin(w*x)+coef[1]*m.cos(w*x)+coef[2]*x+coef[3]
            err += (pred-y)**2
        if best is None or err < best[0]:
            best = (err, w, coef)
    if best is None:
        return {"y": [0.0]*len(probe["x"])}
    err, w, coef = best
    a,b,c,d = coef
    out = []
    for x in probe["x"]:
        out.append(a*math.sin(w*x)+b*math.cos(w*x)+c*x+d)
    return {"y": out}
