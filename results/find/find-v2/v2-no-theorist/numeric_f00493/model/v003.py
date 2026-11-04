def predict(probe):
    # f(x) = -sign(x) * |x|^p for |x|>=1, p~5.85 [E1,E2,E3,E5]
    #   positive x -> negative y; negative x -> positive y [E2,E5]
    #   |x|^5.85 fits large |x| well: 88.2->-2.3e11, 100->-4.9e11 [E1,E2,E5]
    # Small |x|<1: y=0 for x>0; for -1<x<0 a positive bump peaking ~6.76 near -0.7 [E2,E4]
    # Transition region 1<=|x|<2 differs from pure power law [E4]
    #   x=1->-4.3, 1.1->-5.23, ..., 1.9->-25.2, then 2->-60.2 (jump to power law)
    #   Negative side at -1->6.1, -2->-67.0 (note: -2 is NEGATIVE, sign flipped vs -1!)
    #   Wait: -1->+6.1 but -2->-67.0. Sign flips between -1 and -2. [E2]
    #   So for x<=-2: y = -|x|^5.85 (negative), matching positive side magnitude [E2]
    #   Check -4->-3534.8 vs 4^5.85: log10=5.85*0.602=3.52->3311; obs 3534 close [E2]
    #   -8->-171815 vs 8^5.85: log10=5.85*0.903=5.28->1.9e5; obs 1.7e5 close [E2]
    #   So negative side for |x|>=2: y = -|x|^5.85 (same sign as positive side!)
    #   But -1->+6.1 is the exception in transition region.
    import math
    xs = probe.get("x", [])
    ys = []
    # transition table 1<=x<2 from E4
    tab_x = [1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9]
    tab_y = [-4.3,-5.2257,-6.4027,-7.8647,-9.6501,-11.8031,-14.3742,-17.4207,-21.0072,-25.2065]
    def interp(x):
        if x <= tab_x[0]: return tab_y[0]
        if x >= tab_x[-1]: return tab_y[-1]
        for i in range(len(tab_x)-1):
            if tab_x[i] <= x <= tab_x[i+1]:
                t = (x-tab_x[i])/(tab_x[i+1]-tab_x[i])
                return tab_y[i]*(1-t)+tab_y[i+1]*t
        return tab_y[-1]
    # negative small region -1<x<0 from E2,E4
    ntab_x = [-1.0,-0.9,-0.7,-0.5,-0.3,-0.1,0.0]
    ntab_y = [6.1,6.5864,6.7646,6.2406,5.3558,4.3688,0.0]
    def ninterp(x):
        if x <= ntab_x[0]: return ntab_y[0]
        if x >= ntab_x[-1]: return ntab_y[-1]
        for i in range(len(ntab_x)-1):
            if ntab_x[i] <= x <= ntab_x[i+1]:
                t = (x-ntab_x[i])/(ntab_x[i+1]-ntab_x[i])
                return ntab_y[i]*(1-t)+ntab_y[i+1]*t
        return ntab_y[-1]
    for x in xs:
        try:
            ax = abs(x)
            if x >= 2.0:
                y = -(ax ** 5.85)
            elif x > 0:
                if x < 1.0:
                    y = -0.0
                else:
                    y = interp(x)
            elif x <= -2.0:
                y = -(ax ** 5.85)   # same sign as positive side [E2]
            else:  # -2 < x < 0
                if x > -1.0:
                    y = ninterp(x)
                else:
                    # -2<x<=-1: blend from +6.1 at -1 to -67.0 at -2
                    t = (x - (-1.0))/(-2.0 - (-1.0))
                    y = 6.1*(1-t) + (-67.0)*t
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
