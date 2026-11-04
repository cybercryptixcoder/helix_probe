import math

def predict(probe):
    # Observations: all outputs are near -1.6, varying smoothly with x.
    # E1: y ranges from -1.689 (x=2.9) to -1.566 (x=88.2).
    # Looks like a smooth function with a minimum near x~0, rising toward edges.
    # Hypothesis: f(x) = a + b*cos(c*x) or similar smooth periodic/even-ish shape.
    # From E1: x=2.9 -> -1.689 (lowest), x=-6.0 -> -1.6713, x=88.2 -> -1.566 (highest)
    #   x=-61.7 -> -1.5773, x=72.7 -> -1.588, x=66.0 -> -1.5975
    # Not monotonic in |x|: x=88.2 gives -1.566 but x=72.7 gives -1.588, x=66 gives -1.5975.
    # So it oscillates. Roughly period: from x=2.9 (min) to x=88.2 (max) is ~85 -> half period?
    # Let's fit f(x) = A + B*cos(w*x + p). Try w ~ pi/85? 
    # Actually fit a simple sinusoid by least squares guess.
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys = [-1.566,-1.5975,-1.6472,-1.5773,-1.689,-1.6404,-1.588,-1.5964,-1.6713,-1.6609]
    # Try to fit A + B*cos(w*x) + C*sin(w*x) over a grid of w
    best = None
    n = len(xs)
    for k in range(1, 400):
        w = k * math.pi / 128.0
        # build normal equations for [1, cos(wx), sin(wx)]
        import itertools
        S = [[0.0]*3 for _ in range(3)]
        T = [0.0]*3
        for x, y in zip(xs, ys):
            row = [1.0, math.cos(w*x), math.sin(w*x)]
            for i in range(3):
                T[i] += row[i]*y
                for j in range(3):
                    S[i][j] += row[i]*row[j]
        # solve 3x3
        try:
            M = [r[:] + [T[i]] for i, r in enumerate(S)]
            for i in range(3):
                piv = M[i][i]
                if abs(piv) < 1e-12:
                    raise ValueError
                for j in range(i+1, 3):
                    f = M[j][i]/piv
                    for c in range(4):
                        M[j][c] -= f*M[i][c]
            coef = [0.0]*3
            for i in range(2, -1, -1):
                s = M[i][3]
                for j in range(i+1, 3):
                    s -= M[i][j]*coef[j]
                coef[i] = s/M[i][i]
            err = 0.0
            for x, y in zip(xs, ys):
                pred = coef[0] + coef[1]*math.cos(w*x) + coef[2]*math.sin(w*x)
                err += (pred-y)**2
            if best is None or err < best[0]:
                best = (err, w, coef)
        except Exception:
            pass
    if best is None:
        return {"y": [-1.6]*len(probe["x"])}
    err, w, coef = best
    A, B, C = coef
    out = []
    for x in probe["x"]:
        out.append(A + B*math.cos(w*x) + C*math.sin(w*x))
    return {"y": out}
