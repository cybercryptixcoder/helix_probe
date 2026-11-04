def predict(probe):
    # f(x) = sign-dependent power law for |x|>=1, with a small-|x| region [E2,E4]
    # For x>=1: y = -|x|^p, p~5.85 [E1,E2,E3]
    # For x<=-1: y = +c*|x|^p, c~1.037 [E2]
    # For 0<x<1: y = 0 (exactly -0.0) [E2,E4]
    # For -1<x<0: y ~ +5 to +7, roughly flat/plateau [E2,E4]
    #   x=-0.1->4.37, -0.3->5.36, -0.5->6.24, -0.7->6.76, -0.9->6.59, -1->6.1
    #   peak near -0.7, dips toward -1 and toward 0. Model as smooth bump.
    # At x=1: -4.3 (below power law value -1); transition region near |x|~1
    #   x=1.1->-5.23, 1.2->-6.40, 1.3->-7.86, 1.4->-9.65, 1.5->-11.8, 1.6->-14.4,
    #   1.7->-17.4, 1.8->-21.0, 1.9->-25.2, 2->-60.2
    #   So for 1<=x<2 there's a separate ramp, not the power law.
    #   Check: 1.9^5.85 ~ ? log10=5.85*0.2788=1.63 -> 42.7, but observed 25.2. So no.
    #   Looks like ~ -25*(x-1)^? ... 1.9->25.2, 1.5->11.8, 1.1->5.23
    #   ratio: (1.9-1)=0.9 ->25.2; (1.5-1)=0.5->11.8; (1.1-1)=0.1->5.23
    #   log-log: log(25.2/5.23)/log(0.9/0.1)=1.68/2.20=0.76; not clean power.
    #   Try y ~ -A*(x^q - 1)? 1.9^q-1 vs 1.5^q-1: 25.2/11.8=2.14
    #   q=2: (3.61-1)/(2.25-1)=2.61/1.25=2.09 close! q~2
    #   A: 25.2/(3.61-1)=9.66; 11.8/(2.25-1)=9.44; 5.23/(1.21-1)=24.9 hmm no
    #   Actually try y = -k*(x^2-1): 1.9->9.66*2.61=25.2 ✓; 1.5->9.44*1.25=11.8 ✓
    #   1.1->24.9*0.21=5.23 ✓ but k varies. Try x^2-1 with k~9.5: 1.1->2.0 (obs 5.23) no
    #   Try y=-k*(x^p-1) with p~2.5: 1.9^2.5=4.97-1=3.97; 1.5^2.5=2.76-1=1.76
    #   ratio 3.97/1.76=2.26 vs 25.2/11.8=2.14. p~2.3: 1.9^2.3=4.36-1=3.36; 1.5^2.3=2.53-1=1.53
    #   ratio 2.20. p~2.2: 1.9^2.2=4.07-1=3.07; 1.5^2.2=2.42-1=1.42; ratio 2.16 ✓
    #   1.1^2.2=1.234-1=0.234; 3.07/0.234=13.1 vs 25.2/5.23=4.82. no.
    #   Just fit smooth: y ~ -c*(x-1)^a with a~1.5? 0.9^1.5=0.854; 0.5^1.5=0.354; ratio 2.41
    #   a~1.3: 0.9^1.3=0.872; 0.5^1.3=0.406; ratio 2.15 ✓; 0.1^1.3=0.0501; 0.872/0.0501=17.4 vs 4.82 no
    #   The 1.1 point is odd. Let's just use a smooth interpolation.
    #   Actually maybe it's -A*(x^2-1) for x in [1,2] with A~9.5, and 1.1 is the outlier/noise.
    #   Check 1.1: 9.5*(1.21-1)=2.0, obs 5.23. Off by 2.6x. Hmm.
    #   Try -A*(x^3-1)/something... 1.9^3-1=5.86; 1.5^3-1=2.375; ratio 2.47
    #   A: 25.2/5.86=4.30; 11.8/2.375=4.97; 5.23/(1.331-1)=15.8. no.
    #   I'll use a smooth monotone fit through the points via a simple power law in (x-1).
    #   Fit log(y) vs log(x-1): points (0.1,5.23),(0.5,11.8),(0.9,25.2)
    #   slopes: log(11.8/5.23)/log(5)=0.812/1.609=0.505; log(25.2/11.8)/log(1.8)=0.759/0.588=1.29
    #   Not a power law. Use quadratic in (x-1)? 
    #   y = a*(x-1) + b*(x-1)^2: at 0.1: 0.1a+0.01b=5.23; at 0.9: 0.9a+0.81b=25.2
    #   From first: a+0.1b=52.3; second: a+0.9b=28.0. Subtract: 0.8b=-24.3, b=-30.4, a=55.3
    #   Check 0.5: 0.5*55.3+0.25*(-30.4)=27.65-7.6=20.05 vs 11.8. no.
    #   This region is messy. I'll just interpolate linearly between known behavior.
    #   Actually let me reconsider: maybe the whole thing is y = -sign(x)*|x|^p for |x|>=1
    #   but with p varying, OR there's a smooth blend. Given time, use piecewise linear
    #   interpolation through the observed points for 1<=x<2, and power law beyond.
    # For -2<x<=-1: symmetric-ish? x=-1->6.1. We have no data for -1.1 to -2.
    #   Assume similar to positive side but positive sign: y ~ +|x|^p? At -1: 6.1 vs 1^p=1. no.
    #   Just use plateau ~6 for -1<x<0 and power law for x<=-1.
    import math
    xs = probe.get("x", [])
    ys = []
    # interpolation table for 1<=x<2 (positive side), from E4
    tab_x = [1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0]
    tab_y = [-4.3,-5.2257,-6.4027,-7.8647,-9.6501,-11.8031,-14.3742,-17.4207,-21.0072,-25.2065,-60.2]
    def interp(x):
        if x <= tab_x[0]: return tab_y[0]
        if x >= tab_x[-1]: return tab_y[-1]
        for i in range(len(tab_x)-1):
            if tab_x[i] <= x <= tab_x[i+1]:
                t = (x-tab_x[i])/(tab_x[i+1]-tab_x[i])
                return tab_y[i]*(1-t)+tab_y[i+1]*t
        return tab_y[-1]
    # negative small region table from E2,E4
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
                y = 1.037 * (ax ** 5.85)
            else:  # -2 < x <= 0
                if x > -1.0:
                    y = ninterp(x)
                else:
                    # -2<x<=-1: guess power law-ish positive, blend
                    # at -1: 6.1, at -2: 67.0 (from E2)
                    t = (x - (-1.0))/(-2.0 - (-1.0))  # 0 at -1, 1 at -2
                    y = 6.1*(1-t) + 67.0*t
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
