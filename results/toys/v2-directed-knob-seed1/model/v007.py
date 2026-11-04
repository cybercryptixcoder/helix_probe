import math

def predict(probe):
    # x: at b=5, a=0->-5, a=5->5, a=7->10, a=8->10, a=10->10 [E1,E4,E5,E8,E9,E10,E12]
    #   x = min(10, 2a-5) at b=5; saturates at 10 for a>=7.5
    # b shifts x before saturation: x = min(10, 2a-5-(b-5)) [E6,E7,E10,E11,E12]
    #   E12: a=7,b=2 -> min(10,14-5-(-3))=min(10,12)=10 ok
    # y: at c=5: a=0->5, a=5->5, a=7->5, a=8->6, a=10->6 [E1,E4,E5,E8,E9,E10,E12]
    #   y rises only above a~7.5, saturating at 6. y = 5 + min(1, max(0,(a-7.5)/2.5))
    #   E12: a=7 -> 5 ok; E8: a=8 -> 5+min(1,0.2)=5.2? observed 6. Hmm.
    #   E8 a=8 -> 6, E12 a=7 -> 5. So threshold between 7 and 8, reaches 6 by 8.
    #   y = 5 + min(1, max(0,(a-7)/1)) -> a=7:5, a=8:6, a=10:6 ok
    # c scales y: c=0->0 [E2]. y = (5 + min(1,max(0,a-7)))*(c/5)
    # size: 1 + 2.5*|a-5|/5 + 2.5*(5-c)/5 [E1,E2,E4,E5,E8,E9,E10,E12]
    # switch: no effect [E3]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = min(10.0, 2*a - 5 - (b - 5))
    y = (5 + min(1.0, max(0.0, a - 7.0))) * (c / 5.0)
    size = 1.0 + 2.5 * abs(a - 5) / 5.0 + 2.5 * (5 - c) / 5.0
    return {"x": x, "y": y, "size": size}
