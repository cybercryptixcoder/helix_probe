def predict(probe):
    # Looks like f(x) ~ x^2 scaled: check ratios y/x^2
    # -93.6^2=8761 -> 2414.9 (0.2757)
    # 88.9^2=7903 -> 10012 (1.267)  <- not constant, so not pure x^2
    # Try y ~ a*x^2 + b*x + c? Or something with sign.
    # 88.9: 10012, 67.5: 7627, 73.9: 8341, -104: 2686, -120.7: 3121
    # Positive x large -> large y; negative x large -> moderate y.
    # -1.2 -> 7.47, -12.9 -> 310.9, 38.8 -> 4429
    # 38.8^2=1505, y=4429 ~ 2.94x^2. 67.5^2=4556, y=7627 ~1.67x^2
    # Hmm. Try y = a*x^2 + b*x: for 88.9: 7903a+88.9b=10012
    # for 67.5: 4556a+67.5b=7627. Solve: 
    a=(10012*67.5-7627*88.9)/(7903*67.5-4556*88.9)
    # compute quickly
    num=10012*67.5-7627*88.9
    den=7903*67.5-4556*88.9
    a=num/den
    b=(10012-7903*a)/88.9
    # check -104: 10816*a-104*b
    # Just fit quadratic through three points and predict.
    import math
    def fit(xs,ys):
        # least squares quadratic
        n=len(xs)
        S=[[sum(x**(i+j) for x in xs) for j in range(3)] for i in range(3)]
        T=[sum(y*x**i for x,y in zip(xs,ys)) for i in range(3)]
        # solve 3x3
        M=[row[:]+[T[i]] for i,row in enumerate(S)]
        for i in range(3):
            p=M[i][i]
            if abs(p)<1e-12: p=1e-12
            for j in range(i,4): M[i][j]/=p
            for k in range(3):
                if k!=i:
                    f=M[k][i]
                    for j in range(i,4): M[k][j]-=f*M[i][j]
        return [M[i][3] for i in range(3)]
    xs=[-93.6,88.9,67.5,-62.7,-1.2,-12.9,38.8,73.9,-104.0,-120.7]
    ys=[2414.8655,10011.9854,7627.4302,1609.2501,7.4701,310.8797,4429.4519,8340.5682,2686.0111,3121.4084]
    c0,c1,c2=fit(xs,ys)
    out=[]
    for x in probe["x"]:
        out.append(c0+c1*x+c2*x*x)
    return {"y":out}
