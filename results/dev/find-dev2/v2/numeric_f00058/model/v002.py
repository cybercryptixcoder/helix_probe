def predict(probe):
    # f is flat at -84.3663 for |x| <= 32 [E1, E2]
    # Outside, f grows smoothly and is NOT symmetric: negative side is larger [E1, E2]
    # Positive side: f(64)=15971, f(96)=134517, f(120)=227192, f(128)=258083 [E1]
    #   f(72)=42011, f(80)=72734, f(100)=149963, f(112)=196300 [E2]
    # Negative side: f(-64)=44756, f(-96)=185653, f(-128)=326549 [E1]
    #   f(-72)=79980, f(-80)=115204, f(-100)=203265, f(-104)=220877,
    #   f(-112)=256101, f(-120)=291325 [E2]
    # Both sides look like a smooth convex curve in (|x|-32); fit a quadratic
    # separately for each sign using outer points. [?]
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax <= 32:
                y = -84.3663
            else:
                d = ax - 32.0
                if x > 0:
                    # fit through (d=32,y=16055.65),(d=96,y=258168.34) with c=-84.3663
                    # and also (d=64,y=135601.9),(d=88,y=227276.75)
                    # Use least squares-ish: pick a,b from (32,16055.65),(96,258168.34)
                    a = 34.18
                    b = (16055.65 - 1024*a)/32.0
                else:
                    # negative side: (d=32,y=44841.09),(d=96,y=326634.17)
                    # (d=64,y=185737.63),(d=88,y=291410.04)
                    a = 44.0
                    b = (44841.09 - 1024*a)/32.0
                y = a*d*d + b*d - 84.3663
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
