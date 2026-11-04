import math

def predict(probe):
    # Model hypothesis based on E1 only.
    # E1 data: x -> y
    # (88.2,1.1293),(66.0,0.1485),(-20.3,-1.9104),(-61.7,1.2025),(2.9,1.4833),
    # (-24.3,-0.1702),(72.7,2.2951),(-50.4,-0.3553),(-6.0,-0.9291),(21.3,0.5647)
    #
    # Observations:
    # - Outputs are roughly in [-2, 2.3], not monotonic in x.
    # - Looks oscillatory: e.g. x=2.9 -> 1.48, x=-6 -> -0.93, x=-20.3 -> -1.91,
    #   x=21.3 -> 0.56, x=66 -> 0.15, x=72.7 -> 2.30, x=88.2 -> 1.13.
    # - Try y = A*sin(B*x + C) + D. Fit roughly by hand/least squares guess.
    #
    # Quick fit attempt: period ~ 60-70? Let's estimate.
    # Peaks near x=2.9 (1.48) and x=72.7 (2.30). Trough near x=-20.3 (-1.91).
    # If period ~ 70, then 2.9 and 72.7 differ by ~70 -> same phase, but values differ.
    # Try period ~ 90: 2.9 and 72.7 differ by 69.8 ~ 3/4 period? 
    # Let's just do a coarse numeric fit.
    #
    # I'll fit A*sin(B*x+C)+D via grid search over B, then linear least squares for A,C,D.

    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys = [1.1293,0.1485,-1.9104,1.2025,1.4833,-0.1702,2.2951,-0.3553,-0.9291,0.5647]

    best = None
    # grid search B
    import itertools
    for B in [i*0.001 for i in range(1, 2000)]:
        # solve for a*sin(Bx)+b*cos(Bx)+d = y  (linear in a,b,d)
        # normal equations
        Sss=Ssc=Ss=Scs=Scc=Sc=Ssy=Scy=Sy=0.0
        n=len(xs)
        for x,y in zip(xs,ys):
            s=math.sin(B*x); c=math.cos(B*x)
            Sss+=s*s; Ssc+=s*c; Ss+=s
            Scs+=c*s; Scc+=c*c; Sc+=c
            Ssy+=s*y; Scy+=c*y; Sy+=y
        # matrix [[Sss,Ssc,Ss],[Scs,Scc,Sc],[Ss,Sc,n]] [a,b,d] = [Ssy,Scy,Sy]
        M=[[Sss,Ssc,Ss],[Scs,Scc,Sc],[Ss,Sc,n]]
        v=[Ssy,Scy,Sy]
        # solve 3x3
        try:
            det = (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
                  -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
                  +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
            if abs(det)<1e-12: continue
            def solve3(M,v):
                d=det
                def det3(m):
                    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
                           -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                           +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
                out=[]
                for col in range(3):
                    mm=[row[:] for row in M]
                    for r in range(3):
                        mm[r][col]=v[r]
                    out.append(det3(mm)/d)
                return out
            a,b,d=solve3(M,v)
            # residual
            err=0.0
            for x,y in zip(xs,ys):
                pred=a*math.sin(B*x)+b*math.cos(B*x)+d
                err+=(pred-y)**2
            if best is None or err<best[0]:
                best=(err,B,a,b,d)
        except Exception:
            continue

    if best is None:
        return {"y":[None]*len(probe["x"])}

    err,B,a,b,d = best
    # amplitude and phase
    A=math.hypot(a,b)
    # a*sin(Bx)+b*cos(Bx) = A*sin(Bx+phi) where a=A cos(phi)? 
    # A sin(Bx+phi)=A sin cos phi + A cos sin phi -> a=A cos phi, b=A sin phi
    phi=math.atan2(b,a)

    def f(x):
        return A*math.sin(B*x+phi)+d

    return {"y":[f(x) for x in probe["x"]]}
