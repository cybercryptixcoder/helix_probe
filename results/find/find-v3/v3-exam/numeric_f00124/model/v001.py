def predict(probe):
    # Looks like roughly quadratic: y ~ x^2 * something, with asymmetry.
    # Check: x=88.2 -> 9934; 88.2^2=7779, ratio 1.277
    # x=66 -> 7460; 66^2=4356, ratio 1.713
    # x=-20.3 -> 503.8; 20.3^2=412, ratio 1.22
    # x=-61.7 -> 1583; 61.7^2=3807, ratio 0.416
    # x=2.9 -> 429; 2.9^2=8.4, ratio 51
    # Not simple quadratic. Try cubic-ish or exponential?
    # x=2.9 -> 429, x=-6 -> 131, x=21.3 -> 2479
    # 2.9^3=24.4, ratio 17.6; 21.3^3=9664, ratio 0.256
    # Try y = a*x^2 + b*x + c? Fit roughly.
    # Use least squares on the data.
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys = [9933.9859,7460.2885,503.8102,1583.1784,429.1934,608.097,8206.8548,1288.5682,130.985,2479.4652]
    # Fit quadratic via normal equations
    n=len(xs)
    S0=n; S1=sum(xs); S2=sum(x*x for x in xs); S3=sum(x**3 for x in xs); S4=sum(x**4 for x in xs)
    T0=sum(ys); T1=sum(x*y for x,y in zip(xs,ys)); T2=sum(x*x*y for x,y in zip(xs,ys))
    # Solve [S0 S1 S2; S1 S2 S3; S2 S3 S4] [c,b,a] = [T0,T1,T2]
    import math
    A=[[S0,S1,S2],[S1,S2,S3],[S2,S3,S4]]
    B=[T0,T1,T2]
    # Gaussian elimination
    for i in range(3):
        p=A[i][i]
        for j in range(i+1,3):
            f=A[j][i]/p
            for k in range(3): A[j][k]-=f*A[i][k]
            B[j]-=f*B[i]
    sol=[0,0,0]
    for i in range(2,-1,-1):
        s=B[i]-sum(A[i][k]*sol[k] for k in range(i+1,3))
        sol[i]=s/A[i][i]
    c,b,a=sol
    def predict_one(x):
        return a*x*x+b*x+c
    return {"y":[predict_one(x) for x in probe["x"]]}
