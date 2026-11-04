import math

def predict(probe):
    # Beliefs:
    # - Global smooth trend: y rises roughly linearly with x across the domain.
    #   From E2/E5/E6/E7: at x=-128 y~-1.47, at x=128 y~-1.51... actually
    #   y is HIGHER (less negative) at large |x|? Let's check: x=-124.4 -> -1.4727,
    #   x=119.5 -> -1.5214, x=128 -> -1.5099. So both edges are high, center low.
    #   Global shape is a broad U / cosine with minimum near x~0 [E2,E5,E6,E7].
    # - Narrow dip near x=0: a sharp downward spike centered near x=0 (min ~-1.756 at 0),
    #   with extra structure: two deeper troughs near x=+-0.8 (y~-1.813/-1.815) [E8].
    #   So near origin there's a narrow oscillatory dip, not a simple smooth min.
    # - Model: broad cosine baseline + narrow Gaussian-windowed oscillation near 0.

    # Broad baseline: fit from far-field points.
    # Use a cosine: A + B*cos(w*x). Estimate from data:
    #   x=0 -> ~-1.67 (baseline, ignoring dip), x=+-128 -> ~-1.49
    #   So amplitude ~0.09, w such that cos(w*128) ~ +1 -> w ~ pi/128.
    # Refine with a few anchor points.
    xs = [-128,-110,-95,-80,-60,-40,-30,-20,-10,-5,-2,0,2,5,10,20,30,40,60,80,
          88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3,
          104.5,1.2,-55.8,65.5,30.3,-63.9,104.9,123.6,79.4,103.0,
          -48.6,58.8,102.1,47.1,-7.1,-102.2,-16.9,28.4,105.7,119.5,
          90,95,100,105,110,115,120,125,128,92,97,102,107,112,117,122,127,
          -5.9,93.5,-61.3,78.1,12.5,-124.4,56.2,-25.9,83.2,43.0]
    ys = [-1.49,-1.50,-1.51,-1.52,-1.55,-1.58,-1.60,-1.62,-1.65,-1.66,-1.67,-1.67,-1.67,-1.66,-1.65,-1.62,-1.60,-1.58,-1.55,-1.52,
          -1.566,-1.5975,-1.6472,-1.5773,-1.689,-1.6404,-1.588,-1.5964,-1.6713,-1.6609,
          -1.5461,-1.6905,-1.5994,-1.6077,-1.6508,-1.578,-1.541,-1.5214,-1.5804,-1.5461,
          -1.5994,-1.6077,-1.5461,-1.6243,-1.6694,-1.509,-1.6529,-1.6508,-1.541,-1.5214,
          -1.5634,-1.5563,-1.5491,-1.542,-1.5348,-1.5277,-1.5207,-1.514,-1.5099,-1.5606,-1.5534,-1.5462,-1.5391,-1.5319,-1.5249,-1.518,-1.5113,
          -1.6714,-1.5584,-1.578,-1.5804,-1.6733,-1.4727,-1.6114,-1.6377,-1.5732,-1.6301]
    # Exclude near-origin points from baseline fit (|x|<4) since dip dominates.
    bx = [x for x in xs if abs(x) > 4]
    by = [y for x, y in zip(xs, ys) if abs(x) > 4]

    best = None
    n = len(bx)
    for k in range(1, 200):
        w = k * math.pi / 128.0
        S = [[0.0]*3 for _ in range(3)]
        T = [0.0]*3
        for x, y in zip(bx, by):
            row = [1.0, math.cos(w*x), math.sin(w*x)]
            for i in range(3):
                T[i] += row[i]*y
                for j in range(3):
                    S[i][j] += row[i]*row[j]
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
            for x, y in zip(bx, by):
                pred = coef[0] + coef[1]*math.cos(w*x) + coef[2]*math.sin(w*x)
                err += (pred-y)**2
            if best is None or err < best[0]:
                best = (err, w, coef)
        except Exception:
            pass

    if best is None:
        A, B, C, w = -1.6, 0.0, 0.0, math.pi/128.0
    else:
        _, w, coef = best
        A, B, C = coef

    def baseline(x):
        return A + B*math.cos(w*x) + C*math.sin(w*x)

    # Narrow dip near origin. From E8: baseline near 0 is ~-1.67.
    # Observed dip: at x=0 y=-1.756 (depth ~-0.086), at x=+-0.8 y~-1.814 (depth ~-0.144),
    # at x=+-1.5 y~-1.70 (depth ~-0.03). So it's a narrow structure ~1.5 wide,
    # with a local max at 0 and minima near +-0.8. Model as Gaussian-windowed
    # oscillation: dip(x) = -D * exp(-x^2/(2*s^2)) * (something peaked off-center).
    # Simpler: dip(x) = -D*exp(-x^2/(2*s^2)) + E*exp(-(x^2)/(2*s2^2))*cos(2*pi*x/T)
    # Use: dip = -D*exp(-x^2/(2*s^2)) * (1 - cos(2*pi*x/T)) / 2 ... but at 0 that's 0.
    # We need dip(0)~-0.086, dip(0.8)~-0.144, dip(1.5)~-0.03.
    # Try dip(x) = -D*exp(-x^2/(2*s^2)) + E*exp(-x^2/(2*s2^2))*cos(2*pi*x/T)
    # with T~1.6 (period so cos peaks at +-0.8). At x=0: -D + E = -0.086.
    # At x=0.8: -D*exp(-0.32/s^2) + E*exp(-0.32/s2^2)*cos(pi) = -0.144
    # Let s=1.0, s2=1.0: -D*0.726 - E*0.726 = -0.144 -> D+E = 0.198.
    # With -D+E=-0.086: E=0.056, D=0.142. Check x=1.5: exp(-1.125)=0.325.
    # -0.142*0.325 + 0.056*0.325*cos(2*pi*1.5/1.6)= -0.046 + 0.0182*cos(5.89)= -0.046+0.0182*0.925= -0.029. 
    # Matches -0.03! Good.
    D = 0.142
    E = 0.056
    s = 1.0
    s2 = 1.0
    T = 1.6

    def dip(x):
        g = math.exp(-x*x/(2*s*s))
        g2 = math.exp(-x*x/(2*s2*s2))
        return -D*g + E*g2*math.cos(2*math.pi*x/T)

    out = []
    for x in probe["x"]:
        out.append(baseline(x) + dip(x))
    return {"y": out}
