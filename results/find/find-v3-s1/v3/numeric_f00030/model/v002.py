import math

def predict(probe):
    # y is always negative, ~-1.47 to -1.82 [E1,E2,E3,E4]
    # Broad smooth bowl: y rises (less negative) as |x| grows to ~128 [E1,E3]
    # Narrow dip near x=0: y drops to ~-1.81 around |x|~0.8, back up by |x|~1.8 [E2,E4]
    # Dip is smooth and roughly symmetric about x=0, min near |x|=0.8 [E4]
    # Base bowl: quadratic in x, asymmetric slightly [E1]
    # Dip: Gaussian centered at x=0 width ~0.8, amplitude ~-0.14 [E4]
    # Fit base quadratic from E1/E3 broad points, dip from E4.

    # Base quadratic (bowl) fit from broad points
    xs = [-127.5,-120.7,-120.2,-104.0,-93.6,-69.4,56.7,67.1,67.5,73.9,86.0,88.9,102.8,114.0]
    ys = [-1.4676,-1.4788,-1.4796,-1.5061,-1.5235,-1.5643,-1.6107,-1.596,-1.5954,-1.5863,-1.5692,-1.565,-1.5451,-1.5291]
    n=len(xs)
    S=[sum(x**k for x in xs) for k in range(5)]
    T=[sum((x**k)*y for x,y in zip(xs,ys)) for k in range(3)]
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

    # Dip: Gaussian centered 0, sigma ~0.8, amplitude ~-0.14
    # From E4: at x=0 y=-1.756, base ~-1.676 -> dip ~-0.08 at center
    # at |x|=0.8 y=-1.813/-1.815, base ~-1.676 -> dip ~-0.138
    # So dip is a ring/bump peaking at |x|~0.8, not centered at 0.
    # Model as Gaussian in |x| centered at 0.8.
    def dip(x):
        ax=abs(x)
        return -0.14*math.exp(-((ax-0.8)**2)/(2*0.45**2))

    out=[]
    for x in probe["x"]:
        out.append(a+b*x+cc*x*x+dip(x))
    return {"y":out}
