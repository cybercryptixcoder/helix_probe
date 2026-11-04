import math

def predict(probe):
    # A: outside a special interval, output = floor(x)+1 for x>=0, floor(x)-1 for x<0 [E1]
    #    (i.e. round away from zero). Verified on all E1 points.
    # B: special interval is roughly (30,45) exclusive-ish: 30->31, 45->46 are ordinary [E2]
    #    so boundaries are open: 30 < x < 45.
    # C: inside special interval, output varies with x, roughly in [-0.51,-0.23] [E2]
    #    Values: 32->-0.3752, 35->-0.5061, 38.8->-0.2298, 40->-0.4207, 42->-0.4207? 
    #    Actually 42->-0.4207, 40->-0.2298. Noisy/oscillatory. Best guess: some function
    #    of x; we approximate with a smooth-ish guess. Marked uncertain.
    out = []
    for x in probe["x"]:
        if 30 < x < 45:
            # ? unknown formula inside interval; use a rough sinusoid fit guess
            out.append(-0.37 + 0.14 * math.sin((x - 32) * 1.3))
        else:
            out.append(math.floor(x) + (1 if x >= 0 else -1))
    return {"y": out}
