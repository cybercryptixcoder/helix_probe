import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs (with evidence):
    # - For x >= 0: f(x) is a smooth, nearly linear function with slope ~12.9
    #   and a small offset. E4: f(50)=651.5, f(70)=912.5, f(90)=1175.5,
    #   f(110)=1436.5, f(127)=1658.2. Slope ~12.9, intercept ~6.
    #   E2 positive side: f(20)=257.5, f(40)=518.5, f(60)=782.5, f(80)=1042.5.
    #   E3/E5/E1 positive values also match (~12.9*x + ~6).
    # - For x < 0: f(x) is also nearly linear but with a different slope (~1.7)
    #   and offset. E2: f(-100)=-139.9, f(-80)=-114.7, f(-60)=-89.5,
    #   f(-40)=-63.3, f(-30)=-49.2, f(-20)=-37.1, f(-10)=-23.0.
    #   Slope ~1.7, intercept ~30. E6 negatives match too.
    # - There is a special region near x=0 where f is NOT on these lines.
    #   E2: f(0) = -382.12 (huge negative spike), f(-1)=-8.21, f(-2)=-11.52,
    #   f(-5)=-15.45, f(1)=7.6, f(2)=21.7, f(5)=61.0.
    #   E4: f(0.1)=-3.19, f(0.2)=-1.88, f(0.5)=2.05, f(0.8)=4.98, f(1)=7.6,
    #   f(1.5)=14.15, f(2)=21.7, f(3)=34.8, f(4)=48.9, f(6)=73.1, f(8)=99.3,
    #   f(12)=151.7.
    #   The positive side near 0 smoothly continues the ~12.9 slope line:
    #   12.9*1+6=18.9 vs 7.6; not quite. Let's fit better.
    #
    # Fit positive side more carefully using E4 small values:
    # x: 1,1.5,2,3,4,6,8,12 -> y: 7.6,14.15,21.7,34.8,48.9,73.1,99.3,151.7
    # Differences: 6.55,7.55,13.1,14.1,24.2,26.2,52.4 over dx 0.5,0.5,1,1,2,2,4
    # slopes: 13.1,15.1,13.1,14.1,12.1,13.1,13.1 -> ~13.0 slope, intercept ~ -5.4?
    # 13*1-5.4=7.6 yes! 13*2-5.4=20.6 vs 21.7 close. 13*12-5.4=150.6 vs 151.7.
    # Large positive: 13*50-5.4=644.6 vs 651.5. 13*127-5.4=1645.6 vs 1658.2.
    # Slight upward curvature. Use slope 13.02 and intercept -5.0:
    # 13.02*127-5=1648.5 vs 1658.2. Try slope 13.05, intercept -4.5:
    # 13.05*127-4.5=1652.85. slope 13.1, intercept -5: 13.1*127-5=1658.7 yes!
    # Check 50: 13.1*50-5=650 vs 651.5. 110: 13.1*110-5=1436 vs 1436.5 yes!
    # 1: 13.1-5=8.1 vs 7.6. 2: 26.2-5=21.2 vs 21.7. Good.
    # So positive side: f(x) = 13.1*x - 5 approximately.
    #
    # Negative side fit: E2: (-100,-139.9),(-80,-114.7),(-60,-89.5),(-40,-63.3),
    # (-30,-49.2),(-20,-37.1),(-10,-23.0). Slope: (139.9-114.7)/20=1.26?
    # Actually from -100 to -10: (139.9-23.0)/90 = 1.299. Intercept at 0: -23+1.3*10=-10?
    # Check: 1.3*(-100)+c=-139.9 -> c=-9.9. 1.3*(-10)-9.9=-22.9 yes.
    # So negative side: f(x) = 1.3*x - 10 for x <= -5 or so.
    # Check E6: f(-8)=-20.38: 1.3*-8-10=-20.4 yes! f(-4)=-14.14: 1.3*-4-10=-15.2 vs -14.14.
    # f(-3)=-14.83: 1.3*-3-10=-13.9 vs -14.83. Slight deviation near -3.
    #
    # Near zero (special region): E2 f(0)=-382.12 is a spike. E4 f(0.1)=-3.19,
    # f(0.2)=-1.88, f(0.5)=2.05, f(0.8)=4.98.
    # These small positive x values: 13.1*x-5 gives -3.69,-2.38,-1.45,5.48.
    # Close-ish for 0.1,0.2 but 0.5 gives 2.05 vs -1.45, 0.8 gives 4.98 vs 5.48.
    # Hmm. Let's fit small positive: 0.5->2.05, 0.8->4.98, 1->7.6, 1.5->14.15.
    # Slope between 0.5 and 1.5: (14.15-2.05)/1 = 12.1. Intercept: 2.05-12.1*0.5=-4.
    # So ~12.1*x-4. Check 0.8: 9.68-4=5.68 vs 4.98. 1: 8.1 vs 7.6.
    # Maybe there's curvature. Try quadratic fit? Probably overkill.
    #
    # The spike at 0: f(0)=-382.12. Could be 1/0-like or a special value.
    # Nearby: f(-1)=-8.21, f(1)=7.6. f(-2)=-11.52, f(2)=21.7.
    # The negative side near 0: f(-1)=-8.21, f(-2)=-11.52, f(-3)=-14.83,
    # f(-4)=-14.14, f(-5)=-15.45, f(-8)=-20.38.
    # For x=-1: 1.3*-1-10=-11.3 vs -8.21. For x=-2: -12.6 vs -11.52.
    # For x=-3: -13.9 vs -14.83. For x=-4: -15.2 vs -14.14.
    # There's a wiggle but roughly 1.3x-10.
    #
    # The spike at 0 is isolated: f(0)=-382.12. Maybe f(x) = 1.3x-10 + something
    # that blows up at 0? Like -382 at 0 but small nearby. Could be -382.12 * exp(-x^2/s)
    # but f(0.1) is -3.19 which is close to line 13.1*0.1-5=-3.69.
    # Actually maybe the spike is just at exactly 0, or a narrow Lorentzian.
    # E4 doesn't include 0. E2 includes 0 with -382.12.
    # Given only one data point at 0, model as: at x=0 exactly, return -382.12.
    # For 0<|x|<0.05 maybe interpolate? Risky. Use a narrow spike.
    #
    # Let's define:
    # region x >= 0: f(x) = 13.1*x - 5, except near 0 where a spike.
    # At x=0: -382.12.
    # For 0 < x < 0.1: blend? E4: f(0.1)=-3.19. Line gives -3.69. Close.
    # So spike is very narrow. Model spike as -382.12 * exp(-(x/0.02)^2) added to line?
    # At x=0.1: exp(-25)~0, fine. At x=0: -382.12 + (-5) = -387.12, not -382.12.
    # So spike value should be -382.12 - line(0) = -382.12 - (-5) = -377.12.
    # So f(x) = 13.1x - 5 - 377.12*exp(-(x/0.02)^2).
    # Check x=0: -5-377.12=-382.12 yes.
    #
    # Negative side: f(x) = 1.3x - 10 for x <= -5.
    # For -5 < x < 0: E2: f(-1)=-8.21, f(-2)=-11.52, f(-5)=-15.45.
    # Line 1.3x-10: -11.3, -12.6, -16.5. Deviations: +3.09, +1.08, +1.05.
    # E6: f(-3)=-14.83 (line -13.9, dev -0.93), f(-4)=-14.14 (line -15.2, dev +1.06),
    # f(-8)=-20.38 (line -20.4, dev +0.02).
    # There's a bump near -1 to -5. Maybe a small Gaussian bump?
    # f(-1)=-8.21 vs line -11.3: +3.09.
    # f(-2)=-11.52 vs -12.6: +1.08.
    # f(-3)=-14.83 vs -13.9: -0.93.
    # f(-4)=-14.14 vs -15.2: +1.06.
    # f(-5)=-15.45 vs -16.5: +1.05.
    # Noisy. Could be noise. The problem says output could be noisy.
    # Let's just use the line for x<0, with maybe a small correction.
    #
    # Actually check E1: x=-6.0 -> y=-18.76. Line 1.3*-6-10=-17.8. Close.
    # x=-20.3 -> -35.493. Line 1.3*-20.3-10=-36.39. Close.
    # x=-24.3 -> -41.733. Line -41.59. Close.
    # x=-50.4 -> -75.924. Line -75.52. Close.
    # x=-61.7 -> -91.727. Line -90.21. Close.
    # Good, negative line works.
    #
    # Check E5: x=-48.6 -> -73.566. Line 1.3*-48.6-10=-73.18. Close.
    # x=-7.1 -> -20.201. Line 1.3*-7.1-10=-19.23. Close.
    # x=-16.9 -> -31.039. Line -31.97. Close.
    # x=-102.2 -> -143.782. Line -142.86. Close.
    #
    # Positive check E1: x=88.2 -> 1149.92. Line 13.1*88.2-5=1150.42. Close.
    # x=66.0 -> 860.1. Line 13.1*66-5=859.6. Close.
    # x=2.9 -> 34.49. Line 13.1*2.9-5=32.99. Close.
    # x=72.7 -> 947.87. Line 13.1*72.7-5=947.37. Close.
    # x=21.3 -> 274.53. Line 13.1*21.3-5=274.03. Close.
    #
    # E3: x=104.5 -> 1363.45. Line 13.1*104.5-5=1363.95. Close.
    # x=1.2 -> 10.22. Line 13.1*1.2-5=10.72. Close.
    # x=65.5 -> 853.55. Line 13.1*65.5-5=853.05. Close.
    # x=30.3 -> 392.43. Line 13.1*30.3-5=391.93. Close.
    # x=104.9 -> 1368.69. Line 13.1*104.9-5=1369.19. Close.
    # x=123.6 -> 1614.66. Line 13.1*123.6-5=1614.16. Close.
    # x=79.4 -> 1034.64. Line 13.1*79.4-5=1035.14. Close.
    # x=103.0 -> 1343.8. Line 13.1*103-5=1344.3. Close.
    #
    # E5: x=58.8 -> 765.78. Line 13.1*58.8-5=765.28. Close.
    # x=102.1 -> 1333.01. Line 13.1*102.1-5=1332.51. Close.
    # x=47.1 -> 612.51. Line 13.1*47.1-5=612.01. Close.
    # x=28.4 -> 366.54. Line 13.1*28.4-5=367.04. Close.
    # x=105.7 -> 1379.17. Line 13.1*105.7-5=1379.67. Close.
    # x=119.5 -> 1560.95. Line 13.1*119.5-5=1560.45. Close.
    #
    # E6 positive: x=3 -> 34.8. Line 13.1*3-5=34.3. Close.
    # x=4 -> 48.9. Line 47.4. Close.
    # x=7 -> 86.2. Line 86.7. Close.
    # x=9 -> 113.4. Line 112.9. Close.
    # x=11 -> 139.6. Line 139.1. Close.
    # x=13 -> 164.8. Line 165.3. Close.
    # x=45 -> 584.0. Line 584.5. Close.
    # x=55 -> 718.0. Line 715.5. Close.
    # x=75 -> 978.0. Line 977.5. Close.
    # x=85 -> 1111.0. Line 1108.5. Close.
    # x=95 -> 1240.0. Line 1239.5. Close.
    #
    # So model:
    # - For x >= 0: f(x) = 13.1*x - 5, with a narrow spike at 0:
    #   subtract 377.12*exp(-(x/0.02)^2) to hit -382.12 at x=0.
    # - For x < 0: f(x) = 1.3*x - 10.
    # - The tiny deviations are noise.
    #
    # Boundary: x=0. At x=0 exactly, spike. For x>0 use positive line.
    # For x<0 use negative line.
    #
    # ? The spike width is guessed; only f(0) is known to be -382.12.
    # ? The small deviations near 0 on negative side are treated as noise.

    def f(x):
        if x >= 0:
            y = 13.1 * x - 5.0
            # narrow spike at 0
            y += -377.12 * math.exp(-(x / 0.02) ** 2)
            return y
        else:
            return 1.3 * x - 10.0

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x is None:
                ys.append(None)
            else:
                ys.append(f(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}
