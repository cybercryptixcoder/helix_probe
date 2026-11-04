import math

def predict(probe):
    # x: at b=5, a=0->-5, a=5->5, a=8->10, a=10->10. x saturates at 10 for a>=8.
    #   x = min(10, 2a-5) at b=5 [E1,E4,E5,E8]
    # b shifts x by -(b-5), applied AFTER saturation [E6,E7,E10].
    #   E10: a=10,b=0 -> min(10,15)-(0-5)=10+5=15? No, observed 10.
    #   So b shift is applied BEFORE saturation: x = min(10, 2a-5-(b-5)).
    #   Check E6: a=5,b=10 -> min(10,5-5)=0 ok. E7: a=5,b=0 -> min(10,5+5)=10 ok.
    #   E10: a=10,b=0 -> min(10,15+5)=10 ok. E9: a=10,b=5 -> min(10,15)=10 ok.
    # y: at c=5: a=0->5, a=5->5, a=8->6, a=10->6. y=5+min(1,(a-5)/3) [E1,E5,E8,E9,E10]
    # c scales y: c=0->0 [E2]. y=(5+min(1,(a-5)/3))*(c/5)
    # size: 1 + 2.5*|a-5|/5 + 2.5*(5-c)/5 [E1,E2,E4,E5,E8,E9,E10]
    # switch: no effect [E3]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = min(10.0, 2*a - 5 - (b - 5))
    y = (5 + min(1.0, max(0.0, (a - 5) / 3.0))) * (c / 5.0)
    size = 1.0 + 2.5 * abs(a - 5) / 5.0 + 2.5 * (5 - c) / 5.0
    return {"x": x, "y": y, "size": size}
