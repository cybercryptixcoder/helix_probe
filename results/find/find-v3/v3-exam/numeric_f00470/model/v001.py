import math

def predict(probe):
    # Model: f(x) is a sum of two power-law components.
    # From E2: for positive x, y grows roughly like x^7 (70 at x=1, 1.1e7 at x=10).
    # For negative x, y is negative and grows like |x|^7 too but smaller magnitude.
    # E1 shows large values consistent with high power.
    # Hypothesis: f(x) = a*x^7 + b*x^3 + c*x (odd polynomial), with different
    # behavior possibly. Let's fit from E2 data.
    #
    # E2 positive: x=1 -> 70.35, x=2 -> 3783.82, x=10 -> 11386930.38
    # ratio 10/1: 11386930/70.35 = 161,860 ~ 10^5.2, so power ~5.2? Let's check.
    # log(3783.82/70.35)/log(2) = log(53.78)/log(2)=3.99 -> ~4 at small
    # log(11386930/70.35)/log(10)=log(161860)/log(10)=5.209
    # Not a single power. Try polynomial fit.
    #
    # Negative: x=-1 -> -36.091, x=-10 -> -3613824.11
    # ratio = 100,140 ~ 10^5.0006 -> power 5 at large.
    # log(1500.006/36.091)/log(2)=log(41.56)/log(2)=5.377
    #
    # Let's fit odd polynomial a*x^7+b*x^5+c*x^3+d*x using several points.
    # Actually let's just do least squares on powers 1,3,5,7 for positive and negative separately.
    # But simpler: guess form. Let's solve.

    # Use positive data points to fit a*x^7+b*x^5+c*x^3+d*x
    # We'll do a small linear solve.
    pos = [(1,70.35),(2,3783.82),(3,28401.19),(4,118360.4),(5,358940.83),
           (6,889937.3),(7,1919315.07),(8,3736882.84),(9,6727933.75),(10,11386930.38)]
    neg = [(-1,-36.091),(-2,-1500.006),(-3,-10244.411),(-4,-40769.54),(-5,-120305.515),
           (-6,-292916.946),(-7,-623586.531),(-8,-1202334.656),(-9,-2148292.995),(-10,-3613824.11)]

    def fit(data):
        # basis: x, x^3, x^5, x^7
        import itertools
        n = 4
        A = [[0.0]*n for _ in range(n)]
        b = [0.0]*n
        for x,y in data:
            phi = [x, x**3, x**5, x**7]
            for i in range(n):
                b[i] += phi[i]*y
                for j in range(n):
                    A[i][j] += phi[i]*phi[j]
        # gaussian elim
        for i in range(n):
            p = max(range(i,n), key=lambda r: abs(A[r][i]))
            A[i],A[p]=A[p],A[i]
            b[i],b[p]=b[p],b[i]
            if abs(A[i][i])<1e-12: continue
            for r in range(i+1,n):
                f=A[r][i]/A[i][i]
                for c in range(i,n): A[r][c]-=f*A[i][c]
                b[r]-=f*b[i]
        coef=[0.0]*n
        for i in range(n-1,-1,-1):
            if abs(A[i][i])<1e-12: continue
            s=b[i]-sum(A[i][j]*coef[j] for j in range(i+1,n))
            coef[i]=s/A[i][i]
        return coef

    cp = fit(pos)
    cn = fit(neg)

    def predict_one(x):
        if x >= 0:
            c = cp
        else:
            c = cn
        return c[0]*x + c[1]*x**3 + c[2]*x**5 + c[3]*x**7

    return {"y": [predict_one(x) for x in probe["x"]]}
