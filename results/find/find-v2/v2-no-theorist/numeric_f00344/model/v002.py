import math

def predict(probe):
    # Positive side: small-x plateau ~ -37, then ~x^4 growth [E4,E6,E2].
    #   Fit quartic y = a*x^4+b*x^3+c*x^2+d*x+e to positive data.
    # Negative side: plateau ~ -11.67 near 0 [E12], zero near x=-2.15 [E10],
    #   steep |x|^4 growth for |x|>4 [E2,E8]. Fit degree-5 poly.
    pos_x = [0.1,0.2,0.3,0.4,0.6,0.8,1.0,1.4,1.8,2.5,3.5,4.5,6,7,12,24,32,64]
    pos_y = [-36.9541,-37.1099,-37.2897,-37.5187,-38.2395,-39.5315,-41.7,-50.1179,-66.8571,-128.925,-340.075,-791.225,-2217.2,-3914.1,-29993.6,-439160.0,-1355761.6,-20915544.0]
    neg_x = [-0.02,-0.1,-0.3,-0.5,-0.9,-1.3,-1.7,-1.9,-2.1,-2.3,-2.6,-3.0,-3.5,-4.0,-4.5,-6.0,-8.0,-10.0,-14.0,-20.0,-32.0,-64.0]
    neg_y = [-11.6676,-11.5281,-11.0677,-10.375,-8.1313,-4.9353,-1.6625,-0.4725,0.0743,-0.3389,-3.5651,-15.0,-46.525,-106.1,-204.975,-876.9,-3320.5,-8905.7,-37680.1,-178293.8597,-1159026.1,-19342450.1]

    def fit(xs, ys, deg):
        n = deg+1
        A=[[0.0]*n for _ in range(n)]; b=[0.0]*n
        for x,y in zip(xs,ys):
            pw=[x**k for k in range(2*deg+1)]
            for i in range(n):
                b[i]+=y*pw[i]
                for j in range(n): A[i][j]+=pw[i+j]
        for i in range(n):
            p=max(range(i,n),key=lambda r:abs(A[r][i]))
            A[i],A[p]=A[p],A[i]; b[i],b[p]=b[p],b[i]
            if abs(A[i][i])<1e-30: continue
            for r in range(i+1,n):
                f=A[r][i]/A[i][i]
                for c in range(i,n): A[r][c]-=f*A[i][c]
                b[r]-=f*b[i]
        coef=[0.0]*n
        for i in range(n-1,-1,-1):
            s=b[i]
            for j in range(i+1,n): s-=A[i][j]*coef[j]
            coef[i]=s/A[i][i] if abs(A[i][i])>1e-30 else 0.0
        return coef

    pc=fit(pos_x,pos_y,4)
    nc=fit(neg_x,neg_y,5)

    out=[]
    for x in probe.get("x",[]):
        try:
            if x is None: out.append(None); continue
            x=float(x)
            if x>0: y=sum(pc[k]*x**k for k in range(len(pc)))
            elif x<0: y=sum(nc[k]*x**k for k in range(len(nc)))
            else: y=nc[0]
            out.append(y)
        except Exception:
            out.append(None)
    return {"y":out}
