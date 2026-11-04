import math

def predict(probe):
    # x: at b=5, x = min(10, 2a-5) [E1,E4,E5,E8,E9,E10]; b shifts before saturation [E6,E7,E10,E11,E12,E13]
    #   x = min(10, 2a-5-(b-5))  (E13: a=0,b=10 -> -10 ok)
    # y: at c=5, y=5 for a<=7, y=6 for a>=8 [E1,E4,E5,E8,E9,E10,E12]
    #   base = 5 + min(1, max(0, a-7))
    # c affects y: c=0 gives y=1 at a=10 (base 6) [E14], c=0 gives y=0 at a=5 (base 5) [E2]
    #   So y = base*(c/5) + something? At a=10,c=0: 0 + ? = 1. At a=5,c=0: 0 + ? = 0.
    #   Additive term proportional to (base-5): y = base*(c/5) + (base-5)*(1-c/5)
    #   = (c/5)*base + (1-c/5)*(base-5). Check a=10,c=0: 0 + 1*1 = 1 ok. a=5,c=0: 0 ok.
    #   Equivalent: y = 5*(c/5) + (base-5) = c + (base-5). Check E14: 0+1=1 ok. E2: 0+0=0 ok.
    #   E1 a=5,c=5: 5+0=5 ok. E10 a=10,c=5: 5+1=6 ok.
    # size: 1 + 2.5*|a-5|/5 + 2.5*(5-c)/5 [E1,E2,E4,E5,E8,E9,E10,E12,E13,E14]
    # switch: no effect [E3]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = min(10.0, 2*a - 5 - (b - 5))
    base = 5 + min(1.0, max(0.0, a - 7.0))
    y = c + (base - 5)
    size = 1.0 + 2.5 * abs(a - 5) / 5.0 + 2.5 * (5 - c) / 5.0
    return {"x": x, "y": y, "size": size}
