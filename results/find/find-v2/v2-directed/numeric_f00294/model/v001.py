def predict(probe):
    # For x < 0: y = x - 8.4 (linear, slope 1, offset -8.4) [E1]
    # For x > 0: y = x + 16.8 (linear, slope 1, offset +16.8) [E1]
    # At x = 0: y = 2058.0 (isolated spike) [E1]
    # Note: x=0.5 gives 17.8 = 0.5+17.3? Actually 0.5+16.8=17.3, observed 17.8.
    #   x=1 -> 17.8 = 1+16.8. x=0.5 -> 17.8 too. Hmm, 0.5+16.8=17.3 != 17.8.
    #   Perhaps offset is +16.8 for x>=1, and for 0<x<1 something else. [E1]
    #   x=0.5 -> 17.8, x=1 -> 17.8. Maybe y = max(x,1)+16.8 for x>0? Check:
    #   x=2 -> 18.8 = 2+16.8 yes. x=4 -> 20.8 yes. x=0.5 -> max(0.5,1)+16.8=17.8 yes.
    #   So for x>0: y = max(x,1)+16.8. [E1]
    # For x<0: check x=-0.5 -> -8.4 = -0.5-7.9? -0.5-8.4=-8.9 no. Observed -8.4.
    #   x=-1 -> -9.4 = -1-8.4 yes. x=-0.5 -> -8.4 = -0.5-7.9? Hmm -0.5-8.4=-8.9.
    #   Maybe y = min(x,-1)-8.4 for x<0? x=-0.5 -> min(-0.5,-1)-8.4=-1-8.4=-9.4 no.
    #   x=-0.5 -> -8.4. -0.5-8.4=-8.9. Not matching. Try y=x-7.9? -0.5-7.9=-8.4 yes but -1-7.9=-8.9 no.
    #   Hmm. x=-2 -> -10.4 = -2-8.4 yes. x=-1 -> -9.4 yes. x=-0.5 -> -8.4 = -0.5-7.9.
    #   Maybe for -1<x<0: y = x - 7.9? Only one point. Or y = -8.4 constant? 
    #   Actually -0.5-8.4 = -8.9, but observed -8.4. Difference 0.5. Maybe y = x - 8.4 + 0.5*? 
    #   Simpler: maybe y = x - 8.4 for x<=-1, and for -1<x<0 it's x-7.9? Uncertain. [E1 ?]
    #   Let's just use: x<0 -> x - 8.4, except -1<x<0 -> x - 7.9 (guess). [E1 ?]
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                y = 2058.0
            elif x > 0:
                y = max(x, 1) + 16.8
            else:
                if x <= -1:
                    y = x - 8.4
                else:
                    y = x - 7.9
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
