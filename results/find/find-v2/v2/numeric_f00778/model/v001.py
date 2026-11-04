def predict(probe):
    # Hypothesis: f(x) = x^3 * something? Let's check magnitudes.
    # E1: x=88.2 -> -2677280. x^3 = 686128. ratio ~ -3.9
    # x=66 -> -1121971. x^3=287496. ratio ~ -3.9
    # x=-20.3 -> 32506. x^3=-8365. ratio ~ -3.9
    # x=-61.7 -> 915169. x^3=-234885. ratio ~ -3.9
    # x=2.9 -> -87.69. x^3=24.389. ratio ~ -3.6
    # x=-24.3 -> 55797. x^3=-14348. ratio ~ -3.9
    # x=72.7 -> -1499449. x^3=384240. ratio ~ -3.9
    # x=-50.4 -> 498686. x^3=-128024. ratio ~ -3.9
    # x=-6.0 -> 824.74. x^3=-216. ratio ~ -3.8
    # x=21.3 -> -37733. x^3=9663. ratio ~ -3.9
    # Looks like f(x) ~ -3.9 * x^3. Let's refine: maybe -3.9 exactly? or -4?
    # Check x=88.2: -4*686128 = -2744512, observed -2677280. Not -4.
    # ratio: -2677280/686128 = -3.9020
    # x=66: -1121971/287496 = -3.9026
    # x=-20.3: 32506/-8365.4 = -3.8858
    # x=-61.7: 915169/-234885 = -3.8962
    # x=2.9: -87.6894/24.389 = -3.5954  <- off
    # Hmm x=2.9 off. Maybe there's a linear term too.
    # Try f(x) = a*x^3 + b*x. 
    # Use x=88.2: a*686128 + b*88.2 = -2677280
    # x=66: a*287496 + b*66 = -1121971
    # Solve: from second: b = (-1121971 - 287496a)/66
    # plug: 686128a + 88.2*(-1121971-287496a)/66 = -2677280
    # 686128a + 1.33636*(-1121971-287496a) = -2677280
    # 686128a - 1499279 - 384097a = -2677280
    # 302031a = -1178001 -> a = -3.9003
    # b = (-1121971 - 287496*(-3.9003))/66 = (-1121971+1121300)/66 ≈ -1.0
    # So f(x) ≈ -3.9*x^3 - x? Check x=2.9: -3.9*24.389 - 2.9 = -95.12-2.9=-98.0, observed -87.69. Not quite.
    # Maybe -3.9*x^3 + something. Let's just fit: x=2.9 gives -87.6894. -3.9*24.389=-95.12. diff=7.43.
    # x=-6: -3.9*(-216)=842.4, observed 824.74, diff=-17.66. Hmm.
    # Try f(x) = a*x^3 + b*x with a,b from x=2.9 and x=-6:
    # 24.389a + 2.9b = -87.6894
    # -216a - 6b = 824.7403
    # From first: b = (-87.6894 - 24.389a)/2.9
    # -216a -6*(-87.6894-24.389a)/2.9 = 824.7403
    # -216a + 2.06897*(87.6894+24.389a) = 824.7403
    # -216a + 181.42 + 50.46a = 824.7403
    # -165.54a = 643.32 -> a = -3.886
    # b = (-87.6894 -24.389*(-3.886))/2.9 = (-87.6894+94.77)/2.9 = 2.44
    # Check x=88.2: -3.886*686128 + 2.44*88.2 = -2666... let's see: -3.886*686128=-2666... 
    # 686128*3.886 = 2666... 686128*3.886=2666... approx 2666... 
    # Actually 686128*3.886 = 2,666,293. +2.44*88.2=215. total -2666078. observed -2677280. off by 11000.
    # Hmm. Maybe there's an x^2 term too. Let's fit cubic through 3 points.
    # Use x=88.2, x=66, x=-20.3.
    # Actually let's just do polynomial fit mentally is hard. 
    # Given ratios are all ~-3.9, likely f(x) = -3.9*x^3 plus small correction, OR exactly some constant.
    # Check: -3.9*88.2^3 = -3.9*686128.2 = -2675900. observed -2677280. diff -1380.
    # -3.9*66^3 = -3.9*287496 = -1121234. observed -1121971. diff -737.
    # -3.9*(-20.3)^3 = -3.9*(-8365.4)=32625. observed 32506. diff -119.
    # -3.9*(-61.7)^3 = -3.9*(-234885)=915,  3.9*234885=916051. observed 915169. diff -882.
    # -3.9*2.9^3 = -3.9*24.389=-95.12. observed -87.69. diff +7.43.
    # -3.9*(-24.3)^3 = -3.9*(-14348.9)=55961. observed 55797. diff -164.
    # -3.9*72.7^3 = -3.9*384240=-1498536. observed -1499449. diff -913.
    # -3.9*(-50.4)^3 = -3.9*(-128024)=499294. observed 498686. diff -608.
    # -3.9*(-6)^3 = -3.9*(-216)=842.4. observed 824.74. diff -17.66.
    # -3.9*21.3^3 = -3.9*9663.6=-37688. observed -37733. diff -45.
    # Diffs are small and negative-ish. Could be -3.9*x^3 - x? 
    # -x for x=88.2: -88.2, still not -1380.
    # Maybe -3.9*x^3 - 0.1*x^2? x=88.2: -0.1*7779=-778. closer.
    # Let's try f(x) = -3.9*x^3 - 0.1*x^2 - x? 
    # x=88.2: -2675900 -778 -88 = -2676766. observed -2677280. diff -514.
    # Hmm. Maybe coefficient is not exactly 3.9.
    # Let's compute a = y/x^3 for each:
    # 88.2: -3.90201
    # 66: -3.90259
    # -20.3: 32506/-8365.427 = -3.88585  (wait sign: x^3 negative, y positive, so a negative: 32506/(-8365.4)=-3.8858)
    # -61.7: 915169/(-234885.4) = -3.89623
    # 2.9: -87.6894/24.389 = -3.5954
    # -24.3: 55797.76/(-14348.9) = -3.8887
    # 72.7: -1499449/384240.2 = -3.9024
    # -50.4: 498686.8/(-128024.1) = -3.8952
    # -6: 824.74/(-216) = -3.8183
    # 21.3: -37733.4/9663.6 = -3.9047
    # The small |x| values (2.9, -6) deviate. Suggests an added term significant at small x, like c/x or c*x^2.
    # Try f(x) = a*x^3 + b*x^2 + c*x + d. Fit using 4 points.
    # Use x=2.9, -6, 21.3, 88.2.
    # This is getting complex. Let's just do a least squares guess: likely f(x) = -3.9*x^3 - x^2? 
    # x=2.9: -95.12 - 8.41 = -103.5, no.
    # Try f(x) = -3.9*x^3 + 0.5*x^2? x=2.9: -95.12+4.2=-90.9, closer to -87.69.
    # x=-6: 842.4+18=860.4, observed 824.74. no.
    # Hmm. Maybe f(x) = -3.9*x^3 - x^2/2? x=2.9: -95.12-4.2=-99.3. no.
    # Let's try f(x) = a*x^3 + b*x with a,b from large points.
    # x=88.2 and x=72.7:
    # 686128.2a + 88.2b = -2677280.07
    # 384240.2a + 72.7b = -1499449.38
    # Multiply first by 72.7, second by 88.2:
    # 49881... let's do: 
    # eq1*72.7: 49881... 686128.2*72.7=49,881,520a + 6412.14b = -194,638,261
    # eq2*88.2: 33,890,  384240.2*88.2=33,890,  33,890,  33,890,  let's compute: 384240.2*88.2=33,890,  384240.2*88=33,813,137.6 +384240.2*0.2=76,848 -> 33,889,985.6a + 6412.14b = -132,251,435
    # Subtract: (49,881,520-33,889,986)a = -194,638,261+132,251,435 = -62,386,826
    # 15,991,534a = -62,386,826 -> a = -3.9013
    # b = (-1499449.38 - 384240.2*(-3.9013))/72.7 = (-1499449.38+1499,  ) 
    # 384240.2*3.9013 = 1,499,  384240.2*3.9=1,498,536.8 +384240.2*0.0013=499.5 -> 1,499,036.3
    # b = (-1499449.38+1499036.3)/72.7 = (-413.08)/72.7 = -5.68
    # So f(x) ≈ -3.9013*x^3 - 5.68*x? Check x=2.9: -3.9013*24.389 -5.68*2.9 = -95.15-16.47=-111.6. observed -87.69. no.
    # The small x values really deviate. Maybe there's a region inside where behavior differs!
    # "There may be an interval inside the domain where the function behaves differently"
    # For |x| small, ratio deviates. Maybe f(x) = -3.9*x^3 for |x|>threshold, and something else for small x.
    # x=2.9: -87.69. x=-6: 824.74. 
    # If f(x) = -3.9*x^3 - x for small: 2.9: -95.12-2.9=-98. no.
    # Let's see if small x follows a different power. x=2.9 -> -87.69. x=-6 -> 824.74.
    # ratio -87.69/2.9 = -30.24. 824.74/-6 = -137.5. Not linear.
    # 2.9^3=24.389, -87.69/24.389=-3.595. -6^3=-216, 824.74/-216=-3.818.
    # Maybe it's a smooth function, not piecewise. Let's just fit a cubic polynomial through all points via least squares mentally is hard.
    # Let's try f(x) = -3.9*x^3 - x^2*0.1? 
    # Actually, let's reconsider. Maybe f(x) = -3.9*x^3 - x^2/10 - x/10?
    # x=2.9: -95.12 - 0.841 - 0.29 = -96.25. no.
    # What if f(x) = -3.9*x^3 + 0.1*x^2? x=2.9: -95.12+0.841=-94.28. no.
    # Let's try to find exact: maybe f(x) = -3.9*x^3 - x^2 + something.
    # x=2.9: -95.12-8.41=-103.5. no.
    # Hmm, observed -87.69 is HIGHER than -95.12 (less negative). So correction is positive at x=2.9.
    # For x=-6, observed 824.74 is LOWER than 842.4. correction negative.
    # So correction ~ +7.4 at x=2.9, -17.7 at x=-6. Roughly linear in x? slope ~ (7.4-(-17.7))/(2.9-(-6))=25.1/8.9=2.82. 
    # correction ≈ 2.82*x + c. at x=2.9: 8.18+c=7.4 -> c=-0.78. at x=-6: -16.9-0.78=-17.7. yes!
    # So f(x) ≈ -3.9*x^3 + 2.82*x - 0.78? Check x=21.3: -3.9*9663.6 + 2.82*21.3 -0.78 = -37688+60.1-0.78=-37628.7. observed -37733. off by 104.
    # Hmm not great. 
    # Maybe the correction is x^2 term. correction at 2.9=7.4, at -6=-17.7. x^2: 8.41 and 36. ratio 7.4/8.41=0.88, -17.7/36=-0.49. no.
    # Let's just fit cubic through 4 points and use that. But I can't compute easily.
    # Given time, let's go with f(x) = -3.9*x^3 and accept small error, OR try -3.9*x^3 - x^2/2 + ... 
    # Actually let's check if it's exactly f(x) = -3.9*x^3 - x^2/2 - x/2?
    # x=2.9: -95.12-4.205-1.45=-100.8. no.
    # Let's try f(x) = -3.9*x^3 + 0.5*x^2 - 0.5*x? x=2.9: -95.12+4.205-1.45=-92.4. no.
    # Try f(x) = -3.9*x^3 + x^2 - x? x=2.9: -95.12+8.41-2.9=-89.6. close to -87.69!
    # x=-6: 842.4+36+6=884.4. observed 824.74. no.
    # Hmm.
    # Let's just do a proper polynomial fit. I'll use numpy-like reasoning... can't.
    # Let's fit f(x) = a*x^3 + b*x^2 + c*x + d using 4 points: x=2.9, -6, 21.3, 88.2.
    # Actually, maybe simpler: the function might be f(x) = -3.9*x^3 - x^2/10 + ... 
    # Let me try assuming f(x) = a*x^3 + b*x^2 + c*x. (no constant, since f(0) likely 0)
    # Use 3 points: x=2.9, -6, 88.2.
    # 24.389a + 8.41b + 2.9c = -87.6894
    # -216a + 36b - 6c = 824.7403
    # 686128.2a + 7779.24b + 88.2c = -2677280.07
    # From eq1: c = (-87.6894 - 24.389a - 8.41b)/2.9
    # Sub into eq2: -216a + 36b - 6*(-87.6894-24.389a-8.41b)/2.9 = 824.7403
    # -216a + 36b + 2.06897*(87.6894+24.389a+8.41b) = 824.7403
    # -216a + 36b + 181.42 + 50.46a + 17.40b = 824.7403
    # -165.54a + 53.40b = 643.32   ... (A)
    # Sub into eq3: 686128.2a + 7779.24b + 88.2*(-87.6894-24.389a-8.41b)/2.9 = -2677280.07
    # 686128.2a + 7779.24b + 30.4138*(-87.6894-24.389a-8.41b) = -2677280.07
    # 686128.2a + 7779.24b - 2666.8 - 741.7a - 255.8b = -2677280.07
    # 685386.5a + 7523.4b = -2674613.3   ... (B)
    # From (A): b = (643.32+165.54a)/53.40 = 12.047 + 3.100a
    # Sub into (B): 685386.5a + 7523.4*(12.047+3.100a) = -2674613.3
    # 685386.5a + 90634 + 23322.5a = -2674613.3
    # 708709a = -2765247.3 -> a = -3.9018
    # b = 12.047 + 3.100*(-3.9018) = 12.047 - 12.096 = -0.049
    # c = (-87.6894 - 24.389*(-3.9018) - 8.41*(-0.049))/2.9
    # = (-87.6894 + 95.16 + 0.412)/2.9 = 7.88/2.9 = 2.72
    # So f(x) ≈ -3.9018*x^3 - 0.049*x^2 + 2.72*x
    # Check x=66: -3.9018*287496 -0.049*4356 +2.72*66 = -1121,  3.9018*287496=1,121,  287496*3.9=1,121,234.4 +287496*0.0018=517.5 -> 1,121,751.9. 
    # -1121751.9 -213.4 +179.5 = -1121785.8. observed -1121971.2. off by 185. 
    # Check x=-20.3: -3.9018*(-8365.4) -0.049*412.09 +2.72*(-20.3) = 32640.3 -20.2 -55.2 = 32564.9. observed 32506. off by 59.
    # Check x=72.7: -3.9018*384240.2 -0.049*5285.3 +2.72*72.7 = -1499,  384240.2*3.9018=1,499,  384240.2*3.9=1,498,536.8 +384240.2*0.0018=691.6 -> 1,499,228.4. -1499228.4 -259 +197.7 = -1499289.7. observed -1499449.4. off by 160.
    # Check x=-61.7: -3.9018*(-234885.4) -0.049*3806.9 +2.72*(-61.7) = 916,  234885.4*3.9018=916,  234885.4*3.9=916,053.1 +234885.4*0.0018=422.8 -> 916,475.9. -167.8-167.8=916,140.3. observed 915169.7. off by 970. Hmm.
    # The fit isn't perfect. Maybe there's noise, or the function is different.
    # Given the deviations, maybe f(x) = -3.9*x^3 - x^2/20 + 3*x? Let's not overfit.
    # Actually, let me reconsider: maybe f(x) = -3.9*x^3 - x^2/10 + 3*x? 
    # x=2.9: -95.12-0.841+8.7=-87.26. close to -87.69!
    # x=-6: 842.4-3.6-18=820.8. observed 824.74. close!
    # x=21.3: -37688-45.4+63.9=-37669.5. observed -37733. off 63.
    # x=88.2: -2675900-778+264.6=-2676413. observed -2677280. off 867.
    # Hmm.
    # Let's try f(x) = -3.9*x^3 - x^2/10 + 3*x - something.
    # I think the best simple model: f(x) = -3.9*x^3 - 0.1*x^2 + 3*x. But large x off.
    # Actually the large x points: ratio is very consistent ~-3.902. So a≈-3.902.
    # Let's just use f(x) = -3.902*x^3 - 0.05*x^2 + 2.7*x. It's a reasonable fit.
    # Given uncertainty, I'll go with a cubic polynomial fit.
    import math
    def f(x):
        return -3.9018*x**3 - 0.049*x**2 + 2.72*x
    return {"y": [f(x) for x in probe["x"]]}
