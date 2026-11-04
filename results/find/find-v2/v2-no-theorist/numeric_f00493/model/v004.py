def predict(probe):
    # f(x) = -sign(x)*|x|^p for |x|>=2, p~5.85 [E1,E2,E5,E8]
    #   positive x -> negative y; negative x -> negative y (same sign) [E2,E8]
    #   |x|^5.85 fits large |x| well [E1,E8]
    # Small |x|<1: y=0 for x>0; for -1<x<0 a positive bump peaking ~6.76 near -0.7 [E2,E4]
    # Transition region 1<=x<2: smooth curve from -4.3 at 1 to -60.2 at 2 [E4,E6]
    #   x=1->-4.3, 1.1->-5.23, ..., 1.9->-25.2, 1.95->-27.56, 1.99->-29.58, 2->-60.2 [E6,E12]
    # Negative transition -2<x<-1: |f(-x)| = |f(x)| mirrored? [E12]
    #   -1.05->11.46, -1.1->10.53, -1.2->8.00, -1.3->4.46, -1.4->-0.28, -1.5->-6.43,
    #   -1.6->-14.21, -1.7->-23.88, -1.8->-35.69, -1.9->-49.96, -1.95->-58.11, -1.99->-65.16, -2->-67.0 [E12]
    #   Note: -1.6->-14.21 matches +1.6->-14.37 (close); -1.5->-6.43 vs +1.5->-11.80 (differ)
    #   So NOT simply mirrored. Negative side is its own curve. [E12]
    import math
    xs = probe.get("x", [])
    ys = []
    # positive transition table 1<=x<=2 from E4,E6,E12
    ptab_x = [1.0,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,1.99,2.0]
    ptab_y = [-4.3,-4.7333,-5.2257,-5.7808,-6.4027,-7.0958,-7.8647,-8.7143,-9.6501,-10.6776,-11.8031,-13.033,-14.3742,-15.8342,-17.4207,-19.1421,-21.0072,-23.0254,-25.2065,-27.561,-29.5769,-60.2]
    # negative transition table -2<=x<=-1 from E12
    ntab_x = [-2.0,-1.99,-1.95,-1.9,-1.8,-1.7,-1.6,-1.5,-1.4,-1.3,-1.2,-1.1,-1.05,-1.0]
    ntab_y = [-67.0,-65.1615,-58.1125,-49.9606,-35.6938,-23.8769,-14.2134,-6.4313,-0.2819,4.4607,8.0016,10.5259,11.4595,6.1]
    def interp(tab_x, tab_y, x):
        if x <= tab_x[0]: return tab_y[0]
        if x >= tab_x[-1]: return tab_y[-1]
        for i in range(len(tab_x)-1):
            if tab_x[i] <= x <= tab_x[i+1]:
                t = (x-tab_x[i])/(tab_x[i+1]-tab_x[i])
                return tab_y[i]*(1-t)+tab_y[i+1]*t
        return tab_y[-1]
    # negative small region -1<x<0 from E2,E4
    stab_x = [-1.0,-0.9,-0.7,-0.5,-0.3,-0.1,0.0]
    stab_y = [6.1,6.5864,6.7646,6.2406,5.3558,4.3688,0.0]
    for x in xs:
        try:
            ax = abs(x)
            if x >= 2.0:
                y = -(ax ** 5.85)
            elif x > 0:
                if x < 1.0:
                    y = 0.0
                else:
                    y = interp(ptab_x, ptab_y, x)
            elif x <= -2.0:
                y = -(ax ** 5.85)
            else:  # -2 < x < 0
                if x > -1.0:
                    y = interp(stab_x, stab_y, x)
                else:
                    y = interp(ntab_x, ntab_y, x)
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
