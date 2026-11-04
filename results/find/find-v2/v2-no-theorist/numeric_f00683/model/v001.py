def predict(probe):
    # Piecewise function with a discontinuity at x=0 [E2]
    # Negative side: linear, y = 1.38*x - 10.74 approx [E2: x=-128->-176.58, x=-1->-12.21]
    #   slope = (-12.21 - -176.58)/(127) = 164.37/127 = 1.294; intercept: -12.21 = 1.294*(-1)+b -> b=-10.92
    # Positive side: quadratic, y = 0.1021*x^2 + 0.5*x + 7.0 approx [E2: x=1->7.6, x=128->1673.3]
    #   x^2/9.8? Let's fit: x=128 -> 1673.3, x=64->833.9, x=40->518.5, x=20->257.5, x=10->126.5, x=5->61.0, x=2->23.7, x=1->7.6
    #   Differences: looks like ~0.1021*x^2 + 0.5*x + 7.0
    # At x=0: -384.12 (special value, discontinuity) [E2]
    # Check E1 positive: x=88.2 -> 0.1021*7779.24 + 44.1 + 7 = 794.3+44.1+7=845.4? observed 1149.92. Hmm.
    # E1: x=66 -> 859.1; x=72.7 -> 946.87; x=21.3 -> 273.53; x=2.9 -> 33.49
    # Try y = x^2/6 + x + 7? x=66: 726+66+7=799 no.
    # Try y = 0.2*x^2 + 0.5*x + 7? x=66: 871.2+33+7=911 no.
    # Fit from E1: (66,859.1),(72.7,946.87),(21.3,273.53),(2.9,33.49),(88.2,1149.92)
    # Differences: 88.2-72.7=15.5, 1149.92-946.87=203.05 -> slope ~13.1
    # 72.7-66=6.7, 946.87-859.1=87.77 -> slope ~13.1
    # 21.3-2.9=18.4, 273.53-33.49=240.04 -> slope ~13.05
    # So positive side is linear with slope ~13.1? But E2 shows quadratic...
    # Wait E2 positive: x=1->7.6, x=2->23.7 (diff 16.1), x=5->61 (diff 37.3 over 3 -> 12.4), x=10->126.5 (diff 65.5 over 5 ->13.1), x=20->257.5 (diff 131 over 10 ->13.1), x=40->518.5 (diff 261 over 20 ->13.05), x=64->833.9 (diff 315.4 over 24 ->13.14), x=128->1673.3 (diff 839.4 over 64 ->13.12)
    # So positive side is LINEAR with slope ~13.1! Not quadratic.
    # Check: y = 13.1*x + b. x=10 -> 126.5, b = 126.5-131 = -4.5. x=1 -> 13.1-4.5=8.6 vs 7.6. x=128 -> 1676.8-4.5=1672.3 vs 1673.3. Close.
    # Fit better: slope from x=10 to x=128: (1673.3-126.5)/118 = 1546.8/118 = 13.108. b = 126.5 - 131.08 = -4.58
    # x=1: 13.108-4.58 = 8.53 vs 7.6. x=2: 26.2-4.58=21.6 vs 23.7. Hmm not perfect.
    # Try y = 13.1*x - 4.6 + something? x=2: 26.2-4.6=21.6 vs 23.7 (diff 2.1); x=1: 13.1-4.6=8.5 vs 7.6 (diff -0.9)
    # Maybe there's a small quadratic term. Fit quadratic through (10,126.5),(64,833.9),(128,1673.3):
    # a*100+b*10+c=126.5; a*4096+b*64+c=833.9; a*16384+b*128+c=1673.3
    # Subtract: a*3996+b*54=707.4; a*12288+b*64=839.4
    # From first: b=(707.4-3996a)/54. Second: 12288a+64*(707.4-3996a)/54=839.4
    # 12288a + (64/54)*707.4 - (64/54)*3996a = 839.4
    # 12288a + 838.4 - 4736a = 839.4 -> 7552a = 1.0 -> a=0.000132
    # b = (707.4-0.528)/54 = 13.09; c = 126.5 - 0.0132 - 130.9 = -4.41
    # Check x=1: 0.000132+13.09-4.41=8.68 vs 7.6. Still off.
    # Hmm. Let's check E1 with linear 13.1x-4.6: x=66 -> 864.6-4.6=860 vs 859.1 good. x=72.7->952.4-4.6=947.8 vs 946.87 good. x=88.2->1155.4-4.6=1150.8 vs 1149.92 good. x=21.3->279-4.6=274.4 vs 273.53 good. x=2.9->38-4.6=33.4 vs 33.49 good!
    # So positive side: y ≈ 13.1*x - 4.6. Small deviations at small x.
    # Actually maybe y = 13.1*x - 4.6 exactly? x=1: 8.5 vs 7.6 (off 0.9). x=2: 21.6 vs 23.7 (off 2.1). x=5: 65.5-4.6=60.9 vs 61.0 good!
    # Hmm x=1,2 off. Maybe there's a small quadratic: y = 13.1x - 4.6 + k*(x-5)(x-10)? At x=1: k*4*9=36k=0.9 -> k=0.025; x=2: k*3*8=24k=0.6 vs need 2.1. No.
    # Let me just use linear 13.1x - 4.6, small errors at x=1,2 acceptable.
    # Negative side E1: x=-20.3->-37.493; x=-61.7->-91.727; x=-24.3->-39.733; x=-50.4->-75.924; x=-6.0->-16.76
    # Slope: (-91.727 - -37.493)/(-61.7 - -20.3) = -54.234/-41.4 = 1.310
    # b: -37.493 = 1.310*(-20.3)+b -> b = -37.493+26.59 = -10.90
    # Check x=-6: 1.31*-6-10.9 = -7.86-10.9=-18.76 vs -16.76. Off by 2.
    # x=-24.3: 1.31*-24.3-10.9=-31.83-10.9=-42.73 vs -39.733. Off by 3.
    # Hmm. E2 negative: x=-128->-176.58, x=-96->-136.66, x=-64->-94.74, x=-40->-61.3, x=-30->-50.2, x=-20->-37.1, x=-15->-30.55, x=-10->-24.0, x=-5->-17.45, x=-2->-13.52, x=-1->-12.21
    # Slope from -128 to -1: (-12.21 - -176.58)/127 = 164.37/127 = 1.294
    # b: -12.21 = 1.294*(-1)+b -> b=-10.916
    # Check x=-5: 1.294*-5-10.916=-6.47-10.916=-17.39 vs -17.45 good
    # x=-10: -12.94-10.916=-23.86 vs -24.0 good
    # x=-20: -25.88-10.916=-36.8 vs -37.1 good
    # x=-40: -51.76-10.916=-62.68 vs -61.3 off 1.4
    # x=-64: -82.82-10.916=-93.74 vs -94.74 off 1
    # x=-96: -124.2-10.916=-135.1 vs -136.66 off 1.5
    # x=-128: -165.6-10.916=-176.5 vs -176.58 good!
    # Hmm inconsistent. Maybe slight quadratic. Let's fit quadratic through (-128,-176.58),(-64,-94.74),(-1,-12.21):
    # a*16384 - b*128 + c = -176.58; a*4096 - b*64 + c = -94.74; a - b + c = -12.21
    # Subtract eq1-eq2: 12288a - 64b = -81.84; eq2-eq3: 4095a - 63b = -82.53
    # From first: b = (12288a+81.84)/64 = 192a + 1.279
    # Second: 4095a - 63(192a+1.279) = -82.53 -> 4095a - 12096a - 80.58 = -82.53 -> -8001a = -1.95 -> a=0.000244
    # b = 192*0.000244+1.279 = 1.326; c = -12.21 + b - a = -12.21+1.326-0.000244 = -10.884
    # Check x=-20: 0.000244*400 - 1.326*20 - 10.884 = 0.0976 - 26.52 - 10.884 = -37.3 vs -37.1 good
    # x=-40: 0.39 - 53.04 - 10.884 = -63.5 vs -61.3 off 2.2. Hmm.
    # Let me just use linear 1.3x - 10.9 for negative side, small errors.
    # Actually E1 negative: x=-20.3->-37.493. Linear: 1.3*-20.3-10.9=-26.39-10.9=-37.29 vs -37.493 good!
    # x=-61.7: 1.3*-61.7-10.9=-80.21-10.9=-91.11 vs -91.727 off 0.6
    # x=-24.3: -31.59-10.9=-42.49 vs -39.733 off 2.7. Hmm.
    # Let me try slope 1.31, b=-10.9: x=-24.3: -31.83-10.9=-42.73 vs -39.733 off 3.
    # Weird. x=-6: 1.31*-6-10.9=-18.76 vs -16.76 off 2.
    # Maybe negative side also has quadratic: y = 0.000244x^2 + 1.326x - 10.884? x=-6: 0.0088-7.956-10.884=-18.83 vs -16.76 off 2.
    # Hmm. Let me try y = 1.3x - 10.9 + small correction. x=-6: -18.7 vs -16.76. Need +1.94.
    # x=-24.3: -42.49 vs -39.733. Need +2.76.
    # x=-20.3: -37.29 vs -37.493. Need -0.2.
    # Inconsistent. Maybe noise? "output could be noisy."
    # Let me just use linear fits: negative y=1.294x-10.92, positive y=13.1x-4.6, x=0 special -384.12.
    # Actually wait, maybe negative side is also quadratic but with different coefficient.
    # Let me check E2 negative more carefully for quadratic:
    # x=-1->-12.21, x=-2->-13.52 (diff -1.31), x=-5->-17.45 (diff -3.93 over 3 = -1.31), x=-10->-24.0 (diff -6.55 over 5 = -1.31), x=-15->-30.55 (diff -6.55 over 5=-1.31), x=-20->-37.1 (diff -6.55 over 5=-1.31), x=-30->-50.2 (diff -13.1 over 10=-1.31), x=-40->-61.3 (diff -11.1 over 10=-1.11), x=-64->-94.74 (diff -33.44 over 24=-1.393), x=-96->-136.66 (diff -41.92 over 32=-1.31), x=-128->-176.58 (diff -39.92 over 32=-1.2475)
    # Mostly slope -1.31, with some noise. So negative side: y = -1.31*x - 10.9 (since slope is -1.31 means y decreases as x decreases... wait)
    # Actually as x goes from -1 to -128, y goes from -12.21 to -176.58, so y decreases. Slope = dy/dx = (-176.58 - -12.21)/(-128 - -1) = -164.37/-127 = 1.294. So y = 1.294x + b. b = -12.21 - 1.294*(-1) = -12.21+1.294 = -10.916.
    # So negative side: y = 1.294x - 10.916. Let me verify x=-5: 1.294*-5-10.916 = -6.47-10.916 = -17.39 vs -17.45. Good.
    # x=-20: -25.88-10.916 = -36.8 vs -37.1. Off 0.3 (noise).
    # x=-40: -51.76-10.916 = -62.68 vs -61.3. Off 1.4. Hmm.
    # x=-64: -82.82-10.916 = -93.74 vs -94.74. Off 1.
    # x=-96: -124.2-10.916 = -135.1 vs -136.66. Off 1.5.
    # x=-128: -165.6-10.916 = -176.5 vs -176.58. Good.
    # So mostly linear with slope ~1.294, some noise.
    # Positive side: y = 13.1x - 4.6. Check E2: x=1: 8.5 vs 7.6 (off 0.9), x=2: 21.6 vs 23.7 (off 2.1), x=5: 60.9 vs 61.0 good, x=10: 126.4 vs 126.5 good, x=20: 257.4 vs 257.5 good, x=40: 519.4 vs 518.5 good, x=64: 833.8 vs 833.9 good, x=128: 1672.2 vs 1673.3 good.
    # So positive side linear 13.1x - 4.6, with small deviations at x=1,2.
    # Maybe there's a small quadratic term: y = 13.1x - 4.6 + k*x*(x-5)? At x=1: k*1*(-4)=-4k=0.9 -> k=-0.225; x=2: k*2*(-3)=-6k=1.35 vs need 2.1. No.
    # Let me just use linear. The deviations at x=1,2 might be noise or a small quadratic.
    # Actually let me reconsider: maybe positive side is y = 13.1x - 4.6 + 0.02*x^2? x=1: 13.1-4.6+0.02=8.52 vs 7.6. No.
    # Let me try y = 13.1x - 4.6 + c/x? x=1: 8.5+c=7.6 -> c=-0.9; x=2: 21.6-0.45=21.15 vs 23.7. No.
    # OK just linear. Small errors at x=1,2.
    # Actually, maybe the positive side is y = 13.1x - 4.6 for x>=5, and something else for 0<x<5?
    # x=1->7.6, x=2->23.7, x=5->61.0. Linear through (1,7.6),(2,23.7): slope 16.1, b=-8.5. x=5: 80.5-8.5=72 vs 61. No.
    # Through (2,23.7),(5,61): slope 12.43, b=-1.17. x=1: 11.26 vs 7.6. No.
    # Hmm. Maybe there's a quadratic: y = ax^2+bx+c through (1,7.6),(2,23.7),(5,61):
    # a+b+c=7.6; 4a+2b+c=23.7; 25a+5b+c=61
    # Subtract: 3a+b=16.1; 21a+3b=37.3 -> 7a+b=12.43
    # Subtract: 4a=-3.67 -> a=-0.9175; b=16.1+2.75=18.85; c=7.6-(-0.9175)-18.85=-10.33
    # Check x=10: -91.75+188.5-10.33=86.4 vs 126.5. No.
    # So not quadratic. Linear it is.
    # Let me just use: x<0: y=1.294x-10.916; x=0: -384.12; x>0: y=13.1x-4.6
    # Actually let me reconsider the positive side more carefully. E1: x=2.9->33.49. Linear: 13.1*2.9-4.6=37.99-4.6=33.39 vs 33.49 good!
    # x=21.3: 279.03-4.6=274.43 vs 273.53 off 0.9
    # x=66: 864.6-4.6=860 vs 859.1 off 0.9
    # x=72.7: 952.37-4.6=947.77 vs 946.87 off 0.9
    # x=88.2: 1155.42-4.6=1150.82 vs 1149.92 off 0.9
    # Interesting, all off by ~0.9. So maybe y = 13.1x - 5.5? x=2.9: 37.99-5.5=32.49 vs 33.49. No.
    # Or y = 13.1x - 4.6 - 0.9 = 13.1x - 5.5? x=10: 131-5.5=125.5 vs 126.5. Off 1.
    # Hmm. Let me fit slope from E1: (1149.92-33.49)/(88.2-2.9) = 1116.43/85.3 = 13.088
    # b: 33.49 = 13.088*2.9+b -> b = 33.49-37.96 = -4.47
    # Check x=66: 13.088*66-4.47 = 863.8-4.47=859.33 vs 859.1 good
    # x=72.7: 951.5-4.47=947.03 vs 946.87 good
    # x=88.2: 1154.4-4.47=1149.9 vs 1149.92 good!
    # x=21.3: 278.77-4.47=274.3 vs 273.53 off 0.8
    # So slope ~13.088, b~-4.47. Check E2: x=128: 1675.3-4.47=1670.8 vs 1673.3 off 2.5. Hmm.
    # x=64: 837.6-4.47=833.1 vs 833.9 good
    # x=40: 523.5-4.47=519.0 vs 518.5 good
    # x=20: 261.76-4.47=257.3 vs 257.5 good
    # x=10: 130.88-4.47=126.4 vs 126.5 good
    # x=5: 65.44-4.47=60.97 vs 61.0 good
    # x=2: 26.18-4.47=21.7 vs 23.7 off 2
    # x=1: 13.09-4.47=8.62 vs 7.6 off 1
    # So slope 13.088, b=-4.47 fits most, with x=1,2,128 off.
    # Maybe there's a small quadratic term: y = 13.088x - 4.47 + k*x*(x-64)? At x=128: k*128*64=8192k=2.5 -> k=0.000305
    # x=1: k*1*(-63)=-0.019 vs need -1.02. No.
    # Let me just use y = 13.1x - 4.6 for positive. Good enough.
    # Actually let me use the E1 fit: 13.088x - 4.47. And negative: 1.294x - 10.916.
    # x=0: -384.12
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                y = 1.294 * x - 10.916
            elif x == 0:
                y = -384.12
            else:
                y = 13.088 * x - 4.47
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
