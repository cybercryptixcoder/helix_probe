def predict(probe):
    # Observations:
    # - For |x| small (roughly |x| < ~10), output is a constant -20.4469 [E1 x=-6.0, E2 x=1.2, E3 x=-7.1,-16.9]
    # - For larger |x|, output grows like x^2 (quadratic) [E1 x=88.2 -> 21854, E2 x=123.6 -> 37110]
    # - Negative large x also positive quadratic [E1 x=-61.7 -> 5086, E3 x=-102.2 -> 16586]
    # - So f(x) = max(-20.4469, a*x^2 + b) roughly; fit a from data
    # Fit: x=123.6 -> 37109.93 => a ~ 37109.93/123.6^2 = 2.429
    #      x=119.5 -> 35343.03 => a ~ 35343.03/119.5^2 = 2.474
    #      x=105.7 -> 29395.88 => a ~ 2.630
    #      x=102.1 -> 27844.45 => a ~ 2.671
    #      x=88.2  -> 21854.21 => a ~ 2.809
    # Not pure x^2; looks like a smooth MLP. Try a*x^2 + c with floor.
    # Better: use a quadratic fit through points. Let's estimate a and b via least squares on large points.
    # Points (x, y): (88.2,21854.21),(66,12950.84),(72.7,15366.07),(104.5,28878.74),(65.5,12779.96),
    # (104.9,29051.12),(123.6,37109.93),(79.4,18061.83),(103,28232.31),(58.8,10583.10),(102.1,27844.45),
    # (47.1,7233.74),(-102.2,16586.61),(105.7,29395.88),(119.5,35343.03),(-61.7,5086.13),(-50.4,2995.40),
    # (-48.6,2710.67),(-55.8,3927.93),(-63.9,5554.33),(30.3,3514.42),(28.4,3172.87),(21.3,2091.93)
    # Note negative side: x=-102.2 -> 16586, but x=+102.1 -> 27844. Asymmetric! Negative side smaller.
    # x=-61.7 -> 5086 vs x=+58.8 -> 10583. So negative side roughly half.
    # Check: -102.2^2=10445, 16586/10445=1.588; +102.1^2=10424, 27844/10424=2.671. Ratio ~0.594
    # -61.7^2=3807, 5086/3807=1.336; +58.8^2=3457, 10583/3457=3.061. Hmm not constant ratio.
    # Try linear+quadratic: y = a*x^2 + b*x + c for x>0 and separately for x<0.
    # Positive: use (88.2,21854),(123.6,37110),(58.8,10583)
    # Solve: a*88.2^2+b*88.2+c=21854; a*123.6^2+b*123.6+c=37110; a*58.8^2+b*58.8+c=10583
    # 7779.24a+88.2b+c=21854
    # 15276.96a+123.6b+c=37110
    # 3457.44a+58.8b+c=10583
    # Subtract: 7497.72a+35.4b=15256 ; 4321.8a+29.4b=11271
    # From second: b=(11271-4321.8a)/29.4
    # 7497.72a + 35.4*(11271-4321.8a)/29.4 = 15256
    # 7497.72a + 1.20408*(11271-4321.8a)=15256
    # 7497.72a + 13571.5 - 5204.1a = 15256
    # 2293.6a = 1684.5 => a=0.7344
    # b=(11271-4321.8*0.7344)/29.4=(11271-3174)/29.4=275.4
    # c=21854-7779.24*0.7344-88.2*275.4=21854-5713-24290=-8149 -> negative, odd
    # Check x=104.5: 0.7344*10920+275.4*104.5-8149=8019+28779-8149=28649 vs 28879 close-ish
    # x=65.5: 0.7344*4290+275.4*65.5-8149=3151+18039-8149=13041 vs 12780 close
    # x=30.3: 0.7344*918+275.4*30.3-8149=674+8345-8149=870 vs 3514. Bad for small.
    # So small x has floor -20.4469, and transition. Actually 30.3 gives 3514, 28.4 gives 3173, 21.3 gives 2092.
    # 21.3^2=453.7, 2092/453.7=4.61; 30.3^2=918, 3514/918=3.83; 47.1^2=2218, 7234/2218=3.26
    # Ratio decreasing -> not pure quadratic. Maybe cubic-ish? Or MLP.
    # Try y = a*x^2 + b for positive: from (123.6,37110) and (21.3,2092):
    # 15276.96a+b=37110; 453.69a+b=2092 => 14823.27a=35018 => a=2.362, b=2092-1071=1021
    # Check x=88.2: 2.362*7779+1021=18374+1021=19395 vs 21854. Off.
    # MLP likely has smooth nonlinearity. Let's just fit piecewise quadratic per sign with least squares.
    # Given complexity, use a reasonable approximation: y = max(-20.4469, A*x^2 + B*x + C) per sign.
    # Positive fit from data points (x>10):
    # Use numpy-free least squares manually is tedious; use rough fit.
    # Let's fit y = a*x^2 + b for x>0 using points (123.6,37110),(88.2,21854),(58.8,10583),(30.3,3514)
    # Sum approach: minimize sum (a*x^2+b-y)^2
    # d/da: sum x^2*(a*x^2+b-y)=0 ; d/db: sum(a*x^2+b-y)=0
    # Points: (15276.96,37110),(7779.24,21854),(3457.44,10583),(918.09,3514)
    # Sxx=sum x^4: 15276.96^2=2.334e8; 7779.24^2=6.052e7; 3457.44^2=1.195e7; 918.09^2=8.43e5
    # Sx2=sum x^2=27431.7; Sy=63061; Sx2y=sum x^2*y
    # 15276.96*37110=5.669e8; 7779.24*21854=1.700e8; 3457.44*10583=3.659e7; 918.09*3514=3.226e6
    # Sx2y=7.767e8
    # Sxx=3.143e8
    # n=4
    # a*Sxx+b*Sx2=Sx2y ; a*Sx2+b*n=Sy
    # 3.143e8 a + 27431.7 b = 7.767e8
    # 27431.7 a + 4 b = 63061
    # From 2nd: b=(63061-27431.7a)/4
    # 3.143e8 a + 27431.7*(63061-27431.7a)/4 = 7.767e8
    # 3.143e8 a + 6857.9*(63061-27431.7a)=7.767e8
    # 3.143e8 a + 4.325e8 - 1.881e8 a = 7.767e8
    # 1.262e8 a = 3.442e8 => a=2.727
    # b=(63061-27431.7*2.727)/4=(63061-74806)/4=-2936
    # Check x=88.2: 2.727*7779-2936=21213-2936=18277 vs 21854. Off ~16%.
    # The MLP isn't exactly quadratic. Given time, use a*x^2 with a~2.6 for positive, ~1.5 for negative, floor -20.4469.
    # Better: interpolate. Actually let me just use a smooth fit: y = max(-20.4469, k*x^2) with k_pos~2.5, k_neg~1.5.
    # Check pos: 2.5*123.6^2=38192 vs 37110 (3% off); 2.5*88.2^2=19448 vs 21854 (11% off)
    # Try k=2.6: 123.6->39720 (7% high); 88.2->20226 (7% low). k=2.55: 123.6->38956; 88.2->19837
    # Hmm. The function may be more like x^2 scaled by a smooth factor. 
    # Given MLP, maybe it's something like softplus or x^2 with tanh. Let's just do a*x^2+b*x+c fit for positive.
    # From earlier 3-point fit: a=0.7344,b=275.4,c=-8149. Check x=123.6: 0.7344*15277+275.4*123.6-8149=11219+34039-8149=37109. 
    # x=88.2: 0.7344*7779+275.4*88.2-8149=5713+24290-8149=21854. 
    # x=58.8: 0.7344*3457+275.4*58.8-8149=2539+16194-8149=10584. 
    # x=104.5: 0.7344*10920+275.4*104.5-8149=8019+28779-8149=28649 vs 28879 (0.8% off)
    # x=65.5: 0.7344*4290+275.4*65.5-8149=3151+18039-8149=13041 vs 12780 (2% off)
    # x=30.3: 0.7344*918+275.4*30.3-8149=674+8345-8149=870 vs 3514. Bad.
    # x=21.3: 0.7344*453.7+275.4*21.3-8149=333+5866-8149=-1950 vs 2092. Bad.
    # So small positive x doesn't fit. There's a floor region then transition.
    # Actually 21.3->2092, 28.4->3173, 30.3->3514, 47.1->7234. These fit ~ x^2 * something.
    # 21.3: 2092/453.7=4.61; 28.4: 3173/806.6=3.93; 30.3: 3514/918=3.83; 47.1: 7234/2218=3.26; 58.8: 10583/3457=3.06; 65.5: 12780/4290=2.98; 88.2: 21854/7779=2.81; 104.5: 28879/10920=2.64; 123.6: 37110/15277=2.43
    # Ratio decreasing smoothly from ~4.6 to ~2.4. So y = x^2 * g(x) where g decreases. 
    # Could be y = a*x^2 + b*x with b>0? 21.3: a*453.7+b*21.3=2092; 123.6: a*15277+b*123.6=37110
    # From 2nd: b=(37110-15277a)/123.6
    # 453.7a+21.3*(37110-15277a)/123.6=2092
    # 453.7a+0.17233*(37110-15277a)=2092
    # 453.7a+6395-2632.5a=2092
    # -2178.8a=-4303 => a=1.975, b=(37110-30172)/123.6=56.1
    # Check x=88.2: 1.975*7779+56.1*88.2=15364+4948=20312 vs 21854 (7% off)
    # x=58.8: 1.975*3457+56.1*58.8=6828+3299=10127 vs 10583 (4% off)
    # x=30.3: 1.975*918+56.1*30.3=1813+1700=3513 vs 3514. 
    # x=21.3: 1.975*453.7+56.1*21.3=896+1195=2091 vs 2092. 
    # x=28.4: 1.975*806.6+56.1*28.4=1593+1593=3186 vs 3173. 
    # x=47.1: 1.975*2218+56.1*47.1=4381+2642=7023 vs 7234 (3% off)
    # x=65.5: 1.975*4290+56.1*65.5=8473+3675=12148 vs 12780 (5% off)
    # x=104.5: 1.975*10920+56.1*104.5=21567+5862=27429 vs 28879 (5% off)
    # x=123.6: 1.975*15277+56.1*123.6=30172+6934=37106 vs 37110. 
    # Good fit! y = 1.975*x^2 + 56.1*x for x>0 (above floor).
    # Negative side: points (-102.2,16586),(-61.7,5086),(-55.8,3928),(-50.4,2995),(-48.6,2711),(-63.9,5554)
    # Fit y=a*x^2+b*x (x negative): 
    # -102.2: a*10445+b*(-102.2)=16586
    # -48.6: a*2362+b*(-48.6)=2711
    # From 2nd: b=(2711-2362a)/(-48.6)=(2362a-2711)/48.6
    # 10445a -102.2*(2362a-2711)/48.6=16586
    # 10445a -2.1029*(2362a-2711)=16586
    # 10445a -4967a+5701=16586
    # 5478a=10885 => a=1.987, b=(2362*1.987-2711)/48.6=(4693-2711)/48.6=40.8
    # Check -61.7: 1.987*3807+40.8*(-61.7)=7564-2517=5047 vs 5086. 
    # -55.8: 1.987*3114+40.8*(-55.8)=6188-2277=3911 vs 3928. 
    # -50.4: 1.987*2540+40.8*(-50.4)=5047-2056=2991 vs 2995. 
    # -63.9: 1.987*4083+40.8*(-63.9)=8113-2607=5506 vs 5554. 
    # -102.2: 1.987*10445+40.8*(-102.2)=20754-4170=16584 vs 16586. 
    # Excellent! y = 1.987*x^2 + 40.8*x for x<0.
    # Both sides similar a~1.98, b differs (56 vs 41). Floor at -20.4469.
    # Floor region: |x| small. Where does it transition? 
    # x=21.3 gives 2092 (above floor). x=-16.9 gives -20.4469 (floor). x=-7.1 floor.
    # Need boundary. For positive: formula at x=10: 1.975*100+56.1*10=759. At x=5: 49+280=329. 
    # But floor is -20.4469. So floor applies when formula < -20.4469? For x>0 formula always positive. 
    # So positive side never hits floor. But x=1.2 gives -20.4469! Contradiction.
    # So for small x, output is floor regardless. There's a threshold.
    # x=1.2 floor, x=21.3 -> 2092. x=-16.9 floor, x=-48.6 -> 2711.
    # Maybe threshold around |x|<~20? Need to guess. 
    # x=21.3 -> 2092 (not floor). x=-16.9 floor. So positive threshold <21.3, negative threshold >16.9.
    # Let's guess symmetric threshold at |x|<~18 or so. Actually check formula at x=18: 1.975*324+56.1*18=640+1010=1650. 
    # But observed floor at -16.9. So threshold between 16.9 and 21.3. Guess ~18-20.
    # Actually maybe the floor is where the MLP saturates. Let's just use: if formula result < some threshold, return floor.
    # For negative: formula at x=-16.9: 1.987*285.6+40.8*(-16.9)=567-690=-123. That's < -20.4469, so floor! 
    # At x=-20: 1.987*400+40.8*(-20)=795-816=-21. Close to floor. 
    # At x=-21: 1.987*441+40.8*(-21)=876-857=19. Above floor.
    # For positive: formula at x=1.2: 1.975*1.44+56.1*1.2=2.8+67=70. That's > floor, but observed floor!
    # So positive small x also floor. Hmm. Maybe floor applies when |x| < threshold regardless.
    # x=21.3 -> 2092, formula gives 2091. So formula works at 21.3. x=1.2 floor.
    # Threshold between 1.2 and 21.3 for positive. 
    # Let's just use: if |x| < 18: return -20.4469, else formula. Mark as uncertain.
    # Actually maybe it's max(-20.4469, formula) but formula for small x should be < -20.4469. 
    # For positive formula at x=1.2 = 70 > -20. So max wouldn't give floor. So there's a dead zone.
    # Use threshold ~18.
    def f(x):
        if abs(x) < 18:
            return -20.4469
        if x >= 0:
            return 1.975*x*x + 56.1*x
        else:
            return 1.987*x*x + 40.8*x
    return {"y": [f(x) for x in probe["x"]]}
