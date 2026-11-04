def predict(probe):
    # f is a smooth decreasing sigmoid-like curve, saturating at both ends.
    # Left tail: linear slope ~-0.53 for x < ~-20 [E1,E4,E18,E19,E20,E21]
    # Right tail: linear slope ~-0.20 for x > ~45 [E2,E3,E4,E8,E9,E10]
    # Middle: steep transition around x~5-15 [E4,E6,E7,E9,E12,E15,E17,E21]
    # Key correction: the transition is STEEPER and shifted than v3.
    #   v3 under-predicts steepness near x=0..15 (E21 x=7.1: obs -31.8 vs pred -24.1)
    #   and near x=2.2 (E17: obs -16.2 vs pred -11.7), x=0.9 (E15: obs -11.9 vs pred -8.6)
    #   So the sigmoid must drop faster right after x~0.
    # Left line L(x)=8.1-0.53x fits left tail well [E4 -124.4->74.2, E15 -117.9->70.7]
    # Right line R(x)=-46.3-0.2x fits right tail [E10 127->-70.9, E2 123.6->-70.3]
    # Blend s=sigmoid((x-m)/w). Fit s from observations:
    #   x=0.9: obs -11.9, L=7.6, R=-46.5 => s=(7.6+11.9)/(7.6+46.5)=19.5/54.1=0.360
    #   x=2.2: obs -16.2, L=6.9, R=-46.7 => s=23.1/53.6=0.431
    #   x=7.1: obs -31.8, L=4.3, R=-47.7 => s=36.1/52.0=0.694
    #   x=15.7: obs -41.2, L=-0.2, R=-49.4 => s=41.0/49.2=0.833
    #   x=17.7: obs -42.9, L=-1.3, R=-49.8 => s=41.6/48.5=0.858
    #   x=12.5: obs -38.5, L=1.5, R=-48.8 => s=40.0/50.3=0.795
    #   x=-3.3: obs 0.68, L=9.8, R=-45.6 => s=9.1/55.4=0.164
    #   x=-5.9: obs 6.4, L=11.2, R=-45.1 => s=4.8/56.3=0.085
    #   x=-7.3: obs 9.3, L=12.0, R=-44.8 => s=2.7/56.8=0.048
    #   x=-1.4: obs -4.1, L=8.8, R=-46.0 => s=12.9/54.8=0.235
    # Fit sigmoid: s=1/(1+exp(-(x-m)/w))
    #   s=0.048 at -7.3 => (x-m)/w=-2.99
    #   s=0.694 at 7.1 => (x-m)/w=0.82
    #   => 14.4 = 3.81w => w=3.78, m=7.1-0.82*3.78=4.0
    # Check s at 0.9: (0.9-4)/3.78=-0.82 => s=0.306 vs 0.360 (close)
    # Check s at 15.7: (15.7-4)/3.78=3.10 => s=0.957 vs 0.833 (too high)
    # Transition is asymmetric: slower approach on right. Try wider w on right.
    # Use two-sided: w=3.8 for x<m, w=6 for x>m, m=4.
    #   x=15.7: (11.7)/6=1.95 => s=0.875 vs 0.833 (ok)
    #   x=7.1: (3.1)/6=0.517 => s=0.626 vs 0.694 (a bit low)
    #   x=12.5: (8.5)/6=1.42 => s=0.805 vs 0.795 ✓
    #   x=17.7: (13.7)/6=2.28 => s=0.907 vs 0.858 (a bit high)
    # Compromise: m=4, w_left=3.8, w_right=5.5
    #   x=7.1: 3.1/5.5=0.564 => s=0.637 vs 0.694
    #   x=15.7: 11.7/5.5=2.13 => s=0.894 vs 0.833
    # Slight bias. Use m=3.5, w_right=5.0:
    #   x=7.1: 3.6/5=0.72 => s=0.673 vs 0.694 ✓
    #   x=15.7: 12.2/5=2.44 => s=0.920 vs 0.833 (high)
    # The right side s grows slower than sigmoid; maybe R line is slightly off.
    # Accept approximation: m=4, w_left=3.8, w_right=5.5.
    import math
    def f(x):
        L = 8.1 - 0.53*x
        R = -46.3 - 0.2*x
        if x < 4.0:
            s = 1.0/(1.0+math.exp(-(x-4.0)/3.8))
        else:
            s = 1.0/(1.0+math.exp(-(x-4.0)/5.5))
        return L*(1.0-s) + R*s
    out = []
    for x in probe.get("x", []):
        try:
            out.append(f(float(x)))
        except Exception:
            out.append(None)
    return {"y": out}
