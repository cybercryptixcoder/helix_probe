def predict(probe):
    # f is zero for |x| >= 0.8 [E4: -0.81 and 0.81 are 0; -0.8 is -5.252, 0.8 is -2.372]
    # Nonzero only on (-0.8, 0.8) [E4]
    # Asymmetric bump: deep dip near x=-0.8 (~-5.25), shallower on right (~-2.37 at 0.8) [E3, E4]
    # Minimum magnitude at x=0 (-1.7) [E1, E3]
    # Values at grid points from E2/E3 [E2, E3]
    pts = [(-0.8,-5.252),(-0.75,-4.9062),(-0.7,-4.577),(-0.65,-4.2643),
           (-0.6,-3.968),(-0.55,-3.6883),(-0.5,-3.425),(-0.45,-3.1783),(-0.4,-2.948),
           (-0.35,-2.7342),(-0.3,-2.537),(-0.25,-2.3563),(-0.2,-2.192),(-0.15,-2.0442),
           (-0.1,-1.913),(-0.05,-1.7982),(-0.02,-1.7373),(0.0,-1.7),(0.02,-1.6653),
           (0.05,-1.6182),(0.1,-1.553),(0.15,-1.5042),(0.2,-1.472),(0.25,-1.4562),
           (0.3,-1.457),(0.35,-1.4742),(0.4,-1.508),(0.5,-1.625),(0.6,-1.808),
           (0.75,-2.2062),(0.8,-2.372)]
    out=[]
    for x in probe.get("x",[]):
        try:
            if x is None or x<=-0.8 or x>=0.8:
                out.append(-0.0)
            else:
                for i in range(len(pts)-1):
                    x0,y0=pts[i]; x1,y1=pts[i+1]
                    if x0<=x<=x1:
                        t=(x-x0)/(x1-x0)
                        out.append(y0+t*(y1-y0))
                        break
                else:
                    out.append(-0.0)
        except Exception:
            out.append(None)
    return {"y":out}
