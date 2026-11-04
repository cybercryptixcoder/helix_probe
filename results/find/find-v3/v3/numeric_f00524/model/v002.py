def predict(probe):
    # f(x) = x for x in [1,4] and x in [-4,-1] (integers and halves alike) [E2]
    # f(0)=0, f(0.5)=1, f(1.5)=2, f(2.5)=3, f(3.5)=4 -> looks like round-half-up? 
    #   Actually 0.5->1, 1.5->2, 2.5->3, 3.5->4: that's floor(x+0.5) = round half up.
    #   But f(4)=4, f(5)=0, f(-5)=0. So nonzero only where round(x) in {1,2,3,4} or {-1,-2,-3,-4}.
    # f(2.9)=3 [E1] consistent with round(2.9)=3.
    # Hypothesis: f(x) = round(x) if round(x) in [-4,-1] or [1,4], else 0. [E1,E2]
    # ? Boundaries at 0.5 (0.5->1) and 4.5 (4.5->? unknown, guess 0). Negative side: -0.5->? guess 0.
    import math
    out = []
    for x in probe["x"]:
        r = math.floor(x + 0.5)
        if (1 <= r <= 4) or (-4 <= r <= -1):
            out.append(float(r))
        else:
            out.append(0.0)
    return {"y": out}
