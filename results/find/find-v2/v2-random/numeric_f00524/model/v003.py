def predict(probe):
    # f(x) = round(x) for x in [1, 3), else 0 [E1, E2]
    # E1: x=2.9 -> 3.0; E2: x=1.2 -> 2.0
    # E5: x=-1.6 -> -1.0, so band extends to negatives too: round(x) for x in (-3, -1]? 
    # E5 shows -1.6 -> -1.0, so band includes -1.6.
    # Hypothesis (?): f(x) = round(x) when round(x) != 0 and |x| < 3, else 0.
    # i.e. band is roughly |x| in [0.5, 3) giving nonzero rounded values.
    # But E1 x=-6.0 -> 0, E5 x=-1.6 -> -1. So band is |x| < 3 (nonzero round).
    # Check: x=2.9->3 (round=3, |x|<3 yes). x=1.2->2 (round=2). x=-1.6->-1 (round=-2? no, round(-1.6)=-2).
    # Wait round(-1.6) = -2 in Python, but observed -1.0. So it's truncation toward zero, not round!
    # trunc(-1.6) = -1. trunc(2.9)=2? but observed 3.0. Hmm.
    # E1 x=2.9 -> 3.0. round(2.9)=3. E5 x=-1.6 -> -1.0. round(-1.6)=-2. Contradiction.
    # Maybe it's floor for positives, ceil for negatives? floor(2.9)=2 no.
    # Maybe round half away? round(2.9)=3, round(-1.6)=-2. Still -2.
    # int(-1.6) = -1 (trunc). int(2.9)=2. But observed 3.
    # Perhaps: sign(x)*round(|x|)? round(1.6)=2 -> -2. No.
    # Perhaps it's round(x) but with x=-1.6 giving -1 means round-half-up on magnitude? 
    # Actually maybe the band is [1,3) for positive and [-2,-1) for negative? 
    # Let's just say: for x in [1,3): round(x); for x in [-2,-1): round(x) gives -2 for -1.6... no.
    # Simplest consistent: f(x) = round(x) for x in [1,3) and f(x) = trunc(x) for x in [-2,-1)?
    # Too speculative. Best guess: band is |x| in [1,3), value = round(x) but negative side uses trunc.
    # Actually maybe it's just round(x) for x in [1,3), and for negatives x in [-2,-1) it's ceil(x).
    # ceil(-1.6) = -1. Yes! ceil(-1.6)=-1.
    # So: positive band [1,3): round(x). Negative band [-2,-1): ceil(x).
    # Or unified: for x in [1,3): round; for x in [-2,-1): ceil.
    # Hmm but maybe it's just round(x) with banker's? round(-1.6)=-2 regardless.
    # Let me just use: if 1<=x<3: round(x); elif -2<=x<-1: ceil(x); else 0.
    import math
    out = []
    for x in probe["x"]:
        if 1.0 <= x < 3.0:
            out.append(float(round(x)))
        elif -2.0 <= x < -1.0:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
