import math

def predict(probe):
    # Model hypotheses:
    # Dead zone: f(x) = -22.8021 for |x| <= 7 [E2, E4]
    # Outside dead zone, f is smooth quadratic-ish, slightly asymmetric [E1,E2,E3,E5]
    # Transition is a smooth ramp, not a hard jump [E4, E6]
    # From E6: at x=7.5 y=97.0, x=8 y=132.2, x=8.5 y=167.4, x=9 y=202.6,
    #   x=9.5 y=237.7, x=10 y=272.9, x=10.5 y=308.1, x=11 y=343.3
    #   -> linear ramp with slope ~70.6 per unit on positive side
    #   negative side: x=-7.5 y=-13.0, -8 y=21.8, -8.5 y=83.7, -9 y=145.7,
    #   -9.5 y=207.6, -10 y=269.5, -10.5 y=331.5, -11 y=393.4
    #   -> slope ~81.4 per unit on negative side (steeper)
    # So the ramp is NOT symmetric: positive slope ~70.6, negative slope ~81.4.
    # Ramp appears to start at |x|=7 (value -22.8) and continue linearly.
    # Let's fit: positive side y = -22.8021 + 70.6*(x-7) for 7<x<~11
    #   check x=11: -22.8+70.6*4 = 259.6, obs 343.3 -> off.
    # Try slope from x=7.5 to 11: (343.3-97.0)/3.5 = 70.4. Extrapolate to x=7:
    #   97.0 - 70.4*0.5 = 61.8, but obs at 7 is -22.8. So not linear from 7.
    # Actually the ramp from 7 to 7.5 jumps: -22.8 to 97.0 = 119.8 in 0.5.
    # Then 7.5->8: 35.2, 8->8.5: 35.2, ... constant 35.2 per 0.5 = 70.4/unit.
    # So there's a steep initial jump then linear. Hmm.
    # Let's reconsider: maybe it's quadratic outside but the MLP smooths it.
    # Fit quadratic to positive side points 7.5..11:
    #   Use x=8 (132.19), x=10 (272.93), x=11 (343.31)
    #   a*64+b*8+c=132.19; a*100+b*10+c=272.93; a*121+b*11+c=343.31
    #   Subtract: 36a+2b=140.74 -> 18a+b=70.37
    #             21a+b=70.38 -> 3a=0.01 -> a~0.003, b~70.3
    #   So locally linear with slope ~70.3 on positive side.
    # Negative side x=-8 (21.82), -10 (269.53), -11 (393.38):
    #   a*64-8b+c=21.82; a*100-10b+c=269.53; a*121-11b+c=393.38
    #   36a-2b=247.71 -> 18a-b=123.86
    #   21a-b=123.85 -> 3a=-0.01 -> a~0, b~-123.86
    #   So slope ~123.86 on negative side? Check -8.5: 21.82+123.86*0.5=83.75 obs 83.75. 
    #   Check -9: 21.82+123.86=145.68 obs 145.67. Yes! Linear slope 123.86.
    # Wait recompute positive: 8->8.5: 167.38-132.19=35.19 -> slope 70.38
    #   8.5->9: 202.56-167.38=35.18. Yes slope 70.38.
    # So positive ramp slope ~70.38, negative ramp slope ~123.86. Very asymmetric!
    # Hmm but at x=10 positive: 132.19+70.38*2=272.95 obs 272.93. Good.
    # At x=11: 132.19+70.38*3=343.33 obs 343.31. Good.
    # So ramp is linear on each side with different slopes.
    # Where does ramp end and quadratic begin? At x=15 obs 748.24, x=25 obs 2094.92.
    # Quadratic from ramp: at x=11, 343.31. At x=15, 748.24. At x=25, 2094.92.
    # Fit quadratic a*x^2+b*x+c through 11,15,25:
    #   121a+11b+c=343.31
    #   225a+15b+c=748.24
    #   625a+25b+c=2094.92
    #   diff: 104a+4b=404.93 -> 26a+b=101.23
    #         400a+10b=1346.68 -> 40a+b=134.67
    #   14a=33.44 -> a=2.389, b=101.23-26*2.389=39.12
    #   c=343.31-121*2.389-11*39.12=343.31-289.07-430.32=-376.08
    # Check x=20: 2.389*400+39.12*20-376.08=955.6+782.4-376.1=1361.9 obs 1357.3. Close.
    # Check x=30: 2.389*900+39.12*30-376.08=2150.1+1173.6-376.1=2947.6 obs 3042.98. Off by 3%.
    # Check x=40: 2.389*1600+39.12*40-376.08=3822.4+1564.8-376.1=5011.1 obs 5460.3. Off 8%.
    # So quadratic coefficient grows. Maybe it's not quadratic but higher order, or
    # the MLP has a smooth nonlinearity.
    # Let's fit quadratic to larger points: x=40 (5460.32), 60 (12387.5), 80 (22248.69), 100 (34058.67), 120 (45868.65)
    #   Try a*x^2+b*x+c:
    #   1600a+40b+c=5460.32
    #   3600a+60b+c=12387.5
    #   6400a+80b+c=22248.69
    #   10000a+100b+c=34058.67
    #   14400a+120b+c=45868.65
    #   diffs: 2000a+20b=6927.18 -> 100a+b=346.36
    #          2800a+20b=9861.19 -> 140a+b=493.06
    #          3600a+20b=11809.98 -> 180a+b=590.50
    #          4400a+20b=11809.98 -> 220a+b=590.50
    #   From first two: 40a=146.70 -> a=3.6675, b=346.36-366.75=-20.39
    #   Check third: 180*3.6675-20.39=639.76 vs 590.50. Off.
    #   Not a clean quadratic. MLP approximation.
    # Let's just do piecewise linear interpolation from observed data points,
    # since MLP is smooth and we have dense samples. But better: fit a smooth
    # function. Given MLP, maybe f(x) = something like a*x^2 with a sigmoid gate.
    # Actually let's reconsider: maybe f(x) = A*(x^2) * sigmoid-like, or
    # f(x) = a*x^2 + b*x + c for large |x| but with a soft dead zone.
    # Let's fit quadratic to large positive points 60,80,100,120:
    #   3600a+60b+c=12387.5
    #   6400a+80b+c=22248.69
    #   10000a+100b+c=34058.67
    #   14400a+120b+c=45868.65
    #   2800a+20b=9861.19 -> 140a+b=493.06
    #   3600a+20b=11809.98 -> 180a+b=590.50
    #   4400a+20b=11809.98 -> 220a+b=590.50
    #   From first two: 40a=97.44 -> a=2.436, b=493.06-341.04=152.02
    #   Check third: 220*2.436+152.02=687.9 vs 590.5. Off.
    # Not quadratic. The MLP is approximating something with growing curvature.
    # Let's check if it's cubic-ish or exponential.
    # Ratios: 120^2/60^2=4, y ratio 45868/12387=3.70. Less than quadratic.
    # 80^2/40^2=4, y ratio 22248/5460=4.07. About quadratic.
    # Hmm inconsistent. Let's just use interpolation.
    # Given the difficulty, use piecewise linear interpolation on a dense set of
    # known points, plus the dead zone and ramp.
    # Known points (x,y):
    # Negative side (from E2,E3,E5,E6):
    #   -127.5: 50927.45, -121.5: 47385.39, -120.7: 46913.11, -120.6: 46854.08,
    #   -120.2: 46617.94, -104: 37054.37, -93.6: 30914.79, -72.6: 18712.60,
    #   -71.2: 18003.99, -69.4: 17112.22, -62.7: 13990.07, -40: 5748.25,
    #   -30.4: 3348.34, -30: 3259.36, -25: 2277.76, -20: 1508.06, -19.9: 1495.68,
    #   -17.2: 1161.27, -15.9: 1000.26, -15: 888.80, -14: 764.94, -12.9: 628.70,
    #   -11: 393.38, -10.5: 331.45, -10: 269.53, -9.5: 207.60, -9: 145.67,
    #   -8.5: 83.75, -8: 21.82, -7.5: -13.00
    # Positive side:
    #   7.5: 97.00, 8: 132.19, 8.5: 167.38, 9: 202.56, 9.5: 237.75, 10: 272.93,
    #   10.5: 308.12, 10.6: 315.16, 11: 343.31, 15: 748.24, 20: 1357.30,
    #   25: 2094.92, 30: 3042.98, 38.8: 5134.75, 40: 5460.32, 50: 8572.41,
    #   56.7: 11053.66, 60: 12387.50, 67.1: 15521.38, 67.5: 15708.51,
    #   73.9: 18854.79, 80: 22248.69, 86: 25791.69, 88.9: 27504.13,
    #   100: 34058.67, 102.8: 35712.07, 112.4: 41380.86, 114: 42325.65,
    #   120: 45868.65
    # Use linear interpolation between these sorted points, with dead zone |x|<=7.
    # For |x|>max known, extrapolate linearly from last two points.
    neg_pts = [
        (-127.5, 50927.4542), (-121.5, 47385.3894), (-120.7, 46913.11),
        (-120.6, 46854.0797), (-120.2, 46617.942), (-104.0, 37054.37),
        (-93.6, 30914.79), (-72.6, 18712.6042), (-71.2, 18003.9929),
        (-69.4, 17112.224), (-62.7, 13990.07), (-40.0, 5748.2505),
        (-30.4, 3348.3366), (-30.0, 3259.3629), (-25.0, 2277.7612),
        (-20.0, 1508.0627), (-19.9, 1495.6774), (-17.2, 1161.2731),
        (-15.9, 1000.2636), (-15.0, 888.7955), (-14.0, 764.942),
        (-12.9, 628.70), (-11.0, 393.3816), (-10.5, 331.4549),
        (-10.0, 269.5282), (-9.5, 207.6015), (-9.0, 145.6747),
        (-8.5, 83.748), (-8.0, 21.8213), (-7.5, -12.9955),
    ]
    pos_pts = [
        (7.5, 97.0047), (8.0, 132.1905), (8.5, 167.3763), (9.0, 202.5621),
        (9.5, 237.7478), (10.0, 272.9336), (10.5, 308.1194), (10.6, 315.1565),
        (11.0, 343.3051), (15.0, 748.2438), (20.0, 1357.3016),
        (25.0, 2094.9201), (30.0, 3042.9824), (38.8, 5134.75),
        (40.0, 5460.3248), (50.0, 8572.4127), (56.7, 11053.6592),
        (60.0, 12387.5033), (67.1, 15521.3825), (67.5, 15708.51),
        (73.9, 18854.79), (80.0, 22248.6938), (86.0, 25791.6866),
        (88.9, 27504.13), (100.0, 34058.67), (102.8, 35712.0667),
        (112.4, 41380.8553), (114.0, 42325.6534), (120.0, 45868.6463),
    ]
    dead = -22.8021
    edge = 7.0

    def interp(pts, x):
        # pts sorted ascending by x
        if x <= pts[0][0]:
            # extrapolate using first two
            x0, y0 = pts[0]
            x1, y1 = pts[1]
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        if x >= pts[-1][0]:
            x0, y0 = pts[-2]
            x1, y1 = pts[-1]
            return y1 + (y1 - y0) * (x - x1) / (x1 - x0)
        # binary search
        lo, hi = 0, len(pts) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if pts[mid][0] <= x:
                lo = mid
            else:
                hi = mid
        x0, y0 = pts[lo]
        x1, y1 = pts[hi]
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            if abs(x) <= edge:
                y = dead
            elif x > 0:
                y = interp(pos_pts, x)
            else:
                y = interp(neg_pts, x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
