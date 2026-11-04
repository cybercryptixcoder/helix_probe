import math

def predict(probe):
    # f(x) = round(x) for x in (2, 4) roughly? Let's check evidence.
    # E2: x=2.0 -> 2.0, 2.5->3, 2.8->3, 2.9->3, 3.0->3, 3.1->4, 3.2->4, 3.5->4, 4.0->4
    #   That's round-half-up? round(2.5)=3 (banker's would be 2), round(3.5)=4 (banker's 4 ok)
    #   Actually 2.5->3, 3.5->4: consistent with floor(x+0.5) = round half up.
    #   But 2.0->2, 4.0->4, 1.0->1, 0.0->0, 5.0->0, 10.0->0, -2.9->-2
    #   So outside some interval, f=0. Inside, f=round-half-up(x)?
    #   -2.9 -> -2: that's round(-2.9) = -3 normally, but observed -2. Hmm.
    #   Wait -2.9 -> -2.0. round(-2.9) = -3. So not plain rounding.
    #   Maybe f(x) = round(x) only for x in some positive interval, and -2.9 is different.
    #   -2.9 -> -2 could be truncation toward zero? trunc(-2.9) = -2. Yes!
    #   But 2.5->3 not trunc. Hmm.
    # Let's reconsider: maybe f(x) = round(x) for x in [2,4]? But 2.0->2, 4.0->4 fit round.
    #   1.0->1, 0.0->0 also fit round! 5.0->0, 10.0->0 don't.
    #   -2.9->-2: round(-2.9)=-3, doesn't fit. trunc fits.
    # Maybe f(x) = round(x) for x in [0,4]? 0->0,1->1,2->2,2.5->3,...,4->4. Yes fits!
    #   5->0,10->0 outside. -2.9->-2 outside, but observed -2 not 0.
    # Hmm -2.9 gives -2. So negative side has some behavior.
    # E1: -20.3->-0.0, -61.7->-0.0, -24.3->-0.0, -50.4->-0.0, -6.0->-0.0
    #   These are ~0 (negative zero). So for large negatives, ~0.
    #   -2.9 -> -2.0 is special.
    # Maybe interval is [0,4] for round, and [-3,0) for something? -2.9->-2 = ceil? ceil(-2.9)=-2. Yes!
    #   Or trunc toward zero = -2. Both give -2.
    # Hypothesis: f(x) = round(x) on [0,4], and on [-3,0) f(x)=ceil(x)? Need more data.
    # Actually maybe it's round(x) on [0,4] and the negative region is [-3,0) with ceil.
    # But -6.0 -> -0.0 (0), so outside [-3,0) it's 0.
    # Let's guess: 
    #   if 0 <= x <= 4: round half up (floor(x+0.5))
    #   elif -3 <= x < 0: ceil(x)  (gives -2 for -2.9, 0 for -0.5? ceil(-0.5)=0)
    #   else 0
    # Uncertain about exact boundaries. Mark with ?.
    out = []
    for x in probe["x"]:
        try:
            if 0.0 <= x <= 4.0:
                out.append(float(math.floor(x + 0.5)))
            elif -3.0 <= x < 0.0:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
