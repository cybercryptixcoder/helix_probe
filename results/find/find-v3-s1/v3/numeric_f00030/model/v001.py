import math

def predict(probe):
    # Observations [E1]: y is always negative, roughly -1.5 to -1.75.
    # y is most negative near x=0 (-1.2 -> -1.7522) and rises toward
    #   less negative as |x| grows (-120.7 -> -1.4788, 88.9 -> -1.565).
    # Suggests a smooth even-ish function: y = -1.75 + c*x^2-ish, but
    #   asymmetric (88.9 -> -1.565 vs -93.6 -> -1.5235; 67.5 -> -1.5954).
    # Best guess: y = a + b*x + c*x^2 with a ~ -1.75, c>0, small b.
    # Fit from E1 points.
    xs = [-93.6,88.9,67.5,-62.7,-1.2,-12.9,38.8,73.9,-104.0,-120.7]
    ys = [-1.5235,-1.565,-1.5954,-1.5756,-1.7522,-1.6597,-1.6361,-1.5863,-1.5061,-1.4788]
    # least squares quadratic
    n=len(xs)
    S=[sum(x**k for x in xs) for k in range(5)]
    T=[sum((x**k)*y for x,y in zip(xs,ys)) for k in range(3)]
    # solve 3x3
    A=[[S[0],S[1],S[2]],[S[1],S[2],S[3]],[S[2],S[3],S[4]]]
    B=T[:]
    for i in range(3):
        p=A[i][i]
        for j in range(i+1,3):
            f=A[j][i]/p
            for k in range(3): A[j][k]-=f*A[i][k]
            B[j]-=f*B[i]
    c=[0,0,0]
    for i in range(2,-1,-1):
        s=B[i]-sum(A[i][k]*c[k] for k in range(i+1,3))
        c[i]=s/A[i][i]
    a,b,cc=c
    out=[]
    for x in probe["x"]:
        out.append(a+b*x+cc*x*x)
    return {"y":out}
