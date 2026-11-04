import math

def predict(probe):
    # Model hypothesis: f(x) looks like a cubic-ish polynomial.
    # Check ratios: y/x for large |x|:
    #   x=-93.6 -> y/x = -34147 ; x^2=8761 -> y/x^2 = -364.8
    #   x=88.9  -> y/x = -30838 ; x^2=7903 -> y/x^2 = -346.9
    #   x=67.5  -> y/x = -17780 ; x^2=4556 -> y/x^2 = -263.4
    #   x=-62.7 -> y/x = -15317 ; x^2=3931 -> y/x^2 = -244.3
    #   x=-104  -> y/x = -42160 ; x^2=10816 -> y/x^2 = -405.4
    #   x=-120.7-> y/x = -56791 ; x^2=14568 -> y/x^2 = -470.5
    # y/x^2 grows roughly linearly with |x| -> cubic term.
    # Fit cubic a*x^3 + b*x^2 + c*x + d via least squares on E1.
    # Small x: x=-1.2 -> y=7.3208 ; x=-12.9 -> y=8317.4592
    #   x=38.8 -> y=-228025 ; x=73.9 -> y=-1574918
    # Try pure cubic a*x^3: for x=-120.7, x^3=-1758... -> a ~ -3898? 
    # Actually y/x^3: -120.7^3 = -1758... y/x^3 = 6854672/-1758... ~ -3898
    #   88.9^3 = 702... y/x^3 = -2741522/702... ~ -3900
    #   67.5^3 = 307... y/x^3 = -1200206/307... ~ -3900
    #   73.9^3 = 403... y/x^3 = -1574918/403... ~ -3900
    #   104^3 = 1124... y/x^3 = 4384599/1124... ~ 3900 (sign: x negative -> x^3 negative, y positive -> a negative)
    #   -93.6^3 = -820... y/x^3 = 3196163/-820... ~ -3898
    # So y ≈ a*x^3 with a ≈ -3898. Check small x:
    #   x=-1.2: a*x^3 = -3898*(-1.728)=6735, but y=7.32. Not pure cubic.
    # Try a*x^3 + b*x: 
    #   x=-1.2: -3898*(-1.728) + b*(-1.2) = 6735 - 1.2b = 7.32 -> b ≈ 5606
    #   x=-12.9: -3898*(-2146.7) + 5606*(-12.9) = 8367... - 72317 = ... hmm
    #   -12.9^3 = -2146.689; *-3898 = 8367... let me compute: 2146.689*3898=8,367,... ≈ 8367... 
    #   Actually 2146.689*3898 = 8,367,... ~ 8,367,000. minus 5606*12.9=72,317 -> 8,294,700. But y=8317. Way off.
    # So not a*x^3+b*x. Small x gives tiny y. Maybe a*x^3 + b*x^2 + c*x + d.
    # Let's just do least squares fit of cubic on the 10 points.
    xs = [-93.6,88.9,67.5,-62.7,-1.2,-12.9,38.8,73.9,-104.0,-120.7]
    ys = [3196163.7137,-2741522.891,-1200206.4989,960408.3941,7.3208,8317.4592,-228025.2104,-1574918.1983,4384599.9239,6854672.6223]
    # Build normal equations for cubic a x^3 + b x^2 + c x + d
    n = len(xs)
    # powers
    S = [[0.0]*4 for _ in range(4)]
    T = [0.0]*4
    for x,y in zip(xs,ys):
        p = [x**3, x**2, x, 1.0]
        for i in range(4):
            T[i] += p[i]*y
            for j in range(4):
                S[i][j] += p[i]*p[j]
    # Gaussian elimination
    A = [row[:] + [T[i]] for i,row in enumerate(S)]
    for col in range(4):
        piv = max(range(col,4), key=lambda r: abs(A[r][col]))
        A[col],A[piv] = A[piv],A[col]
        if abs(A[col][col]) < 1e-12:
            continue
        for r in range(4):
            if r != col:
                f = A[r][col]/A[col][col]
                for c in range(col,5):
                    A[r][c] -= f*A[col][c]
    coef = [0.0]*4
    for i in range(4):
        if abs(A[i][i]) > 1e-12:
            coef[i] = A[i][4]/A[i][i]
    a,b,c,d = coef

    def f(x):
        return a*x**3 + b*x**2 + c*x + d

    return {"y": [f(x) for x in probe["x"]]}
