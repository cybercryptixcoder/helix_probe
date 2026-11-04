def predict(probe):
    # Flat region: y = -22.8021 for |x| <= ~6 (E1: x=2.9,-6.0; E2: -6,±3,±1,0 all -22.8021)
    # At |x|=8: y=21.82 (pos) and 132.19 (neg) -> asymmetric, so not pure x^2
    # At |x|=10: 269.53 (neg) vs 272.93 (pos) -> nearly symmetric
    # At |x|=12: 517.24 (neg) vs 421.83 (pos) -> asymmetric again
    # At |x|=14: 764.94 (neg) vs 639.44 (pos)
    # At |x|=16: 1012.65 (neg) vs 857.05 (pos)
    # At |x|=18: 1260.36 (neg) vs 1087.42 (pos)
    # At |x|=30: 3042.98
    # E1: 20.3->1545.22, 21.3->1532.72, 24.3->2154.09, 50.4->9077.30, 61.7->13550.62, 66->15014.02, 72.7->18241.82, 88.2->27090.78
    # Looks like y = a*x^2 + b*x + c outside flat region, with a~3.5
    # Check: 88.2^2*3.5=27237, close to 27090. 66^2*3.5=15246 vs 15014.
    # Try fitting quadratic on large |x|: use 88.2, 72.7, 66, 61.7
    # Differences suggest slight asymmetry. Let's fit a*x^2 + b*x + c.
    # Using 88.2: 7779.24a + 88.2b + c = 27090.78
    # Using 72.7: 5285.29a + 72.7b + c = 18241.82
    # Using 66:   4356a + 66b + c = 15014.02
    # Subtract: (7779.24-5285.29)a + 15.5b = 8848.96 -> 2493.95a + 15.5b = 8848.96
    #           (5285.29-4356)a + 6.7b = 3227.80 -> 929.29a + 6.7b = 3227.80
    # From second: b = (3227.80 - 929.29a)/6.7
    # Sub: 2493.95a + 15.5*(3227.80-929.29a)/6.7 = 8848.96
    # 2493.95a + 2.3134*(3227.80-929.29a) = 8848.96
    # 2493.95a + 7467.5 - 2149.9a = 8848.96
    # 344.05a = 1381.46 -> a = 4.015
    # Hmm that's higher. Let me try with 88.2, 66, 50.4
    # 7779.24a + 88.2b + c = 27090.78
    # 4356a + 66b + c = 15014.02
    # 2540.16a + 50.4b + c = 9077.30
    # Sub1: 3423.24a + 22.2b = 12076.76
    # Sub2: 1815.84a + 15.6b = 5936.72
    # From sub2: b = (5936.72 - 1815.84a)/15.6
    # Sub: 3423.24a + 22.2*(5936.72-1815.84a)/15.6 = 12076.76
    # 3423.24a + 1.4231*(5936.72-1815.84a) = 12076.76
    # 3423.24a + 8448.6 - 2584.0a = 12076.76
    # 839.24a = 3628.16 -> a = 4.323
    # Inconsistent. The function isn't a clean quadratic - it's an MLP approximation.
    # Let's just interpolate from data points. Use piecewise linear on |x| with asymmetry.
    # Actually let's look at the negative side more carefully:
    # -16: 1012.65, -14: 764.94, -12: 517.24, -10: 269.53, -8: 21.82, -6: -22.80
    # Differences: 247.71, 247.70, 247.71, 247.71, 44.62
    # Wow, linear! Slope ~247.7 per unit from -16 to -8. Then flat below -6.
    # Positive side: 6: -8.55, 8: 132.19, 10: 272.93, 12: 421.83, 14: 639.44, 16: 857.05, 18: 1087.42
    # Differences: 140.74, 140.74, 148.90, 217.61, 217.61, 230.37
    # Hmm, not linear. Let me check: 6->8: 140.74, 8->10: 140.74, 10->12: 148.90
    # 12->14: 217.61, 14->16: 217.61, 16->18: 230.37
    # Interesting, seems like it's piecewise linear with breakpoints.
    # Actually maybe it's x^2 with different scaling? Let's check x^2 differences:
    # 6^2=36, 8^2=64, 10^2=100, 12^2=144, 14^2=196, 16^2=256, 18^2=324
    # y values: -8.55, 132.19, 272.93, 421.83, 639.44, 857.05, 1087.42
    # Fit y = a*x^2 + c on positive: 
    # 36a+c=-8.55, 324a+c=1087.42 -> 288a=1095.97 -> a=3.806, c=-145.5
    # Check 100: 380.6-145.5=235.1 vs 272.93. Not great.
    # Try a*x^2+b*x+c on positive using 6,12,18:
    # 36a+6b+c=-8.55
    # 144a+12b+c=421.83
    # 324a+18b+c=1087.42
    # Sub: 108a+6b=430.38 -> 18a+b=71.73
    # Sub: 180a+6b=665.59 -> 30a+b=110.93
    # 12a=39.2 -> a=3.267, b=71.73-58.8=12.93, c=-8.55-117.6-77.6=-203.75
    # Check 8: 3.267*64+12.93*8-203.75=209.1+103.4-203.75=108.75 vs 132.19. Off by 23.
    # Check 10: 326.7+129.3-203.75=252.25 vs 272.93. Off by 20.
    # Check 14: 640.3+181-203.75=617.55 vs 639.44. Off by 22.
    # Check 16: 836.4+206.9-203.75=839.55 vs 857.05. Off by 17.5.
    # Reasonable but not exact. MLP approximation.
    # Negative side: -6:-22.80, -8:21.82, -10:269.53, -12:517.24, -14:764.94, -16:1012.65
    # Fit a*x^2+b*x+c using -6,-12,-16:
    # 36a-6b+c=-22.80
    # 144a-12b+c=517.24
    # 256a-16b+c=1012.65
    # Sub: 108a-6b=540.04 -> 18a-b=90.01
    # Sub: 112a-4b=495.41 -> 28a-b=123.85
    # 10a=33.84 -> a=3.384, b=18*3.384-90.01=60.91-90.01=-29.10
    # c=-22.80-36*3.384+6*(-29.10)=-22.80-121.82-174.6=-319.22
    # Check -8: 3.384*64-29.10*(-8)-319.22=216.58+232.8-319.22=130.16 vs 21.82. Off by 108!
    # Hmm. Let me reconsider. Negative side looks very linear from -8 to -16.
    # Slope 247.7. At -8: 21.82. So y = 21.82 + 247.7*(-x-8) for x<-8? 
    # At -16: 21.82+247.7*8=2003.4. No, that's wrong. 21.82+247.7*8=2003.4 vs 1012.65.
    # Wait, differences are 247.7 per 2 units, so slope is 123.85 per unit.
    # At -16: 21.82+123.85*8=1012.6. Yes! 
    # So negative side: y = 21.82 + 123.85*(-x-8) for x in [-16,-8]. Linear!
    # At -6: 21.82+123.85*(-2)=21.82-247.7=-225.88. But observed -22.80. So not linear below -8.
    # So flat region ends around -6 to -8. At -6 it's -22.80 (flat), at -8 it's 21.82.
    # Positive side: 6:-8.55, 8:132.19. Difference 140.74 over 2 units = 70.37/unit.
    # 8->10: 140.74 (70.37/unit). 10->12: 148.90 (74.45/unit). 12->14: 217.61 (108.8/unit).
    # 14->16: 217.61 (108.8/unit). 16->18: 230.37 (115.2/unit).
    # So positive side is piecewise linear with increasing slope. Not clean.
    # Let me check E1 large values against x^2:
    # 20.3^2=412.09, y=1545.22 -> ratio 3.75
    # 21.3^2=453.69, y=1532.72 -> ratio 3.38
    # 24.3^2=590.49, y=2154.09 -> ratio 3.65
    # 50.4^2=2540.16, y=9077.30 -> ratio 3.573
    # 61.7^2=3806.89, y=13550.62 -> ratio 3.560
    # 66^2=4356, y=15014.02 -> ratio 3.447
    # 72.7^2=5285.29, y=18241.82 -> ratio 3.451
    # 88.2^2=7779.24, y=27090.78 -> ratio 3.482
    # Ratio ~3.5 for large x. 
    # Let's check if y = 3.5*x^2 - 22.8 for large x:
    # 88.2: 3.5*7779.24-22.8=27204.5 vs 27090.78. Off by 114.
    # 66: 3.5*4356-22.8=15223.2 vs 15014.02. Off by 209.
    # 50.4: 3.5*2540.16-22.8=8867.76 vs 9077.30. Off by -210.
    # Hmm, mixed signs. Maybe there's a linear term.
    # Let's fit y = a*x^2 + b*x + c on large positive x using 88.2, 66, 50.4:
    # 7779.24a+88.2b+c=27090.78
    # 4356a+66b+c=15014.02
    # 2540.16a+50.4b+c=9077.30
    # Sub1: 3423.24a+22.2b=12076.76
    # Sub2: 1815.84a+15.6b=5936.72
    # From sub2: b=(5936.72-1815.84a)/15.6
    # 3423.24a+22.2*(5936.72-1815.84a)/15.6=12076.76
    # 3423.24a+1.4231*(5936.72-1815.84a)=12076.76
    # 3423.24a+8448.6-2584.0a=12076.76
    # 839.24a=3628.16 -> a=4.323, b=(5936.72-7845.6)/15.6=-122.4
    # c=15014.02-4356*4.323-66*(-122.4)=15014.02-18831+8078.4=4261.4
    # Check 72.7: 4.323*5285.29-122.4*72.7+4261.4=22848-8898+4261=18211 vs 18241.82. Close!
    # Check 61.7: 4.323*3806.89-122.4*61.7+4261.4=16457-7552+4261=13166 vs 13550.62. Off by 384.
    # Not great. MLP is not a clean quadratic.
    # Given the complexity, let me use a piecewise linear interpolation approach based on all data.
    # Actually, let me reconsider. The negative side from -8 to -16 is very linear (slope 123.85).
    # Let me check E1 negative values: -20.3:1545.22, -24.3:2154.09, -50.4:9077.30, -61.7:13550.62
    # From -16 (1012.65) to -20.3 (1545.22): slope (1545.22-1012.65)/4.3=123.85! Same slope!
    # From -20.3 to -24.3: (2154.09-1545.22)/4=152.2. Different.
    # Hmm. -24.3 to -50.4: (9077.30-2154.09)/26.1=265.3. 
    # So the slope increases with |x|. It's roughly quadratic overall.
    # Let me just fit a quadratic to all negative data points and see.
    # Actually, let me take a different approach: fit a*x^2+b*x+c to the whole thing using least squares mentally is hard.
    # Let me try: y = 3.5*x^2 - 22.8 for |x|>8, and flat for |x|<=6, and interpolate 6-8.
    # But E2 shows asymmetry: at 12, pos=421.83, neg=517.24. At 16, pos=857.05, neg=1012.65.
    # Difference: 95.41 at 12, 155.6 at 16. So negative side is higher.
    # This suggests a linear term: y = a*x^2 + b*x + c with b<0 (so negative x gives higher).
    # Let's fit using 16 (pos 857.05, neg 1012.65) and 12 (pos 421.83, neg 517.24):
    # 256a+16b+c=857.05
    # 256a-16b+c=1012.65
    # 144a+12b+c=421.83
    # 144a-12b+c=517.24
    # From 1&2: 32b=-155.6 -> b=-4.8625
    # From 3&4: 24b=-95.41 -> b=-3.975
    # Inconsistent b. So not a clean quadratic.
    # Let me just use interpolation. I'll build a lookup table from all data and interpolate.
    # Data points (x, y):
    data = [
        (-61.7, 13550.6196), (-50.4, 9077.3007), (-24.3, 2154.0941), (-20.3, 1545.2188),
        (-18, 1260.3558), (-16, 1012.6489), (-14, 764.942), (-12, 517.2351), (-10, 269.5282),
        (-8, 21.8213), (-6, -22.8021), (-3, -22.8021), (-1, -22.8021), (0, -22.8021),
        (1, -22.8021), (3, -22.8021), (2.9, -22.8021), (-6.0, -22.8021),
        (6, -8.5526), (8, 132.1905), (10, 272.9336), (12, 421.8308), (14, 639.4395),
        (16, 857.0481), (18, 1087.4238), (20.3, 1545.2188), (21.3, 1532.7222),
        (24.3, 2154.0941), (30, 3042.9824), (50.4, 9077.3007), (61.7, 13550.6196),
        (66.0, 15014.0187), (72.7, 18241.8226), (88.2, 27090.784),
    ]
    # Sort by x
    data.sort()
    xs = [d[0] for d in data]
    ys = [d[1] for d in data]
    
    def interp(x):
        if x <= xs[0]:
            # extrapolate using last two
            return ys[0] + (ys[1]-ys[0])/(xs[1]-xs[0])*(x-xs[0])
        if x >= xs[-1]:
            return ys[-1] + (ys[-1]-ys[-2])/(xs[-1]-xs[-2])*(x-xs[-1])
        # binary search
        lo, hi = 0, len(xs)-1
        while hi-lo > 1:
            mid = (lo+hi)//2
            if xs[mid] <= x:
                lo = mid
            else:
                hi = mid
        # linear interpolation
        return ys[lo] + (ys[hi]-ys[lo])/(xs[hi]-xs[lo])*(x-xs[lo])
    
    out = []
    for x in probe["x"]:
        out.append(interp(x))
    return {"y": out}
