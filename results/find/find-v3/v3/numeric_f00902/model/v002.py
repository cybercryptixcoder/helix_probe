import math

def predict(probe):
    # Observations / beliefs:
    # E2: for |x| small (<~2), y is around -48 and slowly varying: looks like a smooth
    #     low-order polynomial / trig-ish baseline. Values: f(0)=-48.6, f(0.5)=-48.6625,
    #     f(-0.5)=-47.3875, f(1)=-46.6, f(-1)=-46.0, f(1.5)=-41.4375, f(-1.5)=-45.4125.
    #     These are small compared to the huge growth for large |x|.
    # E2: for |x| >= 3, y grows very fast and alternates sign with x:
    #     f(3)=2.4, f(-3)=-58.2, f(5)=163.4, f(-5)=-145.6, f(10)=1465.4, f(-10)=-1102.6,
    #     f(20)=11239.4, f(-20)=-9496.6, f(30)=37073.4, f(-30)=-33030.6,
    #     f(40)=86767.4, f(-40)=-79504.6, f(50)=168121.4.
    #     The odd symmetry is approximate but not exact. Growth looks like ~ x^3 with
    #     leading coefficient ~1.35 (50^3=125000, 168121/125000=1.345; 40^3=64000,
    #     86767/64000=1.356; 30^3=27000, 37073/27000=1.373; 20^3=8000, 11239/8000=1.405).
    # E1: large magnitudes: f(88.2)=909670.19, 88.2^3=686128, ratio 1.326;
    #     f(66)=383609.4, 66^3=287496, ratio 1.334; f(72.7)=511504, 72.7^3=384400, ratio 1.331.
    #     For negative: f(-61.7)=-296544.68, |x|^3=234885, ratio 1.262;
    #     f(-50.4)=-160556.88, 50.4^3=128024, ratio 1.254; f(-24.3)=-17305.17, 24.3^3=14349, ratio 1.206.
    #     So positive side ~1.33 x^3, negative side ~1.25 |x|^3, with extra terms.
    # E1 small: f(2.9)=-2.1913 (near the transition), f(-6.0)=-237.0, f(21.3)=13523.48.
    #     f(-6)=-237: -6^3=-216, ratio 1.097 (close to the negative cubic branch).
    #     f(21.3)=13523.48: 21.3^3=9663.6, ratio 1.399.
    # Conclusion: there is a central region (|x| <~ 2.5-3) where f is a mild smooth
    # function near -48, and outside it f is dominated by an odd cubic-like term with
    # slightly different coefficients for positive and negative x. There is a jump /
    # transition around |x| ~ 2.5-3 (f(3)=2.4 vs f(1.5)=-41.4, big gap).
    # I model: central region |x| <= 2.5: quadratic fit through the E2 small points;
    # outside: cubic plus linear/constant correction, with separate pos/neg coefficients.
    # The exact transition boundary is uncertain; I pick 2.5.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        if abs(x) <= 2.5:
            # Central smooth region. Fit from E2 small points:
            # f(0)=-48.6, f(1)=-46.6, f(-1)=-46.0, f(1.5)=-41.4375, f(-1.5)=-45.4125
            # Use a quadratic a + b x + c x^2. From f(0)=-48.6 -> a=-48.6.
            # f(1)=-46.6: b + c = 2.0
            # f(-1)=-46.0: -b + c = 2.6 -> c = 2.3, b = -0.3
            # Check f(1.5): -48.6 -0.45 + 2.3*2.25 = -48.6 -0.45 +5.175 = -43.875
            #   observed -41.4375, off by 2.4. f(-1.5): -48.6 +0.45+5.175=-42.975 vs -45.4125.
            # The region is not perfectly quadratic; use cubic too.
            # Fit cubic through f(0), f(1), f(-1), f(1.5):
            # a=-48.6; b+c+d=2.0; -b+c-d=2.6; 1.5b+2.25c+3.375d=7.1625
            # From first two: c=2.3, b+d=-0.3.
            # Third: 1.5b+5.175+3.375d=7.1625 -> 1.5b+3.375d=1.9875
            # b=-0.3-d: -0.45-1.5d+3.375d=1.9875 -> 1.875d=2.4375 -> d=1.3, b=-1.6
            # So central: -48.6 -1.6x +2.3x^2 +1.3x^3
            # Check f(-1.5): -48.6+2.4+5.175-4.3875=-45.4125 exact! Good.
            # Check f(0.5): -48.6-0.8+0.575+0.1625=-48.6625 exact! Great.
            # Check f(-0.5): -48.6+0.8+0.575-0.1625=-47.3875 exact!
            # So central polynomial is exact for E2 small points:
            y = -48.6 - 1.6*x + 2.3*x*x + 1.3*x*x*x
        else:
            # Outer cubic branch. Fit using E2 and E1 large points.
            # Positive branch: y ~ A x^3 + B x^2 + C x + D
            # Use points (3,2.4), (5,163.4), (10,1465.4), (20,11239.4), (50,168121.4),
            # (21.3,13523.4831), (66,383609.4), (72.7,511504.0049), (88.2,909670.1904)
            # Try fitting y = a x^3 + b x^2 + c x + d via least squares mentally is hard;
            # use leading coefficient ~1.33 and a quadratic correction.
            # From (10,1465.4): 1330 + 100b + 10c + d = 1465.4
            # From (20,11239.4): 10640 + 400b + 20c + d = 11239.4
            # From (50,168121.4): 166250 + 2500b + 50c + d = 168121.4
            # Subtract: (20)-(10): 9310 + 300b + 10c = 9774 -> 300b+10c=464
            # (50)-(20): 155610 + 2100b + 30c = 156882 -> 2100b+30c=1272
            # From first: 30b + c = 46.4 -> c = 46.4 - 30b
            # Second: 2100b + 30(46.4-30b)=1272 -> 2100b+1392-900b=1272 -> 1200b=-120 -> b=-0.1
            # c = 46.4 + 3 = 49.4
            # d from (10): 1330 -10 +494 + d =1465.4 -> 1814+d=1465.4 -> d=-348.6
            # Check (3): 1.33*27 -0.1*9 +49.4*3 -348.6 = 35.91 -0.9 +148.2 -348.6 = -165.39
            #   observed 2.4. Bad near 3. So a single cubic doesn't fit near the transition.
            # The transition region likely has a different behavior. Use a blend:
            # For 2.5 < |x| < 5, interpolate between central value at 2.5 and cubic at 5.
            # But E2 has f(3)=2.4 and f(5)=163.4; f(3) is much lower than cubic predicts.
            # Maybe there's a smooth ramp. Let's fit a cubic to (3,2.4),(5,163.4),(10,1465.4),
            # (20,11239.4): a*27+b*9+c*3+d=2.4; a*125+b*25+c*5+d=163.4;
            # a*1000+b*100+c*10+d=1465.4; a*8000+b*400+c*20+d=11239.4
            # Subtract: (5)-(3): 98a+16b+2c=161 -> 49a+8b+c=80.5
            # (10)-(5): 875a+75b+5c=1302 -> 175a+15b+c=260.4
            # (20)-(10): 7000a+300b+10c=9774 -> 700a+30b+c=977.4
            # Subtract eq2-eq1: 126a+7b=179.9 -> 18a+b=25.7
            # eq3-eq2: 525a+15b=717 -> 35a+b=47.8
            # Subtract: 17a=22.1 -> a=1.3, b=25.7-23.4=2.3, c=80.5-49*1.3-8*2.3=80.5-63.7-18.4=-1.6
            # d from (3): 1.3*27+2.3*9-1.6*3+d=2.4 -> 35.1+20.7-4.8+d=2.4 -> 51+d=2.4 -> d=-48.6
            # Wow: positive branch is exactly the same polynomial as central!
            # Check (50): 1.3*125000 + 2.3*2500 -1.6*50 -48.6 = 162500+5750-80-48.6=168121.4 exact!
            # Check (66): 1.3*287496 + 2.3*4356 -1.6*66 -48.6 = 373744.8+10018.8-105.6-48.6=383609.4 exact!
            # Check (88.2): 1.3*686128.368 + 2.3*7779.24 -1.6*88.2 -48.6 = 891966.8784+17892.252-141.12-48.6=909669.4104, observed 909670.1904, off by 0.78. Close enough (rounding).
            # So positive side is the SAME cubic polynomial everywhere!
            # Now negative side: f(-3)=-58.2, f(-5)=-145.6, f(-10)=-1102.6, f(-20)=-9496.6,
            # f(-30)=-33030.6, f(-40)=-79504.6, f(-50)=-1102.6? No f(-50) not given; f(-50.4)=-160556.8752
            # f(-61.7)=-296544.6799, f(-24.3)=-17305.1721, f(-6)=-237.0
            # Try same polynomial form with different coefficients: y = a x^3 + b x^2 + c x + d
            # Use (-3,-58.2), (-5,-145.6), (-10,-1102.6), (-20,-9496.6)
            # a(-27)+b(9)+c(-3)+d=-58.2
            # a(-125)+b(25)+c(-5)+d=-145.6
            # a(-1000)+b(100)+c(-10)+d=-1102.6
            # a(-8000)+b(400)+c(-20)+d=-9496.6
            # Subtract: (-5)-(-3): -98a+16b-2c=-87.4 -> 49a-8b+c=43.7
            # (-10)-(-5): -875a+75b-5c=-957 -> 175a-15b+c=191.4
            # (-20)-(-10): -7000a+300b-10c=-8394 -> 700a-30b+c=839.4
            # eq2-eq1: 126a-7b=147.7 -> 18a-b=21.1
            # eq3-eq2: 525a-15b=648 -> 35a-b=43.2
            # Subtract: 17a=22.1 -> a=1.3, b=18*1.3-21.1=23.4-21.1=2.3, c=43.7-49*1.3+8*2.3=43.7-63.7+18.4=-1.6
            # d from (-3): 1.3*(-27)+2.3*9-1.6*(-3)+d=-58.2 -> -35.1+20.7+4.8+d=-58.2 -> -9.6+d=-58.2 -> d=-48.6
            # Same polynomial! Check (-30): 1.3*(-27000)+2.3*900-1.6*(-30)-48.6 = -35100+2070+48-48.6=-33030.6 exact!
            # Check (-40): 1.3*(-64000)+2.3*1600+64-48.6=-83200+3680+64-48.6=-79504.6 exact!
            # Check (-50.4): 1.3*(-128024.064)+2.3*2540.16+80.64-48.6=-166431.2832+5842.368+80.64-48.6=-160556.8752 exact!
            # Check (-61.7): 1.3*(-234885.113)+2.3*3806.89+98.72-48.6=-305350.6469+8755.847+98.72-48.6=-296544.6799 exact!
            # Check (-24.3): 1.3*(-14348.907)+2.3*590.49+38.88-48.6=-18653.5791+1358.127+38.88-48.6=-17305.1721 exact!
            # Check (-6): 1.3*(-216)+2.3*36+9.6-48.6=-280.8+82.8+9.6-48.6=-237.0 exact!
            # So the function is the SAME cubic polynomial everywhere: f(x)=1.3x^3+2.3x^2-1.6x-48.6
            # But wait, E2 small values matched this too? Check f(0.5): 1.3*0.125+2.3*0.25-0.8-48.6=0.1625+0.575-0.8-48.6=-48.6625 yes!
            # f(-1.5): 1.3*(-3.375)+2.3*2.25+2.4-48.6=-4.3875+5.175+2.4-48.6=-45.4125 yes!
            # So there is NO separate region; it's a single cubic polynomial everywhere.
            # The "transition" was just the natural cubic shape.
            y = 1.3*x*x*x + 2.3*x*x - 1.6*x - 48.6

        ys.append(y)

    return {"y": ys}
