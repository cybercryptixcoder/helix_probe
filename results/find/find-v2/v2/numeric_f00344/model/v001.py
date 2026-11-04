def predict(probe):
    # f(x) = 472.73 at x=0 [E2]
    # For x>0: y = 472.73 - something growing; at x=0.1 y=-36.95, so drop ~509.7 [E2]
    # Looks like y ≈ 472.73 - a*x^b with a large coefficient; check ratios [E2]
    # x=1: -41.7 => drop 514.43; x=2: -79.6 => drop 552.33; x=3: -211.7 => drop 684.43
    # x=4: -528 => drop 1000.73; x=5: -1147.3 => drop 1620.03; x=6: -2217.2 => drop 2689.93
    # Differences of drops: 4.73, 37.9, 132.1, 316.3, 619.3, 1069.9 ... roughly cubic-ish?
    # Try y = 472.73 - c*x^4: x=1 drop 514.43 => c=514.43; x=2: 514.43*16=8230 too big. No.
    # Try exponential: drop at x: 514.43,552.33,684.43,1000.73,1620.03,2689.93
    # log(drop): 6.24,6.31,6.53,6.91,7.39,7.90 -> slope ~ (7.90-6.24)/5 ≈ 0.33 per unit... 
    # Actually drop(0.1)=509.7, drop(1)=514.43: nearly flat then growing. Hmm.
    # Consider y = 472.73 - A*(exp(k*x)-1) - B*x? 
    # At x=0.1: 509.7; x=1: 514.43. If exp term: A*(e^k -1)≈514 and A*(e^{0.1k}-1)≈509.7
    # ratio (e^k-1)/(e^{0.1k}-1) ≈ 1.0093. For small k this ratio ≈ 10. So k must be tiny -> no.
    # Maybe y = 472.73 - a*x^b with b<1 near 0? x=0.1 drop 509.7, x=1 drop 514.43: ratio 1.0093 = 10^{-b}? no, (0.1)^b vs 1: 0.1^b=509.7/514.43=0.9908 => b≈0.004. Then x=2: 2^0.004≈1.0028 => drop 515.9, but actual 552. No.
    # Reconsider: maybe there's a constant offset plus power. y = C - a*x^b.
    # Fit with three points x=1,2,3: -41.7, -79.6, -211.7
    # drops from C: C+41.7, C+79.6, C+211.7 proportional to 1,2^b,3^b
    # (C+79.6)/(C+41.7)=2^b, (C+211.7)/(C+41.7)=3^b
    # Try C=472.73: 552.33/514.43=1.0737=2^b => b=0.1025; 684.43/514.43=1.3305=3^b => b=0.2605. inconsistent.
    # Try larger C. Let r2=2^b, r3=3^b, r3=r2^{log3/log2}=r2^1.585
    # (C+79.6)=r2(C+41.7); (C+211.7)=r2^1.585(C+41.7)
    # Let u=C+41.7. Then C+79.6=u+37.9, C+211.7=u+170.
    # (u+37.9)/u=r2; (u+170)/u=r2^1.585
    # Try u=1000: r2=1.0379, r2^1.585=1.0607, u*1.0607=1060.7 vs 1170. no
    # Try u=500: r2=1.0758, r2^1.585=1.1231, 500*1.1231=561.5 vs 670. no
    # Try u=300: r2=1.1263, r2^1.585=1.2074, 300*1.2074=362 vs 470. no
    # Try u=200: r2=1.1895, r2^1.585=1.3155, 200*1.3155=263 vs 370. no
    # Try u=150: r2=1.2527, r2^1.585=1.4273, 150*1.4273=214 vs 320. no
    # Try u=120: r2=1.3158, r2^1.585=1.5425, 120*1.5425=185 vs 290. no
    # Hmm, need (u+170)/(u+37.9) = r2^0.585. 
    # Let me just try polynomial fit. Points (1,-41.7),(2,-79.6),(3,-211.7),(4,-528),(5,-1147.3),(6,-2217.2)
    # Differences: -37.9,-132.1,-316.3,-619.3,-1069.9
    # 2nd diff: -94.2,-184.2,-303,-450.6
    # 3rd diff: -90,-118.8,-147.6
    # 4th diff: -28.8,-28.8 -> constant! So quartic in x for these points.
    # 4th diff constant -28.8 means leading coeff = -28.8/24 = -1.2, so -1.2 x^4.
    # Check x=6: -1.2*1296=-1555.2, plus lower terms. Let's fit.
    # y = -1.2x^4 + a x^3 + b x^2 + c x + d
    # x=1: -1.2+a+b+c+d=-41.7
    # x=2: -19.2+8a+4b+2c+d=-79.6
    # x=3: -97.2+27a+9b+3c+d=-211.7
    # x=4: -307.2+64a+16b+4c+d=-528
    # x=5: -750+125a+25b+5c+d=-1147.3
    # x=6: -1555.2+216a+36b+6c+d=-2217.2
    # From x=1: a+b+c+d=-40.5
    # x=2 minus x=1: 7a+3b+c=-38.7  (since -19.2+19.2... wait recompute)
    # x=2 - x=1: (-19.2+8a+4b+2c+d)-(-1.2+a+b+c+d) = -79.6-(-41.7)=-37.9
    #   => -18+7a+3b+c = -37.9 => 7a+3b+c = -19.9
    # x=3-x=2: (-97.2+27a+9b+3c+d)-(-19.2+8a+4b+2c+d)=-211.7+79.6=-132.1
    #   => -78+19a+5b+c=-132.1 => 19a+5b+c=-54.1
    # x=4-x=3: (-307.2+64a+16b+4c+d)-(-97.2+27a+9b+3c+d)=-528+211.7=-316.3
    #   => -210+37a+7b+c=-316.3 => 37a+7b+c=-106.3
    # x=5-x=4: (-750+125a+25b+5c+d)-(-307.2+64a+16b+4c+d)=-1147.3+528=-619.3
    #   => -442.8+61a+9b+c=-619.3 => 61a+9b+c=-176.5
    # x=6-x=5: (-1555.2+216a+36b+6c+d)-(-750+125a+25b+5c+d)=-2217.2+1147.3=-1069.9
    #   => -805.2+91a+11b+c=-1069.9 => 91a+11b+c=-264.7
    # From eq1: 7a+3b+c=-19.9; eq2: 19a+5b+c=-54.1 => 12a+2b=-34.2 => 6a+b=-17.1
    # eq2-eq3: 19a+5b+c - (37a+7b+c) = -54.1+106.3=52.2 => -18a-2b=52.2 => 9a+b=-26.1
    # Subtract: 3a=-9 => a=-3, b=-17.1-6(-3)=-17.1+18=0.9
    # c from eq1: 7(-3)+3(0.9)+c=-19.9 => -21+2.7+c=-19.9 => c=-1.6
    # d from a+b+c+d=-40.5: -3+0.9-1.6+d=-40.5 => -3.7+d=-40.5 => d=-36.8
    # Check x=6: -1555.2+216(-3)+36(0.9)+6(-1.6)-36.8 = -1555.2-648+32.4-9.6-36.8=-2217.2 ✓
    # So y = -1.2x^4 -3x^3 +0.9x^2 -1.6x -36.8 for x in [1,6]
    # Check x=0: -36.8, but observed 472.73! So x=0 is special.
    # Check x=0.1: -1.2*0.0001 -3*0.001+0.9*0.01-0.16-36.8 = -0.00012-0.003+0.009-0.16-36.8≈-36.95 ✓
    # Check x=0.5: -1.2*0.0625-3*0.125+0.9*0.25-0.8-36.8=-0.075-0.375+0.225-0.8-36.8=-37.825 ✓
    # So the quartic holds for x in (0,6], but x=0 gives 472.73. Interesting.
    # Check x=8: -1.2*4096-3*512+0.9*64-1.6*8-36.8 = -4915.2-1536+57.6-12.8-36.8=-6443.2 ✓
    # x=10: -12000-3000+90-16-36.8=-14962.8 ✓
    # x=12: -1.2*20736-3*1728+0.9*144-19.2-36.8=-24883.2-5184+129.6-56=-29993.6 ✓
    # x=15: -1.2*50625-3*3375+0.9*225-24-36.8=-60750-10125+202.5-60.8=-70733.3 ✓
    # x=20: -1.2*160000-3*8000+0.9*400-32-36.8=-192000-24000+360-68.8=-215708.8 ✓
    # x=25: -1.2*390625-3*15625+0.9*625-40-36.8=-468750-46875+562.5-76.8=-515139.3 ✓
    # x=30: -1.2*810000-3*27000+0.9*900-48-36.8=-972000-81000+810-84.8=-1052274.8 ✓
    # x=40: -1.2*2560000-3*64000+0.9*1600-64-36.8=-3072000-192000+1440-100.8=-3262660.8 ✓
    # x=50: -1.2*6250000-3*125000+0.9*2500-80-36.8=-7500000-375000+2250-116.8=-7872866.8 ✓
    # x=60: -1.2*12960000-3*216000+0.9*3600-96-36.8=-15552000-648000+3240-132.8=-16196892.8 ✓
    # x=70: -1.2*24010000-3*343000+0.9*4900-112-36.8=-28812000-1029000+4410-148.8=-29836738.8 ✓
    # So quartic holds for all x>0 tested. x=0 is special (472.73).
    # Now check E1 negative values with same quartic:
    # x=-20.3: -1.2*(20.3^4)-3*(-20.3^3)+0.9*(20.3^2)-1.6*(-20.3)-36.8
    #   20.3^2=412.09, ^3=8365.427, ^4=169818.17
    #   = -203781.8+25096.28+370.88+32.48-36.8 = -178318.96 vs observed -178293.86. Close but not exact!
    #   diff ~25. Hmm. Maybe coefficient slightly off or rounding.
    # x=-6: -1.2*1296-3*(-216)+0.9*36-1.6*(-6)-36.8 = -1555.2+648+32.4+9.6-36.8=-901.99 vs -876.9. diff 25.
    # x=-24.3: 24.3^2=590.49,^3=14348.9,^4=348678.4
    #   -1.2*348678.4+3*14348.9+0.9*590.49+38.88-36.8 = -418414.1+43046.7+531.44+2.08=-374833.9 vs -374808.79. diff 25.
    # Consistent +25 offset for negatives? Let me check x=-50.4:
    #   50.4^2=2540.16,^3=128024.06,^4=6452412.9
    #   -1.2*6452412.9+3*128024.06+0.9*2540.16+80.64-36.8=-7742895.5+384072.2+2286.1+43.84=-7356493.4 vs -7356468.11. diff 25.3.
    # x=-61.7: 61.7^2=3806.89,^3=234885.1,^4=14492410.9
    #   -1.2*14492410.9+3*234885.1+0.9*3806.89+98.72-36.8=-17390893.1+704655.3+3426.2+61.92=-16682749.7 vs -16682725.2. diff 24.5.
    # x=-20.3 gave diff 25.1. x=-24.3 diff 25.1. So negatives have ~+25 offset.
    # Hmm but x=0.1,0.5 etc were positive and matched exactly. Let me recheck x=-6 carefully.
    # Actually maybe the quartic is exact and I have rounding. Let me recompute x=-6:
    # -1.2*1296 = -1555.2; -3*(-216)=+648; 0.9*36=32.4; -1.6*(-6)=9.6; -36.8
    # sum: -1555.2+648=-907.2; +32.4=-874.8; +9.6=-865.2; -36.8=-902.0. Observed -876.9. diff 25.1.
    # So negatives differ by ~+25. Could be a different branch for x<0.
    # Let me check if maybe it's +25 constant for x<0. Test x=-20.3: predicted -178318.96+25=-178293.96 vs -178293.86 ✓
    # x=-24.3: -374833.9+25=-374808.9 vs -374808.79 ✓
    # x=-50.4: -7356493.4+25=-7356468.4 vs -7356468.11 ✓
    # x=-61.7: -16682749.7+25=-16682724.7 vs -16682725.2 ✓
    # x=-6: -902+25=-877 vs -876.9 ✓
    # So for x<0: y = quartic + 25. For x>0: y = quartic. For x=0: y=472.73.
    # Check positive large values again with +0 offset - they matched. Good.
    # But wait, is x=0 really special or is it a discontinuity? Let me check x=0.1 gave -36.95 which is quartic (no +25).
    # So x=0 -> 472.73, x>0 -> quartic, x<0 -> quartic+25.
    # Hmm, but maybe the +25 for negatives is actually a different constant. Let me verify more carefully.
    # Actually maybe the rule is: for x<0, y = quartic(x) + 25; for x>=0, y=quartic(x); except x=0 gives 472.73.
    # Or maybe x=0 is a special case and the +25 is because of something else.
    # Let me reconsider: maybe the base function is quartic and there's a piecewise adjustment.
    # Given evidence, I'll model: 
    #   x == 0: 472.73
    #   x > 0: quartic
    #   x < 0: quartic + 25
    # But +25 seems arbitrary. Let me double check with more precision on one.
    # x=-20.3: 20.3^4 = 169818.1681; *-1.2 = -203781.80172
    #   20.3^3=8365.427; *-3*(-1)=+25096.281 (since -3x^3, x^3 negative, so +)
    #   20.3^2=412.09; *0.9=370.881
    #   -1.6*(-20.3)=32.48
    #   -36.8
    #   sum: -203781.80172+25096.281=-178685.52072; +370.881=-178314.63972; +32.48=-178282.15972; -36.8=-178318.95972
    # observed -178293.8597. diff = 25.1. Yes.
    # So +25.1? Let me check x=-6: diff was 25.1. x=-24.3: 25.1. So it's ~25.1, maybe exactly 25.1? or 25?
    # x=-50.4: -7356493.4+25.1=-7356468.3 vs -7356468.1147. diff 0.19. Hmm.
    # Let me be more precise. x=-50.4: 50.4^4: 50.4^2=2540.16; ^4=6452412.8256; *-1.2=-7742895.39072
    #   50.4^3=128024.064; *3=384072.192
    #   2540.16*0.9=2286.144
    #   1.6*50.4=80.64
    #   -36.8
    #   sum: -7742895.39072+384072.192=-7358823.19872; +2286.144=-7356537.05472; +80.64=-7356456.41472; -36.8=-7356493.21472
    # observed -7356468.1147. diff = 25.1. 
    # x=-61.7: 61.7^2=3806.89; ^4=14492410.9... let me: 3806.89^2=14492410.9 (approx)
    #   61.7^3=234885.113; *3=704655.339
    #   3806.89*0.9=3426.201
    #   1.6*61.7=98.72
    #   -36.8
    #   -1.2*14492410.9=-17390893.08
    #   sum: -17390893.08+704655.339=-16686237.741; +3426.201=-16682811.54; +98.72=-16682712.82; -36.8=-16682749.62
    # observed -16682725.2065. diff=24.4. Hmm, not exactly 25.1.
    # Let me recompute 61.7^4 precisely: 61.7^2=3806.89. 3806.89^2 = 14492410.9... 
    #   3806.89*3806.89: 3806.89*3800=14466182; 3806.89*6.89=26229.47; total=14492411.47
    #   *-1.2=-17390893.76
    #   sum: -17390893.76+704655.339=-16686238.42; +3426.201=-16682812.22; +98.72=-16682713.5; -36.8=-16682750.3
    # observed -16682725.2. diff=25.1. OK good, 25.1.
    # So +25.1 for x<0. Let me use 25.1.
    # Actually, could it be that the quartic coefficients are slightly different and there's no offset? 
    # The positive side matched exactly with -1.2,-3,0.9,-1.6,-36.8. So negatives need +25.1.
    # I'll go with +25.1 for x<0. Mark with ? since it's odd.
    import math
    def quartic(x):
        return -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x - 36.8
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(472.73)
            elif x > 0:
                out.append(quartic(x))
            else:
                out.append(quartic(x) + 25.1)  # ? offset for negatives
        except Exception:
            out.append(None)
    return {"y": out}
