import math

def predict(probe):
    # x = min(10, 2a - 5 - (b - 5)): a doubles then shifts, b shifts before saturation [E1,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13]
    #   E13: a=0,b=10 -> -10 ok; E12: a=7,b=2 -> min(10,14-5+3)=10 ok
    # y: base = 5 + min(1, max(0, a-7)); y = c + (base-5) [E1,E2,E4,E5,E8,E9,E10,E12,E14]
    #   E14: a=10,c=0 -> 0+1=1 ok; E2: a=5,c=0 -> 0 ok; E15: a=5,c=10 -> 10 ok
    # size: 1 + 2.5*|a-5|/5 + 2.5*max(0, 5-c)/5 [E1,E2,E4,E5,E8,E9,E10,E12,E13,E14,E15]
    #   E15: a=5,c=10 -> 1 + 0 + 0 = 1? but observed 3.5. So c term is |5-c| not max(0,5-c).
    #   Check E2: a=5,c=0 -> 1+0+2.5=3.5 ok. E14: a=10,c=0 -> 1+2.5+2.5=6 ok.
    #   E15: a=5,c=10 -> 1+0+2.5=3.5 ok. So size uses |5-c|.
    # switch: no effect [E3]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = min(10.0, 2*a - 5 - (b - 5))
    base = 5 + min(1.0, max(0.0, a - 7.0))
    y = c + (base - 5)
    size = 1.0 + 2.5 * abs(a - 5) / 5.0 + 2.5 * abs(5 - c) / 5.0
    return {"x": x, "y": y, "size": size}
