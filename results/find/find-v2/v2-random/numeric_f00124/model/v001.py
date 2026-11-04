def predict(probe):
    # Observations suggest f(x) is roughly quadratic in x.
    # E1: x=88.2 -> 9933.99; x=66 -> 7460.29; x=-61.7 -> 1583.18
    # Check ratios: 9933.99/88.2^2 = 1.277; 7460.29/66^2 = 1.713; not pure x^2.
    # Try y ~ a*x^2 + b*x + c via least squares on E1 data.
    # Points: (88.2,9933.99),(66,7460.29),(-20.3,503.81),(-61.7,1583.18),
    # (2.9,429.19),(-24.3,608.10),(72.7,8206.85),(-50.4,1288.57),(-6,130.99),(21.3,2479.47)
    # Fit quadratic: solve normal equations.
    import math
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys = [9933.9859,7460.2885,503.8102,1583.1784,429.1934,608.097,8206.8548,1288.5682,130.985,2479.4652]
    # Build sums
    n=len(xs)
    S=[sum(x**k for x in xs) for k in range(5)]
    T=[sum(y*x**k for x,y in zip(xs,ys)) for k in range(3)]
    # Solve 3x3: [S4 S3 S2; S3 S2 S1; S2 S1 n] [a b c] = [T2 T1 T0]
    A=[[S[4],S[3],S[2]],[S[3],S[2],S[1]],[S[2],S[1],n]]
    B=[T[2],T[1],T[0]]
    # Gaussian elimination
    for i in range(3):
        p=A[i][i]
        for j in range(i+1,3):
            f=A[j][i]/p
            for k in range(3): A[j][k]-=f*A[i][k]
            B[j]-=f*B[i]
    c=B[2]/A[2][2]
    b=(B[1]-A[1][2]*c)/A[1][1]
    a=(B[0]-A[0][1]*b-A[0][2]*c)/A[0][0]
    def f(x):
        return a*x*x+b*x+c
    return {"y":[f(x) for x in probe["x"]]}
