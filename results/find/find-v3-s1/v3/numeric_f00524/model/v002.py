def predict(probe):
    # f(x) = round(x) except on a region around [-2, -1] where it's clamped to -1..? 
    # Evidence E2: x=-3->-3, -2.5->-2, -2->-2, -1.8..-1.0 -> -1, -0.8->0, -0.6->0, -0.4->0, -0.2->0, 0->0, 0.5->1, 1->1, 2->2
    # E1: -93.6->0, 88.9->0, 67.5->0, -62.7->0, -1.2->-1, -12.9->0, 38.8->0, 73.9->0, -104->0, -120.7->0
    # So: outside the special region, f(x)=0 for |x| large, but E2 shows f(x)=round(x) near 0.
    # Hypothesis: f(x) = round(x) for x in some band, but 0 outside? E1 large values give 0.
    # Actually E1: -93.6->0 not -94. So large |x| -> 0. Band where round(x) applies.
    # E2 shows round behavior from -3 to 2. E1 shows -12.9->0. So band roughly |x| < ~? 
    # But -1.2->-1 fits round. -12.9->0 means band ends before 12.9.
    # Special region: [-2,-1] gives -1 (clamp) instead of round (-2->-2 though). 
    # -2.5->-2 = round(-2.5)=-2 (banker's? round(-2.5)=-2 in Python). -2->-2.
    # -1.8->-1, round(-1.8)=-2. So NOT round there. Clamped to -1.
    # -0.8->0, round(-0.8)=-1. So not round. ->0.
    # Hmm. Let's reconsider: maybe f(x)=x rounded toward zero? -1.8->-1 (trunc), -0.8->0 (trunc), 0.5->1? trunc(0.5)=0 not 1.
    # 0.5->1, 1->1, 2->2, -0.6->0, -0.4->0, -0.2->0, 0->0.
    # Looks like round-half-up? round(0.5)=0 in Python but here 1. So round half away from zero: 0.5->1.
    # -0.8->-1 with round-half-away, but observed 0. So floor? floor(-0.8)=-1 no.
    # -1.8->-1 = ceil. -0.8->0 = ceil. 0.5->1=ceil. 1->1. 2->2. -2.5->-2=ceil. -2->-2. -3->-3.
    # ceil works for all E2 except -1.8->-1 ok, -1.6->-1 ok, -1.4->-1 ok, -1.2->-1 ok, -1.0->-1 ok.
    # ceil(-1.8)=-1 yes! ceil(-0.8)=0 yes! ceil(0.5)=1 yes! ceil(-2.5)=-2 yes!
    # So f(x)=ceil(x) in the band. Check E1: -1.2->ceil=-1 yes. -12.9->ceil=-12, but observed 0. So band excludes -12.9.
    # Large values -> 0. So band is limited. Where? -3 in band (E2). -12.9 not. 
    # Guess band |x| <= some threshold, maybe 10? Unknown. Use |x|<10 -> ceil, else 0. Mark ?.
    import math
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif -10.0 <= x <= 10.0:  # ? band boundary unknown; -3 in, -12.9 out
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
