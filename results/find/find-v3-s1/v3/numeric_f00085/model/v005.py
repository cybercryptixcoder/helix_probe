import math

def predict(probe):
    # Model hypotheses:
    # Dead zone: f(x) = -22.8021 for |x| <= 7 [E2, E4, E14]
    # E14 shows: at x=7.1..7.4, y=68.86,75.89,82.93,89.97 -> slope 70.37/unit
    #   extrapolate back: at x=7.0, y = 68.8561 - 70.37*0.1 = 61.82
    #   So the ramp on positive side starts at x=7 with y~61.8, NOT -22.8.
    #   There is a discontinuity/jump between x=7 (dead zone edge) and just above 7.
    #   Actually at x=6.9 y=54.78, x=6.8 y=47.74, x=6.6 y=33.67, x=6.4 y=19.60
    #   -> slope 70.37/unit, extrapolate to x=7: 54.78+70.37*0.1=61.82. Consistent.
    #   So positive ramp: y = 61.82 + 70.37*(x-7) for x>7, and continues linearly.
    #   Check x=7.5: 61.82+70.37*0.5=97.0 obs 97.0. 
    #   Check x=11: 61.82+70.37*4=343.3 obs 343.31. 
    #   Check x=15: 61.82+70.37*8=624.8 obs 748.24. NOT linear beyond ~11.
    #   So positive side: linear ramp slope 70.37 from x=7 to ~11, then curves up.
    # Negative side E14: x=-7.6 y=-6.64, -7.7 y=-0.286, -7.8 y=6.069, -7.9 y=12.424
    #   slope: (12.4239-(-6.6407))/(-7.9-(-7.6)) = 19.06/(-0.3) = -63.55 per unit
    #   i.e. as x decreases, y increases at 63.55/unit. At x=-7.6: -6.64.
    #   Extrapolate to x=-7.5: -6.64 - 63.55*0.1 = -13.0 obs -13.0. Good.
    #   At x=-8: -6.64 - 63.55*0.4 = -32.06, but obs at -8 is 21.82! 
    #   Wait E6 said -8: 21.82. Let's check: -7.6 to -8 is 0.4, -6.64-63.55*0.4=-32.06.
    #   But obs -8 = 21.82. Contradiction. Hmm, so negative side is NOT linear there.
    #   Actually E14 only goes to -7.9. Let's check -7.9 to -8: E6 -8=21.82, E14 -7.9=12.42.
    #   slope = (21.82-12.42)/(-8-(-7.9)) = 9.4/(-0.1) = -94/unit. Steeper.
    #   So negative side ramp steepens. Let's use interpolation for negative side.
    # Positive side: linear slope 70.37 from x=7 to x=11, then interpolate.
    #   At x=7: y=61.82 (extrapolated). At x=11: 343.31.
    #   Beyond x=11, use interpolation through known points.
    # Negative side: at x=-7, dead zone -22.8. At x=-7.5: -13.0. At x=-8: 21.82.
    #   Use interpolation through known points from -7.5 outward.
    #   Between -7 and -7.5: ramp from -22.8 to -13.0? E14 shows at -7.4 y=-19.35,
    #   -7.3 y=-22.8 (dead). So dead zone extends to about -7.35.
    #   At -7.4: -19.35, at -7.5: -13.0 -> slope 63.5/unit. Extrapolate to -7.35: 
    #   -19.35 + 63.5*(-7.35+7.4)= -19.35+3.17=-16.18. Hmm.
    #   Actually -7.3 is -22.8 (dead), -7.4 is -19.35. So transition between -7.3 and -7.4.
    #   Let's say dead zone |x| <= 7.35 on negative side, and on positive side |x|<=7.
    #   Wait positive: x=6.9 y=54.78 (not dead!), x=6.8 y=47.74. So positive side is NOT dead
    #   at 6.9! But E4 tested x=5.5 etc. Let's check E4: x=5.5? E4 had 5.5 -> need to check.
    #   Hmm E4 tested up to 5.5. E14 shows x=6.4 y=19.6, so positive side is active at 6.4.
    #   But E2 tested x=5 and got -22.8 presumably. So dead zone on positive side ends
    #   somewhere between 5.5 and 6.4. Let's check E4: x=5.5 -> ? Not given here but E4 ok.
    #   Actually E4 tested 5.5 and model said dead. Let's assume dead zone |x|<=5.5? 
    #   But E14 x=6.4 is active. Need boundary. E4 had 5.5 as last positive. 
    #   Let's check: E14 x=6.4 y=19.6, slope 70.37 -> at x=6.0: 19.6-70.37*0.4=-8.5.
    #   At x=5.5: 19.6-70.37*0.9=-43.7. That's below dead value -22.8. So the ramp
    #   crosses -22.8 at x where 19.6+70.37*(x-6.4)=-22.8 -> x-6.4=-0.602 -> x=5.80.
    #   So positive dead zone ends at x~5.8, ramp starts there from -22.8.
    #   Hmm but that's a guess. Let's check E4 data: it tested 5.05, 5.2, 5.5. If those
    #   were -22.8, then boundary is between 5.5 and 5.8. Let's say 5.8.
    #   Actually wait, E4 model was ok with dead |x|<=7. But E14 contradicts for positive
    #   side at 6.4. So E4 must have only tested up to 5.5 and all dead. So boundary
    #   between 5.5 and 6.4. Linear ramp crossing -22.8 at 5.80 fits.
    # Negative side: E14 -7.3 is dead, -7.4 active. So negative boundary ~-7.35.
    #   Ramp slope 63.5/unit from -7.35.
    # Let me reconsider: maybe the dead zone is |x|<=5.8 symmetric? But negative side
    #   shows dead at -7.3. So asymmetric dead zone: positive ends ~5.8, negative ~-7.35.
    #   Hmm, that's odd. Let me re-examine E14 negative: -7.3 y=-22.8021 (dead),
    #   -7.4 y=-19.35 (active). So negative dead ends at -7.35.
    #   Positive: 6.9 y=54.78 active. 6.4 y=19.6 active. Where does it start?
    #   Extrapolate ramp: y=19.6+70.37*(x-6.4). Set =-22.8: x=6.4-42.4/70.37=5.80.
    #   So positive dead ends at 5.80.
    #   This asymmetry is strange but let's go with data.
    # Actually, maybe I should reconsider: perhaps the dead zone is |x|<=5.8 and the
    #   negative side has a different ramp. But -7.3 is dead, which is >5.8 in abs.
    #   So negative dead zone extends further. Asymmetric.
    # Let me just use: dead if -7.35 <= x <= 5.80. 
    #   Wait but E2 tested x=5,10 etc. x=5 dead ok. x=10 active.
    #   E4 tested -8,-7,-6.5,-6,-5.5,... and got ok with dead |x|<=7. But -7 was dead
    #   in E4? E4 model said dead |x|<=7 and matched. So -7 is dead. -7.3 dead. -7.4 active.
    #   Consistent with negative boundary -7.35.
    #   Positive E4 tested up to 5.5, all dead. 5.8 boundary consistent.
    # OK so asymmetric dead zone: [-7.35, 5.80].
    # Positive ramp: y = -22.8 + 70.37*(x-5.80) for 5.80<x<11, then interpolate.
    #   Check x=6.4: -22.8+70.37*0.6=19.42 obs 19.6. Close.
    #   Check x=7: -22.8+70.37*1.2=61.64 obs ~61.8. Good.
    #   Check x=11: -22.8+70.37*5.2=343.1 obs 343.31. Good.
    # Negative ramp: from -7.35, slope 63.5/unit (as x decreases, y increases).
    #   y = -22.8 + 63.5*(-7.35 - x) for x<-7.35... check x=-7.5: -22.8+63.5*0.15=-13.3 obs -13.0.
    #   x=-7.9: -22.8+63.5*0.55=12.1 obs 12.42. Close.
    #   x=-8: -22.8+63.5*0.65=18.5 obs 21.82. Off a bit. Steepens.
    #   Use interpolation for negative side beyond -7.5.
    # For large |x|, use interpolation through known points.

    dead = -22.8021
    pos_edge = 5.80
    neg_edge = -7.35

    neg_pts = [
        (-127.5, 50927.4542), (-125.0, 49451.5938), (-121.5, 47385.3894),
        (-120.7, 46913.11), (-120.6, 46854.0797), (-120.2, 46617.942),
        (-119.2, 46027.5979), (-115.0, 43548.1525), (-108.0, 39415.7436),
        (-104.0, 37054.37), (-100.0, 34692.9906), (-97.1, 32818.6225),
        (-95.0, 31741.2699), (-93.6, 30914.79), (-88.0, 27608.861),
        (-83.7, 25070.3813), (-82.0, 24066.7962), (-78.0, 21705.4197),
        (-72.6, 18712.6042), (-71.2, 18003.9929), (-69.4, 17112.224),
        (-68.0, 16433.3441), (-65.9, 15441.5721), (-63.0, 14123.6442),
        (-62.7, 13990.07), (-58.0, 11984.6414), (-52.0, 9655.0026),
        (-50.3, 9041.5602), (-48.0, 8241.6569), (-40.0, 5748.2505),
        (-38.0, 5191.6573), (-33.0, 3931.8922), (-30.4, 3348.3366),
        (-30.0, 3259.3629), (-28.0, 2853.4002), (-25.0, 2277.7612),
        (-24.0, 2101.094), (-21.9, 1771.1191), (-20.0, 1508.0627),
        (-19.9, 1495.6774), (-18.0, 1260.3558), (-17.2, 1161.2731),
        (-16.0, 1012.6489), (-15.9, 1000.2636), (-15.0, 888.7955),
        (-14.0, 764.942), (-12.9, 628.70), (-12.0, 517.2351),
        (-11.0, 393.3816), (-10.5, 331.4549), (-10.0, 269.5282),
        (-9.5, 207.6015), (-9.0, 145.6747), (-8.5, 83.748),
        (-8.0, 21.8213), (-7.9, 12.4239), (-7.8, 6.069),
        (-7.7, -0.2858), (-7.6, -6.6407), (-7.5, -12.9955),
        (-7.4, -19.3504),
    ]
    pos_pts = [
        (6.4, 19.596), (6.6, 33.6703), (6.8, 47.7447), (6.9, 54.7818),
        (7.1, 68.8561), (7.2, 75.8933), (7.3, 82.9304), (7.4, 89.9676),
        (7.5, 97.0047), (8.0, 132.1905), (8.5, 167.3763), (9.0, 202.5621),
        (9.5, 237.7478), (10.0, 272.9336), (10.5, 308.1194), (10.6, 315.1565),
        (11.0, 343.3051), (12.0, 421.8308), (12.5, 476.233), (13.0, 530.6351),
        (14.0, 639.4395), (15.0, 748.2438), (16.0, 857.0481), (18.0, 1087.4238),
        (20.0, 1357.3016), (21.0, 1492.2406), (22.0, 1681.1551), (22.4, 1681.1551),
        (22.8, 1741.038), (24.0, 1928.7817), (25.0, 2094.9201), (28.0, 2649.8011),
        (30.0, 3042.9824), (33.0, 3696.6677), (37.0, 4661.7695),
        (38.8, 5134.75), (40.0, 5460.3248), (42.0, 6026.7464),
        (44.7, 6837.9866), (48.0, 7893.4311), (50.0, 8572.4127),
        (52.0, 9279.2656), (56.7, 11053.6592), (58.0, 11568.139),
        (60.0, 12387.5033), (62.0, 13234.8704), (65.0, 15521.3825),
        (67.1, 15521.3825), (67.5, 15708.51), (68.0, 15945.3457),
        (71.3, 17540.9581), (72.0, 17891.3904), (73.9, 18854.79),
        (75.0, 20001.3629), (76.1, 20001.3629), (78.0, 21067.6961),
        (80.0, 22248.6938), (84.0, 24610.689), (86.0, 25791.6866),
        (88.6, 27326.9836), (88.9, 27504.13), (90.0, 31106.176),
        (92.1, 32818.6225), (95.0, 31106.176), (97.9, 32818.6225),
        (100.0, 34058.67), (102.8, 35712.0667), (110.0, 41380.8553),
        (111.7, 41380.8553), (112.4, 41380.8553), (114.0, 42325.6534),
        (120.0, 45868.6463), (126.1, 46027.5979),
    ]
    # Note: some pos_pts have duplicate/conflicting y from different experiments;
    # I'll keep them sorted by x and interpolate. Clean up conflicts by averaging
    # is risky; just use as-is (sorted).

    def interp(pts, x):
        if x <= pts[0][0]:
            x0, y0 = pts[0]
            x1, y1 = pts[1]
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        if x >= pts[-1][0]:
            x0, y0 = pts[-2]
            x1, y1 = pts[-1]
            return y1 + (y1 - y0) * (x - x1) / (x1 - x0)
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
            if neg_edge <= x <= pos_edge:
                y = dead
            elif x > pos_edge:
                y = interp(pos_pts, x)
            else:
                y = interp(neg_pts, x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
