def predict(probe):
    # x = a [E1, E5]
    # y = b at c=5 [E1]; y=0 at c=0,b=5 [E2]; y=6 at a=10,b=5,c=5 [E5]
    #   -> y depends on a too: at a=10, y=b+1; at a=0, y=b [E4]
    #   Hypothesis: y = b + (a-5)/5 * something? At a=10 -> +1, a=0 -> +0, a=5 -> +0.
    #   ? maybe y = b + max(0,(a-5)/5)? but E4 a=0 gives +0, consistent with (a-5)/5 too (=-1, no).
    #   Try y = b + (a-5)/5: a=10->+1, a=0->-1 (but E4 y=5=b, so -1 wrong).
    #   Try y = b + max(0,(a-5)/5): a=10->+1 ok, a=0->0 ok, a=5->0 ok. ? 
    #   Also c scales y: at c=0 y=0 [E2]. So y = (b + max(0,(a-5)/5)) * (c/5)?
    #   At E2 a=5,b=5,c=0: (5+0)*0=0 ok. E1: 5*1=5 ok. E5: (5+1)*1=6 ok. E4: (5+0)*1=5 ok.
    # size = 1.0 at c=5 [E1,E3]; 3.5 at c=0 [E2]; 3.5 at a=0,c=5 [E4]; 3.5 at a=10,c=5 [E5]
    #   -> size depends on a too: a=5 -> 1.0, a=0 or 10 -> 3.5. |a-5|/5*2.5+1?
    #   a=0: 2.5+1=3.5 ok; a=10: 3.5 ok; a=5: 1.0 ok.
    #   And c: at c=0 size=3.5 with a=5. So size = 1 + 2.5*(|a-5|/5) + 2.5*((5-c)/5)?
    #   E2 a=5,c=0: 1+0+2.5=3.5 ok. E1: 1 ok. E4 a=0,c=5: 1+2.5+0=3.5 ok. E5: 3.5 ok.
    # ? switch assumed no effect [E3]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    y = (b + max(0.0, (a - 5) / 5.0)) * (c / 5.0)
    size = 1.0 + 2.5 * abs(a - 5) / 5.0 + 2.5 * (5 - c) / 5.0
    return {"x": a, "y": y, "size": size}
