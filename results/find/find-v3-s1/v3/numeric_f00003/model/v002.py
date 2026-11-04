import math

def predict(probe):
    # Beliefs about f(x):
    # - f is even: f(-x)=f(x) [E4: f(5)=48.39, f(-5)=-20.45? No—check]
    #   Actually E4: f(5)=48.3879, f(-5)=-20.4469. NOT even! Asymmetric.
    #   Wait: E4 probe has -5 -> -20.4469, +5 -> 48.3879. So not even.
    #   But E2: f(4)=-12.9234, f(6)=146.0188, f(8)=398.2498... rising on positive side.
    #   E4 negative side: -5,-6,...-18 all -20.4469. So floor extends further on negative side.
    # - Flat floor at -20.4469 for x <= ~4 (negative side extends to at least -18) [E2,E4]
    #   E2: x=4 -> -12.9234 (just above floor), x=6 -> 146.02
    #   E4: x=5 -> 48.39, x=7 -> 272.13, x=9 -> 524.37
    # - Positive side rises quadratically: differences 48.39, 272.13, 524.37 at 5,7,9
    #   272.13-48.39=223.74 over 2 units; 524.37-272.13=252.24 over 2 units. 
    #   Second difference ~28.5 over 2 -> curvature. Fit a*x^2+b*x+c:
    #   25a+5b+c=48.39; 49a+7b+c=272.13; 81a+9b+c=524.37
    #   (2)-(1): 24a+2b=223.74 -> 12a+b=111.87
    #   (3)-(2): 32a+2b=252.24 -> 16a+b=126.12
    #   Subtract: 4a=14.25 -> a=3.5625, b=111.87-42.75=69.12, c=48.39-89.06-345.6=-386.3
    #   Check E2: x=6: 3.5625*36+69.12*6-386.3=128.25+414.72-386.3=156.67 vs 146.02 close-ish
    #   x=8: 3.5625*64+69.12*8-386.3=228+552.96-386.3=394.66 vs 398.25 good
    #   x=10: 3.5625*100+69.12*10-386.3=356.25+691.2-386.3=661.15 vs 650.48 ok
    #   x=12: 3.5625*144+69.12*12-386.3=513+829.44-386.3=956.14 vs 902.71 (off)
    #   x=14: 3.5625*196+69.12*14-386.3=698.25+967.68-386.3=1279.6 vs 1154.94 (off)
    #   x=16: 3.5625*256+69.12*16-386.3=912+1105.92-386.3=1631.6 vs 1407.17 (off)
    #   x=18: 3.5625*324+69.12*18-386.3=1154.25+1244.16-386.3=2012.1 vs 1659.4 (off)
    #   So curvature less than quadratic at larger x. Maybe linear-ish with slope ~126?
    #   E2 diffs: 6->146, 8->398 (diff 252 over 2 = 126/unit), 10->650 (126/unit),
    #   12->902 (126), 14->1155 (126), 16->1407 (126), 18->1659 (126). LINEAR slope 126!
    #   So for x>=6: f = 146.0188 + 126*(x-6) = 126*x - 610.0 approx
    #   Check x=5: 126*5-610=20 vs 48.39. Hmm not quite. x=7: 126*7-610=272 vs 272.13 good!
    #   x=9: 126*9-610=524 vs 524.37 good! x=5: 126*5-610=20 vs 48.39 (off, transition zone)
    #   So slope 126, intercept: 272.13-126*7=272.13-882=-609.87. f=126x-609.87 for x>=~6.5
    # - Negative side: floor -20.4469 extends to at least -18 [E4]. Where does it rise?
    #   E1: x=-62.7 -> 5293.6; x=-93.6 -> 13835.8; x=-104 -> 17162.4; x=-120.7 -> 22504
    #   Check linear slope 126 on negative side? -62.7: 126*62.7-609.87=7290 vs 5293. No.
    #   Negative side large |x|: -62.7->5293.6, -93.6->13835.8, -104->17162.4, -120.7->22504
    #   diffs: -93.6 to -104 (10.4 units): 17162-13836=3326 -> 320/unit
    #   -104 to -120.7 (16.7): 22504-17162=5342 -> 320/unit. LINEAR slope 320!
    #   -62.7 to -93.6 (30.9): 13836-5294=8542 -> 276/unit. Hmm.
    #   Fit line through -93.6 and -120.7: slope 320, intercept 13835.8-320*93.6=13835.8-29952=-16116
    #   Check -104: 320*104-16116=33280-16116=17164 vs 17162 good!
    #   Check -62.7: 320*62.7-16116=20064-16116=3948 vs 5294. Off (transition).
    #   So negative side large |x|: f = 320*|x| - 16116 for |x|>=~90
    # - Positive side large x: E1: 67.5->13475.7, 73.9->15822.7, 88.9->22155.9, 93.6->13835.8(?)
    #   93.6 anomaly: 13835.8 much lower than 88.9's 22155.9. Weird.
    #   67.5->13475.7, 73.9->15822.7: diff 2347 over 6.4 = 366.7/unit
    #   73.9->88.9: 22155.9-15822.7=6333 over 15 = 422/unit
    #   Not linear. Maybe quadratic on positive side large x?
    #   67.5^2=4556, 73.9^2=5461, 88.9^2=7903, 93.6^2=8761
    #   Fit a*x^2+b: 4556a+b=13475.7; 7903a+b=22155.9 -> 3347a=8680 -> a=2.593, b=13475.7-11813=1662.7
    #   Check 73.9: 5461*2.593+1662.7=14160+1663=15823 good!
    #   Check 93.6: 8761*2.593+1662.7=22717+1663=24380 vs 13835.8. WAY off.
    #   93.6 is anomalous. Maybe noise or a dip. E3: 86->20906, 102.8->28146, 114->32972
    #   86^2=7396: 2.593*7396+1663=19178+1663=20841 vs 20906 good!
    #   102.8^2=10568: 2.593*10568+1663=27403+1663=29066 vs 28146 close
    #   114^2=12996: 2.593*12996+1663=33700+1663=35363 vs 32972 (off)
    #   Hmm. 93.6 anomaly and 114 off. Maybe there's oscillation.
    #   E3: 56.7->9936, 67.1->13335. 56.7^2=3215: 2.593*3215+1663=8337+1663=10000 vs 9936 good
    #   67.1^2=4502: 2.593*4502+1663=11674+1663=13337 vs 13335 great!
    #   So positive side large x ~ 2.593*x^2+1663, except 93.6 (anomaly) and 114 (off).
    #   Maybe 93.6 and 114 are noise. I'll use quadratic.
    # - Negative side large |x|: check quadratic? -93.6: 2.593*8761+1663=24380 vs 13836. No, linear 320.
    #   So asymmetric: positive side quadratic, negative side linear at large |x|.
    #   Actually maybe negative side is also quadratic but different? -62.7: 2.593*3931+1663=11857 vs 5294 no.
    #   Linear 320 fits negative large well.
    # - Transition on negative side: floor until some point, then rises to linear 320.
    #   E1: -62.7->5294. Linear 320*62.7-16116=3948. Actual higher. 
    #   Maybe negative side: floor, then quadratic-ish, then linear? Complex.
    #   Let me just interpolate: floor -20.4469 for x in [-18, ~4.5]; 
    #   then positive rises with slope 126 (linear) for x in [6, ~40]; then quadratic 2.593x^2+1663 for x>~40
    #   Check continuity: at x=40, linear 126*40-610=4430; quad 2.593*1600+1663=4149+1663=5812. Mismatch.
    #   At x=30: linear 126*30-610=3170; quad 2.593*900+1663=2334+1663=3997. 
    #   Hmm. E1 has 38.8->5236.5. Linear: 126*38.8-610=4889-610=4279. Quad: 2.593*1505+1663=3903+1663=5566.
    #   Actual 5236.5 closer to quad. So maybe quadratic from earlier.
    #   E2 x=18: 1659.4. Quad: 2.593*324+1663=840+1663=2503. Linear: 126*18-610=1658. Linear wins!
    #   So small-mid positive: linear slope 126. Large positive: quadratic. Crossover ~40-50.
    #   At x=38.8: linear 4279, quad 5566, actual 5236 -> quad-ish. 
    #   At x=18: linear 1658 (exact), quad 2503. Linear.
    #   So crossover between 18 and 38.8. Let's say ~30.
    #   This is getting complex. Given MLP approximation, maybe it's smooth.
    #   I'll model positive side as: max(-20.4469, 126*x - 610) for x<35, then 2.593x^2+1663 for x>=35
    #   with blend. Actually simpler: use the linear for mid, quadratic for large, take max.
    # - Negative side: floor to -18, then rises. E1 -62.7->5294. 
    #   Maybe negative side also has linear then quadratic. -62.7: linear320 gives 3948, actual 5294.
    #   Let me fit negative side as quadratic too? -62.7^2=3931, -93.6^2=8761, -104^2=10816, -120.7^2=14568
    #   a*3931+b=5294; a*14568+b=22504 -> 10637a=17210 -> a=1.618, b=5294-6360=-1066
    #   Check -93.6: 1.618*8761-1066=14175-1066=13109 vs 13836 close
    #   Check -104: 1.618*10816-1066=17500-1066=16434 vs 17162 close-ish
    #   So negative side ~1.618*x^2-1066 for large |x|. 
    #   But E4 -18: 1.618*324-1066=524-1066=-542, actual -20.4469. So floor dominates at -18.
    #   Where does negative side leave floor? Unknown between -18 and -62.7. Guess ~-25?
    #   Actually maybe negative side is also linear slope 126 near threshold then quadratic.
    #   I'll use: negative side max(-20.4469, 1.618*x^2-1066) for |x|>~25, else floor.
    #   Check -62.7: 1.618*3931-1066=6360-1066=5294. EXACT! 
    #   -93.6: 1.618*8761-1066=14175-1066=13109 vs 13836 (off 5%)
    #   -104: 16434 vs 17162 (off 4%)
    #   -120.7: 1.618*14568-1066=23571-1066=22505 vs 22504. EXACT!
    #   Wow, 1.618*x^2-1066 fits -62.7 and -120.7 exactly. Middle points slightly off (noise).
    #   So negative side: f = 1.618*x^2 - 1066 for |x| large, floored at -20.4469.
    #   Threshold: 1.618*x^2-1066=-20.4469 -> x^2=1045.5/1.618=646 -> |x|=25.4
    #   So floor for |x|<25.4 on negative side. E4 -18 floor ✓.
    # - Positive side: 2.593*x^2+1663? Check x=18: 2.593*324+1663=2503 vs 1659. Off.
    #   Hmm positive side doesn't fit quadratic at small x. 
    #   Maybe positive side: linear 126 then quadratic. Or maybe positive side is 1.618*x^2-1066 too?
    #   x=18: 1.618*324-1066=524-1066=-542 vs 1659. No.
    #   x=38.8: 1.618*1505-1066=2435-1066=1369 vs 5236. No.
    #   Positive side is different. Let me refit positive side quadratic with more points:
    #   38.8->5236.5, 56.7->9936.3, 67.1->13335.2, 67.5->13475.7, 73.9->15822.7, 86->20906.1, 88.9->22155.9
    #   Use 38.8 and 88.9: 1505a+b=5236.5; 7903a+b=22155.9 -> 6398a=16919 -> a=2.644, b=5236.5-3979=1257.5
    #   Check 67.1: 2.644*4502+1257.5=11903+1258=13161 vs 13335 close
    #   Check 86: 2.644*7396+1257.5=19555+1258=20813 vs 20906 close
    #   Check 56.7: 2.644*3215+1257.5=8500+1258=9758 vs 9936 close
    #   Check 18: 2.644*324+1257.5=857+1258=2115 vs 1659 (off)
    #   Check 6: 2.644*36+1257.5=95+1258=1353 vs 146. Way off.
    #   So positive side: linear near threshold, quadratic far. Crossover.
    #   At x=18 linear gives 1658 (exact). Quadratic gives 2115. Linear better.
    #   At x=38.8 linear 4279, quad 5237 (exact). Quad better.
    #   Crossover ~25-30. 
    #   Model positive side: for x in [~4.5, 28]: linear 126x-610; for x>28: 2.644x^2+1257.5
    #   At x=28: linear 126*28-610=2918; quad 2.644*784+1257.5=2073+1258=3331. Mismatch.
    #   Blend or just pick. Given MLP smoothness, maybe it's a smooth curve.
    #   Actually maybe positive side is linear 126 up to ~30 then curves up. 
    #   Let me just use: positive side = max(-20.4469, 126*x-610) for x<30, and 2.644x^2+1257.5 for x>=30.
    #   Discontinuity at 30: linear 3170, quad 3637. Small jump. Acceptable.
    # - 93.6 anomaly: 13835.8 vs predicted quad 2.644*8761+1257.5=23164+1258=24422. Big miss.
    #   Maybe noise or a dip. I'll ignore, use quad.
    # - 114: 32972.7 vs quad 2.644*12996+1257.5=34362+1258=35620. Off 8%. 
    #   Maybe quadratic coefficient slightly lower at very large x. Use 2.5? 
    #   2.5*12996+1257.5=32490+1258=33748 vs 32972. Better. 
    #   But 88.9: 2.5*7903+1258=19758+1258=21016 vs 22156. Worse.
    #   Keep 2.644.
    # - Positive side threshold from floor: 126x-610=-20.4469 -> x=589.6/126=4.68
    #   E2 x=4: -12.9234 (just above floor), x=6: 146. Linear at 4: 126*4-610=-106 vs -12.9. Off.
    #   At x=4.68 floor. E2 x=4 gives -12.9 (above floor). So threshold ~4.5.
    #   Linear at 4.5: 126*4.5-610=-43. Hmm. Actual -12.9 at x=4.
    #   Maybe transition is smooth. I'll use max(-20.4469, 126*x-610) which gives floor until x=4.68.
    #   E2 x=4: max(-20.4469, -106)=-20.4469 vs actual -12.9234. Off by 7.5. Acceptable-ish.
    #   E4 x=5: max(-20.4469, 20)=20 vs 48.39. Off 28.
    #   Hmm. Maybe slope steeper near threshold. 
    #   Let me refit positive small: x=5->48.39, x=6->146.02, x=7->272.13, x=8->398.25, x=9->524.37
    #   diffs: 97.63, 126.11, 126.12, 126.12. So slope 126 from x=6 onward, but x=5->6 is 97.6.
    #   So threshold ~5.5, slope 126. f=126*(x-5.5)+48.39? At x=6: 126*0.5+48.39=111 vs 146. No.
    #   f=126*(x-6)+146.02 for x>=6. At x=5: 126*(-1)+146=20 vs 48.39. Off.
    #   There's a kink. x=5->48.39, x=6->146.02. Slope 97.6 there. Then 126 after.
    #   I'll just use linear 126x-610 for x>=6, and interpolate 4.5-6.
    #   For x in [4.5,6]: linear from (-20.4469 at 4.5) to (146.02 at 6): slope 166.5/1.5=111
    #   f = -20.4469 + 111*(x-4.5)
    #   At x=5: -20.4469+55.5=35 vs 48.39. Closer.
    #   Good enough.
    
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
            continue
        if x < 0:
            # negative side: quadratic 1.618x^2-1066, floored at -20.4469
            v = 1.618 * x * x - 1066.0
            out.append(max(-20.4469, v))
        else:
            # positive side
            if x < 4.5:
                out.append(-20.4469)
            elif x < 6.0:
                out.append(-20.4469 + 111.0 * (x - 4.5))
            elif x < 30.0:
                out.append(126.0 * x - 610.0)
            else:
                out.append(2.644 * x * x + 1257.5)
    return {"y": out}
