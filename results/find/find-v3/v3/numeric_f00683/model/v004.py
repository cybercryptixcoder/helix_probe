import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Positive side (x > 0): f = 13.1*x - 3.5 [E11,E12,E13].
    #   E12 confirms single straight line from x=1 to 70 (slope 13.1, intercept -3.5).
    #   Small positive x (0<x<1) also follows ~13.1x-3.5? Check E14:
    #   0.01->-4.369, 0.025->-4.1725, 0.05->-3.845, 0.1->-3.19, 0.15->-2.535,
    #   0.2->-1.88, 0.25->-2.225, 0.3->0.43, 0.4->0.74, 0.5->2.05, 0.75->8.325.
    #   Slope from 0.01 to 0.5: (2.05+4.369)/0.49 = 13.1. Intercept: 13.1*0.01-3.5=-4.369 YES!
    #   So positive side is ONE line 13.1x-3.5 for all x>0. No 15x-4.5 branch.
    #
    # x == 0: f(0) = -385.12 [E2].
    #
    # Negative side (x < 0): f = 1.35*x - 8.7 approximately? Check E14:
    #   -0.25->-11.2275, -0.2->-11.162, -0.15->-9.0965, -0.1->-11.031,
    #   -0.075->-10.9982, -0.05->-10.9655, -0.025->-9.9327, -0.01->-10.9131.
    #   Most are ~-11, but -0.15->-9.0965 and -0.025->-9.9327 are outliers (noise).
    #   Median near -11. E10 near 0: -0.05->-10.9655, -0.02->-10.9262, -0.005->-10.9065.
    #   So as x->0-, f -> ~-10.9. 
    #   E4 -0.01->-7.9131 is an outlier (noise). E4 -0.1->-8.031 also outlier.
    #   So near 0-, f ~ -10.9.
    #   At x=-1: E4 -1->-11.21, E6 -1.5->-11.865. 
    #   Slope from -0.005 (-10.9065) to -1 (-11.21): (-11.21+10.9065)/(-1+0.005)=0.305? 
    #   Hmm that's shallow. But E10 -0.9->-9.079 (outlier), -0.8->-11.948 (outlier).
    #   Let's use E6/E8 for larger |x|: slope ~1.345, intercept ~-9.85.
    #   At x=-1: 1.345*-1-9.85=-11.195 matches E4 -11.21.
    #   At x=-0.005: 1.345*-0.005-9.85=-9.857 vs observed -10.9065. Off by 1.
    #   So near 0 the line 1.345x-9.85 gives -9.86 but observed ~-10.9.
    #   Hmm. Let's reconsider: maybe f = 1.345*x - 9.85 everywhere on negative side,
    #   and near-0 observations ~-10.9 are just noise around -9.86? Off by ~1, plausible.
    #   But E14 has many near-0 points all ~-11: -0.25,-0.2,-0.1,-0.075,-0.05,-0.01
    #   all ~-11. That's a consistent bias, not noise.
    #   So near 0-, f ~ -11. At x=-1, f~-11.2. At x=-5, f~-16.5. At x=-30, f~-50.
    #   Slope from -1 to -30: (-50.2+11.2)/(-29)=1.345. Intercept: -11.2=1.345*(-1)+c -> c=-9.855.
    #   At x=-0.1: 1.345*-0.1-9.855=-9.99 vs observed -11.03. Off by 1.
    #   At x=-0.25: 1.345*-0.25-9.855=-10.19 vs -11.2275. Off by 1.
    #   So near 0 there's a consistent offset of ~-1. Maybe a small kink near 0.
    #   Let's fit two segments:
    #   x in [-1,0): f = a*x + b. Use -0.005->-10.9065 and -1->-11.21:
    #     slope = (-11.21+10.9065)/(-1+0.005) = 0.305. b = -10.9065 - 0.305*(-0.005) = -10.905.
    #     So f = 0.305*x - 10.905 for -1<x<0. At -0.5: -11.06. E4 -0.5->-9.555 (outlier).
    #     E10 -0.5 not sampled. E14 -0.25->-11.2275 vs 0.305*-0.25-10.905=-10.98. Close.
    #   x <= -1: f = 1.345*x - 9.855.
    #   At x=-1: first gives -11.21, second gives -11.2. Continuous.
    #   Check E6 -1.5: 1.345*-1.5-9.855=-11.87 vs -11.865 YES.
    #   Check E8 -2.2: 1.345*-2.2-9.855=-12.81 vs -12.782 YES.
    #   Check E6 -30: 1.345*-30-9.855=-50.2 YES.
    #   Check E4 -128: 1.345*-128-9.855=-182 vs -178.58. Off by 3.4.
    #   For x<-30, slope slightly less: E4 -128->-178.58, -100->-141.9, -80->-114.7,
    #   -60->-89.5, -45->-67.85, -35->-54.75.
    #   Slope -128 to -35: (-54.75+178.58)/93=1.332. Intercept: -54.75=1.332*(-35)+c -> c=-8.13.
    #   Check -128: 1.332*-128-8.13=-178.6 YES. -100: -141.3 vs -141.9 ok.
    #   So for x<-30: f = 1.332*x - 8.13.
    #   At x=-30: 1.332*-30-8.13=-48.09 vs E6 -50.2. Off by 2. Hmm.
    #   Maybe the kink is at -30 and there's a jump? Or slope changes gradually.
    #   Let's just use 1.345*x-9.855 for x in [-30,-1] and 1.332*x-8.13 for x<-30.
    #   At -30: first -50.2, second -48.09. Discontinuity of 2.1. 
    #   E6 -30->-50.2. E4 -35->-54.75. Slope between: (-54.75+50.2)/(-5)=0.91. 
    #   Hmm shallow. Then -45->-67.85: slope (-67.85+54.75)/(-10)=1.31.
    #   Noisy. Let's just use 1.345*x-9.855 for all x<=-1. At -128: -182 vs -178.58, off 3.4.
    #   At -100: -144.35 vs -141.9, off 2.4. At -60: -90.55 vs -89.5, off 1.
    #   Acceptable given noise. Simpler.
    #
    # So final model:
    #   x == 0: -385.12
    #   x > 0: 13.1*x - 3.5
    #   -1 <= x < 0: 0.305*x - 10.905  (near-flat, ~-11)
    #   x < -1: 1.345*x - 9.855

    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            x = float(x)
            if x == 0.0:
                y = -385.12
            elif x > 0.0:
                y = 13.1 * x - 3.5
            elif x >= -1.0:
                y = 0.305 * x - 10.905
            else:
                y = 1.345 * x - 9.855
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
