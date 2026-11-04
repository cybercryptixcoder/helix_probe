import math

def predict(probe):
    # Mechanism beliefs (from evidence):
    # Positive side: smooth quartic growth; small-x plateau ~ -37 then rises [E4,E6,E14].
    # Negative side has THREE regimes:
    #   |x| small (|x| < ~1.6): gentle plateau near -11.67, rising toward 0 [E12,E16].
    #   |x| ~ 1.6..4.5: a smooth "bump" peaking near x=-2.15 (y~0.074) then plunging [E16,E20].
    #   |x| ~ 4.5..~80: steep quartic growth [E2,E18,E21].
    #   |x| > ~80: SATURATES to a constant ~ -24973124.6 [E5,E7,E9,E11,E15,E19,E21].
    #     (positive side does NOT saturate: E3,E5 large positive x still grow) [E3,E5].
    # The negative transition is NOT a single polynomial; it's a localized hump.
    # The saturation threshold is between 71.6 (quartic) and 98 (constant) [?].

    pos_x = [0.1,0.2,0.3,0.4,0.6,0.8,1.0,1.4,1.8,2.5,3.5,4.5,6,7,12,24,32,64]
    pos_y = [-36.9541,-37.1099,-37.2897,-37.5187,-38.2395,-39.5315,-41.7,-50.1179,-66.8571,-128.925,-340.075,-791.225,-2217.2,-3914.1,-29993.6,-439160.0,-1355761.6,-20915544.0]

    neg_tail_x = [4.5,5.0,5.5,6.0,6.5,7.0,8.0,9.0,10.0,11.0,12.0,14.0,16.0,18.0,20.0,24.0,28.0,32.0,40.0]
    neg_tail_y = [-204.975,-356.2,-574.625,-876.9,-1281.475,-1808.6,-3320.5,-5610.6,-8905.7,-13461.4,-19562.1,-37680.1,-66110.9,-108166.5,-167619.7,-356114.1,-670992.5,-1159026.1,-2878507.7]

    hump_x = [-1.62,-1.68,-1.72,-1.76,-1.8,-1.85,-1.9,-1.95,-2.0,-2.05,-2.1,-2.15,-2.2,-2.25,-2.3,-2.4,-2.5,-2.6,-2.7,-2.8,-2.9,-3.0,-3.2,-3.5,-3.8,-4.0,-4.2,-4.5]
    hump_y = [-2.2564,-1.8061,-1.5227,-1.255,-1.0051,-0.7211,-0.4725,-0.2639,-0.1,0.0144,0.0743,0.0744,0.0093,-0.1266,-0.3389,-1.0171,-2.075,-3.5651,-5.5429,-8.0667,-11.1977,-15.0,-24.8891,-46.525,-78.2243,-106.1,-140.2435,-204.975]

    plat_x = [-0.02,-0.05,-0.08,-0.12,-0.18,-0.25,-0.35,-0.45,-0.55,-0.65,-0.75,-0.85,-0.95,-1.05,-1.15,-1.25,-1.35,-1.45,-1.55,-1.65]
    plat_y = [-11.6676,-11.6174,-11.5648,-11.4901,-11.3666,-11.2016,-10.9191,-10.5736,-10.1584,-9.6701,-9.1078,-8.4738,-7.773,-7.0135,-6.2059,-5.3641,-4.5044,-3.6465,-2.8125,-2.0278]

    # Negative-side saturation: constant for |x| beyond threshold [?].
    SAT_THRESH = 80.0
    SAT_VALUE = -24973124.64

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
    tc=fit(neg_tail_x,neg_tail_y,4)
    hc=fit(hump_x,hump_y,6)
    plc=fit(plat_x,plat_y,4)

    def poly(c,x):
        return sum(c[k]*x**k for k in range(len(c)))

    out=[]
    for x in probe.get("x",[]):
        try:
            if x is None: out.append(None); continue
            x=float(x)
            if x>0:
                y=poly(pc,x)
            elif x==0:
                y=poly(plc,0.0)
            else:
                ax=abs(x)
                if ax>SAT_THRESH:
                    y=SAT_VALUE
                elif ax<=1.65:
                    y=poly(plc,x)
                elif ax<=4.5:
                    y=poly(hc,x)
                else:
                    y=poly(tc,ax)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y":out}
