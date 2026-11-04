def predict(probe):
    # f is undefined for x <= 0 [E1: nulls at -128..0]
    # f is linear for x > 0: slope ~3.09 per unit [E1: 1->-7.8, 2->-1.4907, 4->4.8186, ...]
    #   check: (30.0557 - (-7.8))/(64-1) = 37.8557/63 = 0.6009... no
    #   Actually differences: 1->-7.8, 2->-1.4907 (diff 6.3093 per 1)
    #   2->4: 6.3092 over 2 = 3.1546 per 1
    #   4->8: 6.3092 over 4 = 1.5773 per 1
    #   Hmm, not linear in x. Try log: log2(2)-log2(1)=1 -> 6.3093; log2(4)-log2(2)=1 -> 6.3092; log2(8)-log2(4)=1 -> 6.3092
    #   So f(x) = a + b*log2(x) for x>0
    #   b = 6.3092, a: at x=1, f=-7.8 => a=-7.8
    #   check x=16: -7.8 + 6.3092*4 = -7.8+25.2368=17.4368 ~ 17.4371 ✓
    #   x=32: -7.8+6.3092*5=23.746 ✓
    #   x=64: -7.8+6.3092*6=30.0552 ~ 30.0557 ✓
    import math
    out = []
    for x in probe["x"]:
        if x is None or x <= 0:
            out.append(None)
        else:
            out.append(-7.8 + 6.3092 * math.log2(x))
    return {"y": out}
