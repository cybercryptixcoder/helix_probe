def predict(probe):
    # x: at a=5, x=10-b [E1 b=5->5, E3 b=8->2, E9 b=0->10]
    #    at a=8, x=10 regardless of b [E5 b=5->10, E6 b=5->10, E7 b=0->10, E10 b=2->10]
    #    at a=2, b=0 -> x=4 [E8]; at a=2, b=5 -> x=-1 [E11]; so x=4-b at a=2
    #    at a=3, b=0 -> x=6 [E12]; so intercept grows with a in low range
    #    Intercepts at b=0: a=2->4, a=3->6, a=5->10, a=8->10.
    #    Slope -1 per b for a<=5; slope 0 for a>=8 (interpolate between).
    #    For a<=5: intercept = 2a (a=2->4, a=3->6, a=5->10). x = 2a - b.
    #    For a>=5: x = 10 - b*(8-a)/3 [E5,E6,E7,E9,E10 ok].
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    if a >= 5:
        x = 10 - b*(8-a)/3.0
    else:
        x = 2*a - b
    # y = c + max(0,(a-5)/3) [E1,E2,E5,E6,E8,E9,E10,E11,E12]
    y = c + max(0, (a-5)/3.0)
    # size = 1 + 0.5|a-c| [E1,E2,E3,E5,E6,E7,E8,E9,E10,E11,E12]
    size = 1 + 0.5*abs(a-c)
    # switch: no effect [E4]
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
