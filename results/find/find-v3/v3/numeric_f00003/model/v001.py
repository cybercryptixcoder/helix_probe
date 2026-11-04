import math

def predict(probe):
    # Observations [E1]:
    # - Large positive x -> large positive y, roughly quadratic (88.2->21854, 66->12951, 72.7->15366, 21.3->2092, -61.7->5086)
    # - Small |x| (2.9, -6.0) -> ~ -20.45 (a floor/constant)
    # - x=-20.3 -> -15.87 (slightly above floor), x=-24.3 -> 166.2
    # Hypothesis: y = max(quadratic, floor) where floor ~ -20.45, quadratic ~ a*x^2 + b*x + c
    # Fit from E1: use three points to solve quadratic.
    # Points: (88.2, 21854.2087), (66.0, 12950.8364), (21.3, 2091.9289)
    # Solve for a,b,c.
    x1,y1 = 88.2, 21854.2087
    x2,y2 = 66.0, 12950.8364
    x3,y3 = 21.3, 2091.9289
    # Vandermonde solve
    def solve3():
        # matrix rows [x^2, x, 1]
        import itertools
        A = [[x1*x1, x1, 1.0],[x2*x2, x2, 1.0],[x3*x3, x3, 1.0]]
        b = [y1,y2,y3]
        # Gaussian elimination
        M = [row[:] + [b[i]] for i,row in enumerate(A)]
        for i in range(3):
            piv = M[i][i]
            if abs(piv) < 1e-12:
                # swap
                for j in range(i+1,3):
                    if abs(M[j][i]) > 1e-12:
                        M[i],M[j] = M[j],M[i]
                        piv = M[i][i]
                        break
            for j in range(i+1,3):
                f = M[j][i]/piv
                for k in range(i,4):
                    M[j][k] -= f*M[i][k]
        sol = [0,0,0]
        for i in range(2,-1,-1):
            s = M[i][3]
            for k in range(i+1,3):
                s -= M[i][k]*sol[k]
            sol[i] = s/M[i][i]
        return sol
    a,b,c = solve3()
    floor = -20.4469
    def f(x):
        q = a*x*x + b*x + c
        return max(q, floor)
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
