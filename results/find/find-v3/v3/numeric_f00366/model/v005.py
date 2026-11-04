import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Observations:
    # - Output is one of a few discrete values: 9.8, 8.8, -11.4, -12.4, and a huge 1548.92 at x=0.
    # - For |x| < ~0.001 (tiny nonzero), sign determines output:
    #     x > 0 -> -11.4, x < 0 -> 9.8  [E4, E6]
    # - At exactly x = 0: 1548.92  [E2]
    # - For |x| in (0.001, ~1): output is 9.8 for x<0, -11.4 for x>0  [E2, E4]
    # - For |x| in (~1, ~4): output is 9.8 for x<0, -11.4 for x>0 until ~3.1-3.5,
    #   then flips to 8.8 for x<0 and -12.4 for x>0  [E2, E4]
    #   Boundary: between 3.0 and 3.1 for positive; between -3.0 and -3.1... 
    #   Actually E2: x=3 -> -11.4, x=5 -> -12.4; E4: 3.1 -> -11.4, 3.5 -> -11.4, 3.9 -> -11.4, 4.1 -> -11.4, 4.5 -> -12.4, 4.9 -> -12.4
    #   Wait re-check E4 positives: 3.1,3.5,3.9,4.1 all -11.4; 4.5,4.9 -> -12.4.
    #   Negatives E4: -4.9,-4.5 -> 8.8; -4.1,-3.9,-3.5,-3.1 -> 9.8.
    #   So boundary for positive is between 4.1 and 4.5; for negative between -4.5 and -4.1.
    #   E2: x=5 -> -12.4, x=-5 -> 8.8. Consistent.
    # - For |x| > ~4.5: output is 8.8 for x<0, -12.4 for x>0  [E1, E3, E5]
    # - So overall: sign(x) determines two families (negative -> 9.8/8.8, positive -> -11.4/-12.4),
    #   and magnitude determines which of the pair.
    # - The tiny region near 0: |x| < ~0.001? E4: 0.001 -> -11.4, 0.01 -> -11.4; -0.001 -> 9.8, -0.01 -> 9.8.
    #   E6: 0.0005 -> -11.4, 0.002 -> -11.4, 0.005 -> -11.4, 0.0001 -> -11.4, 5e-5 -> -11.4.
    #   So even 5e-5 gives -11.4 for positive. So no special tiny region except x=0 exactly.
    #   Wait E4: 0.001 -> -11.4, -0.001 -> 9.8. So the "small" values are just the normal sign-based
    #   values (9.8 for neg, -11.4 for pos) which happen to be the "inner" pair.
    # - So the structure is:
    #     x == 0: 1548.92
    #     x < 0: 9.8 if |x| < B, else 8.8
    #     x > 0: -11.4 if |x| < B, else -12.4
    #   where B is a boundary around 4.1-4.5.
    #
    # Need to pin B. E4 positives: 4.1 -> -11.4, 4.5 -> -12.4. Negatives: -4.1 -> 9.8, -4.5 -> 8.8.
    # E2: 3 -> -11.4, 5 -> -12.4; -3 -> 9.8, -5 -> 8.8.
    # E1: 2.9 -> -11.4, -6 -> 8.8, -20.3 -> 8.8, 21.3 -> -12.4, -24.3 -> 8.8, 72.7 -> -12.4,
    #     -50.4 -> 8.8, -61.7 -> 8.8, 66 -> -12.4, 88.2 -> -12.4.
    # E3: 1.2 -> -11.4, 30.3 -> -12.4, -55.8 -> 8.8, 65.5 -> -12.4, -63.9 -> 8.8, 79.4 -> -12.4,
    #     103 -> -12.4, 104.5 -> -12.4, 104.9 -> -12.4, 123.6 -> -12.4.
    # E5: -48.6 -> 8.8, 58.8 -> -12.4, 102.1 -> -12.4, 47.1 -> -12.4, -7.1 -> 8.8, -102.2 -> 8.8,
    #     -16.9 -> 8.8, 28.4 -> -12.4, 105.7 -> -12.4, 119.5 -> -12.4.
    # E4: -4.9 -> 8.8, -4.5 -> 8.8, -4.1 -> 9.8, -3.9 -> 9.8, -3.5 -> 9.8, -3.1 -> 9.8,
    #     3.1 -> -11.4, 3.5 -> -11.4, 3.9 -> -11.4, 4.1 -> -11.4, 4.5 -> -12.4, 4.9 -> -12.4,
    #     -0.01 -> 9.8, 0.01 -> -11.4, -0.001 -> 9.8, 0.001 -> -11.4, -2 -> 9.8, 2 -> -11.4,
    #     -0.05 -> 9.8, 0.05 -> -11.4.
    #
    # So boundary B is between 4.1 and 4.5 (both signs symmetric). Likely B = 4 (or maybe pi+1?).
    # E4: 4.1 -> inner, 4.5 -> outer. So B in (4.1, 4.5]. Best guess: B = 4.2? 
    # Hmm, but 4.1 inner, 4.5 outer. Could be B=4.3 or 4.4. 
    # Actually maybe B = 4? No, 4.1 is inner so B > 4.1.
    # Could be something like 4.2 or 4.25. Let's guess B = 4.3 (midpoint-ish). Mark with "?".
    # Actually maybe the boundary is at 4.2? Or sqrt(18)=4.2426? Or 4.25? 
    # Let's pick B = 4.25 as a guess (midpoint between 4.1 and 4.5 is 4.3, but 4.25 is plausible).
    # Hmm, 4.1 < B <= 4.5. I'll use B = 4.3 with "?".
    #
    # Also need to check: is x=0 the only special point? E2 has x=0 -> 1548.92.
    # What about very small nonzero? E6 shows 5e-5 -> -11.4 (positive), so no special near-zero region.
    # So only x==0 exactly is special. But what if x is extremely tiny like 1e-300? Probably still
    # sign-based. We'll treat x==0 exactly as special.
    #
    # Also: what's 1548.92? Could be some formula like 1/epsilon? Unclear. Just hardcode for x==0.
    # Maybe it's 1+something. Let's just return 1548.92 for x==0.
    #
    # Also, could the boundary be different for positive and negative? Evidence is symmetric-ish:
    # positive: 4.1 inner, 4.5 outer; negative: -4.1 inner, -4.5 outer. Symmetric.
    #
    # Output values: 9.8, 8.8, -11.4, -12.4. Note 9.8 = 10-0.2, 8.8 = 10-1.2? 
    # -11.4 = -11-0.4, -12.4 = -12-0.4? Unclear. Just use the values.
    
    B = 4.3  # boundary guess, between 4.1 and 4.5 [E4] "?"
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            xv = float(x)
        except (TypeError, ValueError):
            ys.append(None)
            continue
        if math.isnan(xv):
            ys.append(None)
            continue
        if xv == 0.0:
            ys.append(1548.92)
        elif xv < 0:
            if abs(xv) < B:
                ys.append(9.8)
            else:
                ys.append(8.8)
        else:  # xv > 0
            if abs(xv) < B:
                ys.append(-11.4)
            else:
                ys.append(-12.4)
    return {"y": ys}
