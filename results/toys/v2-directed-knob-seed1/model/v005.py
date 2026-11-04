import math

def predict(probe):
    # x: at b=5, a=0->-5, a=5->5, a=8->10, a=10->10. So x saturates at 10 for a>=8.
    #   x = min(10, 2a-5) at b=5. Check: a=0->-5, a=5->5, a=8->11->10, a=10->15->10. ok [E1,E4,E5,E8]
    # b shifts x by -(b-5): b=10->x=0 at a=5 (5-5=0) [E6], b=0->x=10 at a=5 (5+5=10) [E7].
    #   So x = min(10, 2a-5) - (b-5)? E6: 5-5=0 ok. E7: 5+5=10 ok. But does b shift before/after clamp? assume after.
    # y: at c=5: a=0->5, a=5->5, a=8->6, a=10->6. So y=5+max(0,(a-5)/3)? a=8->6, a=10->6.67 no.
    #   a=8->6, a=10->6: saturates at 6. y=5+min(1,(a-5)/3). a=8->6, a=10->6.67->6. ok.
    #   Actually a=5->5, a=8->6: slope 1/3. y=5+min(1,(a-5)/3) [E1,E5,E8]
    # c scales y: c=0->0 [E2]. y=(5+min(1,(a-5)/3))*(c/5)
    # size: 1 + 2.5*|a-5|/5 + 2.5*(5-c)/5. E8 a=8: 1+1.5=2.5 ok [E1,E2,E4,E5,E8]
    # switch: no effect [E3]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = min(10.0, 2*a - 5) - (b - 5)
    y = (5 + min(1.0, max(0.0, (a - 5) / 3.0))) * (c / 5.0)
    size = 1.0 + 2.5 * abs(a - 5) / 5.0 + 2.5 * (5 - c) / 5.0
    return {"x": x, "y": y, "size": size}
