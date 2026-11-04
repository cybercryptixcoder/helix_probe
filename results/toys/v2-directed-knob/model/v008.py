def predict(probe):
    # x: at a=5, x=10-b [E1 b=5->5, E3 b=8->2, E9 b=0->10]
    #    at a=8, x=10 regardless of b [E5 b=5->10, E6 b=5->10, E7 b=0->10, E10 b=2->10]
    #    at a=2,b=0 -> x=4 [E8]; at a=2,b=5 -> x=-1 [E11]
    #    So at a=2, b shifts x by -1 per unit: x = 4 - b. At a=5, x = 10 - b.
    #    Slope of b-dependence: at a=2 slope=-1, at a=5 slope=-1, at a=8 slope=0.
    #    Intercept at b=0: a=2->4, a=5->10, a=8->10.
    #    Try x = 10 - b*(8-a)/3 for a>=5 [E5,E6,E7,E9,E10 ok]; for a<5 try x = a+2 - b [E8: 4-0=4 ok; E11: 4-5=-1 ok].
    #    Check a=5 in a>=5 branch: 10-b [E1,E3,E9 ok].
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    if a >= 5:
        x = 10 - b*(8-a)/3.0
    else:
        x = a + 2 - b
    # y = c + max(0,(a-5)/3) [E1,E2,E5,E6,E8,E9,E10,E11]
    y = c + max(0, (a-5)/3.0)
    # size = 1 + 0.5|a-c| [E1,E2,E3,E5,E6,E7,E8,E9,E10,E11]
    size = 1 + 0.5*abs(a-c)
    # switch: no effect [E4]
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
