import math

def predict(probe):
    # Observations [E1]:
    #   x=88.2 -> 912.9058 ; x=66.0 -> 853.8872 ; x=72.7 -> 873.5674
    #   x=21.3 -> 623.6874 ; x=2.9 -> 217.8175
    #   x=-20.3, -61.7, -24.3, -50.4, -6.0 -> null
    # Pattern: outputs look like a quadratic-ish curve for x>0, undefined for x<0.
    # Try y = a*x^2 + b*x + c fit through the five defined points.
    # Quick check: differences suggest roughly quadratic. Fit below.
    # Undefined region: x < 0 (all negatives null; need boundary check, maybe x<=0).
    # ? Boundary between defined/undefined somewhere near 0; assume x < 0 -> null.
    xs = probe.get("x", [])
    out = []
    # Fit quadratic to E1 defined points (least squares, precomputed coefficients)
    # Using points (2.9,217.8175),(21.3,623.6874),(66,853.8872),(72.7,873.5674),(88.2,912.9058)
    # Solve normal equations numerically here for robustness.
    pts = [(2.9,217.8175),(21.3,623.6874),(66.0,853.8872),(72.7,873.5674),(88.2,912.9058)]
    # Normal equations for [a,b,c]
    S = [[0.0]*3 for _ in range(3)]
    T = [0.0]*3
    for x,y in pts:
        row = [x*x, x, 1.0]
        for i in range(3):
            for j in range(3):
                S[i][j] += row[i]*row[j]
            T[i] += row[i]*y
    # Gaussian elimination
    coef = None
    try:
        M = [S[i][:]+[T[i]] for i in range(3)]
        for i in range(3):
            p = max(range(i,3), key=lambda r: abs(M[r][i]))
            M[i],M[p] = M[p],M[i]
            for r in range(i+1,3):
                f = M[r][i]/M[i][i]
                for c in range(i,4):
                    M[r][c] -= f*M[i][c]
        coef = [0.0]*3
        for i in reversed(range(3)):
            s = M[i][3] - sum(M[i][j]*coef[j] for j in range(i+1,3))
            coef[i] = s/M[i][i]
    except Exception:
        coef = [0.0,0.0,0.0]
    a,b,c = coef
    for x in xs:
        try:
            if x is None:
                out.append(None)
            elif x < 0:
                out.append(None)
            else:
                out.append(a*x*x + b*x + c)
        except Exception:
            out.append(None)
    return {"y": out}
