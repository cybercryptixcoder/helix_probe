import math

def predict(probe):
    # Beliefs:
    # - Output is max(g(x), floor) with floor = -20.4469 [E1,E2,E4,E6,E8]
    # - g is smooth and quadratic-ish on each side, but NOT a clean parabola;
    #   the true g is a small MLP, so a quadratic fit is only approximate [E2,E5,E7]
    # - Positive side: g crosses floor between 3.8 and 4.1 (g(3.8)=-20.16,
    #   g(4.1)=-9.30, g(4.4)=6.11) [E4]
    # - Negative side: g crosses floor between -20.8 and -21.0
    #   (g(-20.8)=4.69, g(-21.0)=12.92); below -21 g is smooth quadratic
    #   continuing (g(-22)=54.04, g(-23)=96.01) [E6,E8]
    # - Floor region roughly -20.8 < x < 3.9 [E4,E6,E8]
    # - Fit g as a*x^2+b*x+c per side using all data points [E1..E8]

    floor = -20.4469

    # Positive-side data (x, y) where y is g (above floor)
    pos = [(4.1,-9.3046),(4.4,6.1095),(4.7,27.2487),(5.0,48.3879),
           (10,650.4807),(12.5,965.7695),(15,1281.0582),(21.3,2091.9289),
           (28.4,3172.8715),(30,3458.112),(30.3,3458.112),(43.0,6206.724),
           (47.1,7233.7369),(56.2,9783.9818),(58.8,10583.1013),
           (65.5,12779.9647),(66.0,12950.8364),(72.7,15366.0691),
           (78.1,17501.5867),(79.4,18061.8252),(83.2,19699.4453),
           (88.2,21854.2087),(93.5,24138.2578),(102.1,27844.4507),
           (103.0,28232.3081),(104.5,28878.7371),(104.9,29051.1182),
           (105.7,29395.8803),(119.5,35343.0271),(123.6,37109.9331)]
    # Negative-side data (x, y) where y is g (above floor)
    neg = [(-21.0,12.9172),(-21.2,21.1413),(-21.4,29.3655),(-21.6,37.5896),
           (-21.8,45.8137),(-21.9,49.9257),(-22.0,54.0378),(-22.1,58.1498),
           (-22.2,62.2619),(-22.4,70.486),(-22.6,78.7101),(-22.8,86.9342),
           (-23.0,96.0144),(-24.0,150.0136),(-24.3,166.2134),(-25.0,204.0128),
           (-26.0,267.9176),(-27.0,334.5351),(-28.0,401.1526),(-30,548.2541),
           (-32.0,711.7673),(-35,989.5128),(-38.0,1304.1246),(-42.0,1779.6348),
           (-45,2179.6225),(-46.0,2323.1851),(-48.6,2710.6724),
           (-50.4,2995.4039),(-52.0,3257.673),(-55,3783.0537),
           (-55.8,3927.9297),(-58.0,4342.1354),(-61.3,5003.1218),
           (-61.7,5086.1272),(-63.9,5554.3344),(-70,6954.3912),
           (-80,9582.0843),(-100,15882.924),(-102.2,16586.6114),
           (-124.4,23687.4572),(-128,24838.9457)]

    def lsq_quad(pts):
        Sx4=Sx3=Sx2=Sx1=Sx0=0.0
        Sx2y=Sxy=Sy=0.0
        for x,y in pts:
            x2=x*x
            Sx4+=x2*x2; Sx3+=x2*x; Sx2+=x2; Sx1+=x; Sx0+=1
            Sx2y+=x2*y; Sxy+=x*y; Sy+=y
        A=[[Sx4,Sx3,Sx2],[Sx3,Sx2,Sx1],[Sx2,Sx1,Sx0]]
        b=[Sx2y,Sxy,Sy]
        M=[A[i][:]+[b[i]] for i in range(3)]
        for i in range(3):
            piv=M[i][i]
            if abs(piv)<1e-12:
                for j in range(i+1,3):
                    if abs(M[j][i])>1e-12:
                        M[i],M[j]=M[j],M[i]; piv=M[i][i]; break
            for j in range(i+1,3):
                f=M[j][i]/piv
                for k in range(i,4):
                    M[j][k]-=f*M[i][k]
        sol=[0,0,0]
        for i in range(2,-1,-1):
            s=M[i][3]
            for k in range(i+1,3):
                s-=M[i][k]*sol[k]
            sol[i]=s/M[i][i]
        return sol

    ap,bp,cp = lsq_quad(pos)
    an,bn,cn = lsq_quad(neg)

    def g(x):
        if x >= 0:
            return ap*x*x + bp*x + cp
        else:
            return an*x*x + bn*x + cn

    def f(x):
        return max(g(x), floor)

    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
