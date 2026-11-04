def predict(probe):
    # Observations:
    # - Small |x| gives constant floor -20.4469 [E1 x=-6.0,2.9; E2 x=1.2; E3 x=-7.1,-16.9; E4 x=-5.9]
    # - Large |x| grows ~quadratically, roughly symmetric coefficient ~2.0 [E1-E4]
    # - E4 shows transition: x=12.5 -> 965.77 (NOT floor), x=-25.9 -> 261.26 (small, near floor)
    #   So the dead-zone threshold is smaller than 18; x=12.5 is already active.
    # - E4 x=-25.9 -> 261.26 : formula 1.987*670.8+40.8*(-25.9)=1333-1057=276, close (5% off)
    # - E4 x=12.5 -> 965.77 : positive formula 1.975*156.25+56.1*12.5=308.6+701=1010, close (4% off)
    # - E4 x=43.0 -> 6206.72 : 1.975*1849+56.1*43=3652+2412=6064, close (2% off)
    # - E4 x=56.2 -> 9783.98 : 1.975*3158+56.1*56.2=6238+3153=9391, ~4% low
    # - E4 x=78.1 -> 17501.59 : 1.975*6100+56.1*78.1=12047+4381=16428, ~6% low
    # - E4 x=93.5 -> 24138.26 : 1.975*8742+56.1*93.5=17266+5245=22511, ~7% low
    # - E4 x=83.2 -> 19699.45 : 1.975*6922+56.1*83.2=13671+4668=18339, ~7% low
    # - E4 x=-124.4 -> 23687.46 : 1.987*15475+40.8*(-124.4)=30748-5076=25672, ~8% high
    # - E4 x=-61.3 -> 5003.12 : 1.987*3758+40.8*(-61.3)=7467-2501=4966, ~1% off
    # The positive side is consistently ~5-7% LOW at large x; negative side ~8% HIGH at large |x|.
    # Refit positive using E4 large points: (93.5,24138),(78.1,17502),(83.2,19699)
    # Try y=a*x^2+b*x: 
    # 8742a+93.5b=24138 ; 6100a+78.1b=17502
    # From these: solve. 8742a+93.5b=24138; 6100a+78.1b=17502
    # Multiply 2nd by (93.5/78.1)=1.1972: 7303a+93.5b=20953
    # Subtract: 1439a=3185 => a=2.213, b=(17502-6100*2.213)/78.1=(17502-13500)/78.1=51.2
    # Check x=123.6: 2.213*15277+51.2*123.6=33808+6328=40136 vs 37110 (8% high). Hmm.
    # Check x=88.2: 2.213*7779+51.2*88.2=17215+4516=21731 vs 21854 (0.6% off). 
    # Check x=104.5: 2.213*10920+51.2*104.5=24166+5350=29516 vs 28879 (2% high)
    # Check x=43: 2.213*1849+51.2*43=4092+2202=6294 vs 6207 (1.4% high)
    # Check x=56.2: 2.213*3158+51.2*56.2=6989+2877=9866 vs 9784 (0.8% high)
    # Check x=78.1: 2.213*6100+51.2*78.1=13500+3999=17499 vs 17502. 
    # Check x=93.5: 2.213*8742+51.2*93.5=19346+4787=24133 vs 24138. 
    # Check x=83.2: 2.213*6922+51.2*83.2=15318+4260=19578 vs 19699 (0.6% off)
    # Check x=21.3: 2.213*453.7+51.2*21.3=1004+1091=2095 vs 2092. 
    # Check x=30.3: 2.213*918+51.2*30.3=2032+1551=3583 vs 3514 (2% high)
    # Check x=65.5: 2.213*4290+51.2*65.5=9494+3354=12848 vs 12780 (0.5% off)
    # Check x=47.1: 2.213*2218+51.2*47.1=4908+2412=7320 vs 7234 (1.2% high)
    # Check x=58.8: 2.213*3457+51.2*58.8=7650+3011=10661 vs 10583 (0.7% high)
    # Check x=102.1: 2.213*10424+51.2*102.1=23068+5228=28296 vs 27844 (1.6% high)
    # Check x=105.7: 2.213*11172+51.2*105.7=24724+5412=30136 vs 29396 (2.5% high)
    # Check x=119.5: 2.213*14280+51.2*119.5=31602+6118=37720 vs 35343 (6.7% high)
    # Check x=123.6: 8% high. So large x slightly high but much better overall.
    # Try a=2.15, b=55: 
    # 123.6: 2.15*15277+55*123.6=32846+6798=39644 (6.8% high)
    # 88.2: 2.15*7779+55*88.2=16725+4851=21576 (1.3% low)
    # 93.5: 2.15*8742+55*93.5=18795+5143=23938 (0.8% low)
    # 78.1: 2.15*6100+55*78.1=13115+4296=17411 (0.5% low)
    # 43: 2.15*1849+55*43=3975+2365=6340 (2% high)
    # 21.3: 2.15*453.7+55*21.3=975+1172=2147 (2.6% high)
    # 30.3: 2.15*918+55*30.3=1974+1667=3641 (3.6% high)
    # Compromise: a=2.18, b=53
    # 123.6: 2.18*15277+53*123.6=33304+6551=39855 (7.4% high)
    # 88.2: 2.18*7779+53*88.2=16958+4675=21633 (1% low)
    # 93.5: 2.18*8742+53*93.5=19058+4956=24014 (0.5% low)
    # 78.1: 2.18*6100+53*78.1=13298+4139=17437 (0.4% low)
    # 43: 2.18*1849+53*43=4031+2279=6310 (1.7% high)
    # 21.3: 2.18*453.7+53*21.3=989+1129=2118 (1.2% high)
    # 30.3: 2.18*918+53*30.3=2001+1606=3607 (2.6% high)
    # 65.5: 2.18*4290+53*65.5=9352+3472=12824 (0.3% high)
    # 58.8: 2.18*3457+53*58.8=7536+3116=10652 (0.7% high)
    # 47.1: 2.18*2218+53*47.1=4835+2496=7331 (1.3% high)
    # 102.1: 2.18*10424+53*102.1=22724+5411=28135 (1% high)
    # 104.5: 2.18*10920+53*104.5=23806+5539=29345 (1.6% high)
    # 105.7: 2.18*11172+53*105.7=24355+5602=29957 (1.9% high)
    # 119.5: 2.18*14280+53*119.5=31130+6334=37464 (6% high)
    # Good enough. Use a=2.18, b=53 for positive.
    # Negative refit: E4 x=-124.4 -> 23687, x=-61.3 -> 5003, x=-25.9 -> 261
    # Try y=a*x^2+b*x (b negative since x neg):
    # 15475a-124.4b=23687 ; 3758a-61.3b=5003
    # From 2nd: b=(3758a-5003)/61.3
    # 15475a-124.4*(3758a-5003)/61.3=23687
    # 15475a-2.0294*(3758a-5003)=23687
    # 15475a-7626a+10153=23687
    # 7849a=13534 => a=1.724, b=(3758*1.724-5003)/61.3=(6479-5003)/61.3=24.1
    # Check x=-102.2: 1.724*10445+24.1*(-102.2)=18007-2463=15544 vs 16587 (6% low)
    # Check x=-48.6: 1.724*2362+24.1*(-48.6)=4072-1171=2901 vs 2711 (7% high)
    # Check x=-55.8: 1.724*3114+24.1*(-55.8)=5369-1345=4024 vs 3928 (2.4% high)
    # Check x=-50.4: 1.724*2540+24.1*(-50.4)=4379-1215=3164 vs 2995 (5.6% high)
    # Check x=-63.9: 1.724*4083+24.1*(-63.9)=7039-1540=5499 vs 5554 (1% low)
    # Check x=-61.7: 1.724*3807+24.1*(-61.7)=6563-1487=5076 vs 5086. 
    # Check x=-25.9: 1.724*670.8+24.1*(-25.9)=1156-624=532 vs 261 (2x high). Hmm.
    # The -25.9 point is near transition, so formula less reliable there.
    # Try a=1.85, b=30:
    # -124.4: 1.85*15475+30*(-124.4)=28629-3732=24897 vs 23687 (5% high)
    # -102.2: 1.85*10445+30*(-102.2)=19323-3066=16257 vs 16587 (2% low)
    # -61.7: 1.85*3807+30*(-61.7)=7043-1851=5192 vs 5086 (2% high)
    # -55.8: 1.85*3114+30*(-55.8)=5761-1674=4087 vs 3928 (4% high)
    # -50.4: 1.85*2540+30*(-50.4)=4699-1512=3187 vs 2995 (6% high)
    # -48.6: 1.85*2362+30*(-48.6)=4370-1458=2912 vs 2711 (7% high)
    # -63.9: 1.85*4083+30*(-63.9)=7554-1917=5637 vs 5554 (1.5% high)
    # -25.9: 1.85*670.8+30*(-25.9)=1241-777=464 vs 261 (high)
    # Try a=1.9, b=28:
    # -124.4: 1.9*15475+28*(-124.4)=29403-3483=25920 (9% high)
    # -102.2: 1.9*10445+28*(-102.2)=19846-2862=16984 (2.4% high)
    # -61.7: 1.9*3807+28*(-61.7)=7233-1728=5505 (8% high)
    # Hmm. a=1.8, b=32:
    # -124.4: 1.8*15475+32*(-124.4)=27855-3981=23874 vs 23687 (0.8% high)
    # -102.2: 1.8*10445+32*(-102.2)=18801-3270=15531 vs 16587 (6% low)
    # -61.7: 1.8*3807+32*(-61.7)=6853-1974=4879 vs 5086 (4% low)
    # -55.8: 1.8*3114+32*(-55.8)=5605-1786=3819 vs 3928 (3% low)
    # -50.4: 1.8*2540+32*(-50.4)=4572-1613=2959 vs 2995 (1% low)
    # -48.6: 1.8*2362+32*(-48.6)=4252-1555=2697 vs 2711 (0.5% low)
    # -63.9: 1.8*4083+32*(-63.9)=7349-2045=5304 vs 5554 (4.5% low)
    # -25.9: 1.8*670.8+32*(-25.9)=1207-829=378 vs 261 (high)
    # Compromise a=1.83, b=31:
    # -124.4: 1.83*15475+31*(-124.4)=28319-3856=24463 (3% high)
    # -102.2: 1.83*10445+31*(-102.2)=19114-3168=15946 (4% low)
    # -61.7: 1.83*3807+31*(-61.7)=6967-1913=5054 (0.6% low)
    # -55.8: 1.83*3114+31*(-55.8)=5699-1730=3969 (1% high)
    # -50.4: 1.83*2540+31*(-50.4)=4648-1562=3086 (3% high)
    # -48.6: 1.83*2362+31*(-48.6)=4322-1507=2815 (4% high)
    # -63.9: 1.83*4083+31*(-63.9)=7472-1981=5491 (1% low)
    # -25.9: 1.83*670.8+31*(-25.9)=1228-803=425 vs 261 (high, near transition)
    # Use a=1.83, b=31 for negative.
    # Transition: E4 x=12.5 -> 965.77 (active), x=-25.9 -> 261 (active but small).
    # E1 x=2.9 -> floor, x=-6.0 -> floor. E2 x=1.2 -> floor.
    # So dead zone roughly |x| < ~10? x=12.5 active. Need boundary.
    # Positive formula at x=10: 2.18*100+53*10=218+530=748. At x=8: 139+424=563.
    # But floor is -20.4469. So if formula > floor, why floor at small x?
    # The MLP likely has a flat region then rises. Model as: if |x| < T return floor, else formula.
    # T between 2.9 and 12.5 for positive. For negative, -6.0 floor, -25.9 active.
    # Guess T ~ 10 (uncertain).
    # Actually maybe smoother: the floor region is where formula would be below some value.
    # For negative formula at x=-10: 1.83*100+31*(-10)=183-310=-127 < floor -> floor. Good.
    # At x=-20: 1.83*400+31*(-20)=732-620=112 > floor. But E1 x=-20.3 -> -15.87 (near floor, not 112).
    # Hmm E1 x=-20.3 -> -15.8672, which is slightly above floor -20.4469.
    # Formula at -20.3: 1.83*412+31*(-20.3)=754-629=125. Observed -15.87. Big mismatch!
    # So near x=-20 the function is still near floor, not 125.
    # E1 x=-24.3 -> 166.21. Formula: 1.83*590.5+31*(-24.3)=1081-753=328. Observed 166.
    # E4 x=-25.9 -> 261.26. Formula: 425. Observed 261.
    # So negative side near transition is lower than formula. The formula overestimates near -20 to -26.
    # Maybe the negative side has a different shape near transition. 
    # Let's use a smooth transition: y = max(floor, formula) but formula for negative should be lower.
    # Actually observed: -20.3 -> -15.87 (just above floor), -24.3 -> 166, -25.9 -> 261.
    # These are much less than formula. So there's a soft ramp.
    # Try: for negative, y = floor + softplus-like. Or use formula with smaller coefficient near transition.
    # Given complexity, use: if x > -18: floor (approx), else formula but with a ramp.
    # Actually -20.3 gives -15.87 which is floor+4.6. -24.3 gives 166. -25.9 gives 261.
    # The ramp from -20 to -26 goes from ~0 to 261. 
    # Let's model negative as: y = max(floor, 1.83*x^2+31*x) but that gives 125 at -20.3, too high.
    # Alternative: the MLP output is smooth; near transition it's between floor and quadratic.
    # Use a blend: y = floor + (formula - floor) * sigmoid((|x|-T)/w) for negative.
    # But simpler: just use formula for |x|>~28, floor for |x|<~18, and linear ramp between.
    # For positive: x=12.5 -> 965.77. Formula: 2.18*156.25+53*12.5=340+662=1002. Close (4% off).
    # x=2.9 -> floor. So positive transition between 2.9 and 12.5.
    # Positive formula at x=5: 2.18*25+53*5=54.5+265=319. At x=8: 563.
    # Observed at 2.9 is floor. So threshold ~ maybe 6-8?
    # Let's guess positive threshold T_pos ~ 7, negative T_neg ~ 18 with ramp.
    # Given uncertainty, use: if |x| < 7: floor; else formula. For negative, formula at -7: 1.83*49+31*(-7)=90-217=-127 < floor, so max(floor,formula) works there.
    # At x=-18: 1.83*324+31*(-18)=593-558=35 > floor. But observed near -20 is -15.87. 
    # So max(floor, formula) gives 35 at -18, but actual is lower. Use larger threshold for negative.
    # Let's use: if x < -20: formula (but formula overestimates near -20). 
    # Compromise: negative formula a=1.83,b=31, but apply max(floor, formula) and accept error near -20.
    # Actually E1 -20.3 -> -15.87, formula gives 125. That's a big error. 
    # Maybe negative side has smaller coefficient near transition. 
    # Let's try a piecewise: for x in [-30,-18], linear ramp from floor to formula(-30).
    # formula(-30)=1.83*900+31*(-30)=1647-930=717. 
    # Ramp: at -20.3 -> -15.87, at -24.3 -> 166, at -25.9 -> 261.
    # Slope between -20.3 and -24.3: (166-(-15.87))/4 = 45.5 per unit.
    # Between -24.3 and -25.9: (261-166)/1.6=59.4 per unit.
    # So roughly linear with slope ~50. At x=-20.3 y=-15.87. 
    # Extrapolate: y = -15.87 + 50*(x+20.3). At x=-30: -15.87+50*(-9.7)=-500. Negative, not matching formula 717.
    # So it curves up. 
    # Given time constraints, use: for x < -18: max(floor, 1.83*x^2+31*x) but with a correction.
    # Actually let's just use a=1.83,b=31 and accept near-transition error, but shift threshold.
    # Use: if x >= 0: if x < 7: floor else 2.18*x^2+53*x
    #      if x < 0: if x > -18: floor else 1.83*x^2+31*x
    # This gives -20.3 -> 1.83*412+31*(-20.3)=754-629=125 (observed -15.87, error large).
    # Hmm. The negative transition is wider. 
    # Let's use a smooth max: y = floor + softplus(formula - floor) with small width? 
    # Or: for negative, use formula but with a=1.5, b=45 near transition?
    # At -20.3: 1.5*412+45*(-20.3)=618-913=-295 < floor -> floor. But observed -15.87 (just above floor).
    # At -24.3: 1.5*590+45*(-24.3)=885-1093=-208 < floor -> floor. But observed 166.
    # Not working.
    # The data suggests negative side: floor until ~-20, then ramps up. 
    # Let's model negative as: y = floor + max(0, k*(|x|-20))^2 * something? 
    # At -24.3: 166-(-20.4)=186.4. |x|-20=4.3. 186.4/4.3^2=10.1.
    # At -25.9: 261-(-20.4)=281.4. |x|-20=5.9. 281.4/5.9^2=8.1.
    # At -48.6: 2711+20.4=2731. |x|-20=28.6. 2731/28.6^2=3.34.
    # Not constant.
    # Given time, use the quadratic formula for |x|>~28, floor for |x|<~18, and linear interpolation between.
    # For positive: floor for x<7, formula for x>7 (formula at 7: 2.18*49+53*7=107+371=478, but observed at 12.5 is 966 which matches formula).
    # Wait at x=7 formula gives 478, but is actual floor or 478? Unknown. E2 x=1.2 floor. 
    # Let's just use: positive: if x<7 floor else formula. negative: if x>-18 floor else formula.
    # Accept error near negative transition.
    def f(x):
        if x >= 0:
            if x < 7:
                return -20.4469
            return 2.18*x*x + 53.0*x
        else:
            if x > -18:
                return -20.4469
            return 1.83*x*x + 31.0*x
    return {"y": [f(x) for x in probe["x"]]}
