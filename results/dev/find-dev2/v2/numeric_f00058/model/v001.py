def predict(probe):
    # f is flat at -84.3663 for |x| <= 32 (a dead/clamped region) [E1]
    # Outside that region f grows steeply and roughly symmetrically-ish [E1]
    # At x=64 f=15971, x=96 f=134517, x=120 f=227192, x=128 f=258083 [E1]
    # Negative side: x=-64 f=44756, x=-96 f=185653, x=-128 f=326549 [E1]
    # Looks like a smooth convex growth outside the flat zone; approximate with
    # a quadratic in (|x|-32) fitted to the outer points. [?]
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
                # fit quadratic through (32,0)->(-84.3663 baseline), (64,15971),(128,258083)
                # Use quadratic a*d^2 + b*d + c with c=-84.3663
                # d=32: 1024a+32b = 16055.65
                # d=96: 9216a+96b = 258168.34
                # solve: from first b=(16055.65-1024a)/32
                # 9216a+96*(16055.65-1024a)/32 = 258168.34
                # 9216a+3*(16055.65-1024a)=258168.34
                # 9216a+48166.95-3072a=258168.34
                # 6144a=210001.39 -> a=34.1800
                a = 34.18
                b = (16055.65 - 1024*a)/32.0
                y = a*d*d + b*d - 84.3663
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
