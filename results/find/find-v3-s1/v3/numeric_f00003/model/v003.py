import math

def predict(probe):
    # Beliefs about f(x):
    # - Flat floor at -20.4469 for |x| small; floor ends near |x|~24 on both sides [E2,E4,E6,E8]
    # - Positive side: smooth curve. Small x linear-ish slope 126 [E2,E4,E6]; 
    #   then smooth quadratic-like growth. Large x (90-128) is LINEAR slope ~490.9/unit [E12]
    #   E12: 90->22629.9, 128->39006.1: slope (39006.1-22629.9)/38 = 430.9? 
    #   Check consecutive: 95-90: 2154.76/5=430.95; 100-95:2154.76/5=430.95; uniform 430.95/unit!
    #   So for x>=~88: f = 22629.9235 + 430.95*(x-90) = 430.95*x - 16155.6
    #   Check 128: 430.95*128-16155.6=55161.6-16155.6=39006.0 ✓
    # - Mid positive (30-80): E8: 30->3458.1, 80->18320.4. E12: 60->10960,70->14370,80->18320
    #   60->70: 3410/10=341; 70->80: 3950/10=395. Increasing slope -> quadratic-ish.
    #   Fit quadratic a*x^2+b*x+c through 30,60,90? 30->3458.1,60->10960,90->22629.9
    #   900a+30b+c=3458.1; 3600a+60b+c=10960; 8100a+90b+c=22629.9
    #   (2)-(1): 2700a+30b=7501.9 -> 90a+b=250.06
    #   (3)-(2): 4500a+30b=11669.9 -> 150a+b=388.997
    #   Subtract: 60a=138.93 -> a=2.3156, b=250.06-208.4=41.66, c=3458.1-2084-1249.8=124.3
    #   Check 80: 2.3156*6400+41.66*80+124.3=14819.8+3332.8+124.3=18276.9 vs 18320 ✓
    #   Check 40: 2.3156*1600+41.66*40+124.3=3705+1666.4+124.3=5495.7 vs 5505.5 ✓
    #   Check 20: 2.3156*400+41.66*20+124.3=926.2+833.2+124.3=1883.7 vs 1914.2 close
    #   Check 10: 2.3156*100+416.6+124.3=231.6+416.6+124.3=772.5 vs 650.5 (off)
    #   Check 8: 2.3156*64+333.3+124.3=148.2+333.3+124.3=605.8 vs 398.2 (off)
    #   So quadratic good for x>=~20, but small x is linear slope 126.
    #   At x=20: linear 126*20-610=1910 vs 1914.2 ✓ (linear better!)
    #   At x=30: linear 126*30-610=3170 vs 3458 (quad 3458 exact). Quad better.
    #   Crossover ~22-25. Use linear for x<24, quad for x>=24.
    #   At x=24: linear 126*24-610=2414; quad 2.3156*576+41.66*24+124.3=1333.8+999.8+124.3=2457.9. Close.
    #   Use linear up to 24, quad after. Small discontinuity ok.
    # - Large positive x>=88: linear slope 430.95. But quad at 88: 2.3156*7744+41.66*88+124.3
    #   =17932+3666+124=21722 vs 21768 (E12 x=88). Close! And at 90 quad: 2.3156*8100+3749.4+124.3
    #   =18756+3749+124=22629.7 vs 22629.9 EXACT! So quad actually works at 90 too!
    #   Check 128 quad: 2.3156*16384+41.66*128+124.3=37938+5332+124=43394 vs 39006. WAY off.
    #   So quad works up to ~90, then linear. Crossover ~90.
    #   At 95 quad: 2.3156*9025+3957.7+124.3=20898+3958+124=24980 vs 24784.7 (off 0.8%)
    #   At 100 quad: 2.3156*10000+4166+124=23156+4166+124=27446 vs 26939 (off 1.9%)
    #   So linear takes over around 90. Use quad for x<90, linear for x>=90.
    #   At 90: quad 22629.7, linear 430.95*90-16155.6=38785.5-16155.6=22629.9. Match!
    # - Negative side: E8 shows floor ends between -24 and -25 (E8: -24->150, -25->204).
    #   Wait E8: -24->150.01, -25->204.01, -26->267.9, -27->334.5, -28->401.2, -29->470.9, -30->548.3
    #   E6: -20->-20.4, -22->54.0, -24->150.0, -26->267.9, -28->401.2
    #   So floor ends between -20 and -22. E6 -22->54.0 (above floor). 
    #   E8 -24->150.0. Check quadratic 1.618x^2-1066: -22: 1.618*484-1066=783-1066=-283. No.
    #   Let me fit negative side. E8: -24->150, -30->548.3, -36->1090.9
    #   -24^2=576, -30^2=900, -36^2=1296
    #   576a+b=150; 1296a+b=1090.9 -> 720a=940.9 -> a=1.3068, b=150-752.7=-602.7
    #   Check -30: 1.3068*900-602.7=1176.1-602.7=573.4 vs 548.3 (off)
    #   Check -26: 1.3068*676-602.7=883.4-602.7=280.7 vs 267.9 close
    #   Check -28: 1.3068*784-602.7=1024.5-602.7=421.8 vs 401.2 close
    #   Hmm. Try linear? -24->150, -36->1090.9: slope 940.9/12=78.4/unit
    #   -30: 150+78.4*6=620 vs 548. No, not linear.
    #   Try quadratic through -22 (54.0 from E6) and -36 (1090.9):
    #   484a+b=54; 1296a+b=1090.9 -> 812a=1036.9 -> a=1.277, b=54-618=-564
    #   Check -24: 1.277*576-564=735.6-564=171.6 vs 150 close
    #   Check -30: 1.277*900-564=1149.3-564=585.3 vs 548.3 (off 7%)
    #   Check -28: 1.277*784-564=1001.2-564=437.2 vs 401.2 (off 9%)
    #   Hmm. Let me use more points. E8: -24:150.01,-25:204.01,-26:267.92,-27:334.54,-28:401.15,-29:470.91,-30:548.25,-32:711.77,-34:891.11,-36:1090.92
    #   Diffs: 54.0, 63.9, 66.6, 66.6, 69.8, 77.3, 81.8(over2), 89.7(over2), 99.9(over2)
    #   Slope increasing. Quadratic fit through -24 and -36: a=1.3068,b=-602.7 gave -30:573 vs 548.
    #   Let me fit through -26 (267.92) and -36 (1090.92): 676a+b=267.92; 1296a+b=1090.92
    #   620a=823 -> a=1.327, b=267.92-897=-629
    #   Check -24: 1.327*576-629=764.4-629=135.4 vs 150 close
    #   Check -30: 1.327*900-629=1194.3-629=565.3 vs 548 (off 3%)
    #   Check -28: 1.327*784-629=1040.4-629=411.4 vs 401 (off 2.6%)
    #   Good enough. Use 1.327x^2-629 for negative side beyond floor.
    #   Floor end: 1.327x^2-629=-20.4469 -> x^2=608.5/1.327=458.6 -> |x|=21.4
    #   E6 -20->-20.4 (floor), -22->54.0 (above). So threshold ~21.4 ✓
    # - Large negative |x|: E1 -93.6->13835.8, -104->17162.4, -120.7->22504
    #   Quad 1.327x^2-629: -93.6: 1.327*8761-629=11626-629=10997 vs 13836. Off.
    #   -120.7: 1.327*14568-629=19332-629=18703 vs 22504. Off.
    #   So large negative is steeper. Linear? -93.6->13836, -120.7->22504: slope 8668/27.1=319.9/unit
    #   -104: 13836+319.9*10.4=17163 vs 17162 ✓ LINEAR slope 320 for |x|>=~90
    #   intercept: 13835.8-320*93.6=13835.8-29952=-16116
    #   Check -62.7: 320*62.7-16116=20064-16116=3948 vs 5294 (off, transition)
    #   Check -72.6 (E5): 320*72.6-16116=23232-16116=7116 vs 7597 (off 6%)
    #   Check -71.2 (E5): 320*71.2-16116=22784-16116=6668 vs 7249 (off 8%)
    #   So transition region -60 to -90. Quad at -72.6: 1.327*5271-629=6995-629=6366 vs 7597. Off.
    #   Hmm. Let me fit negative mid-large. E5: -72.6->7597, -71.2->7249. E1: -62.7->5294, -93.6->13836
    #   -62.7^2=3931, -72.6^2=5271, -93.6^2=8761
    #   3931a+b=5294; 8761a+b=13836 -> 4830a=8542 -> a=1.7685, b=5294-6952=-1658
    #   Check -72.6: 1.7685*5271-1658=9322-1658=7664 vs 7597 ✓
    #   Check -71.2: 1.7685*5069-1658=8965-1658=7307 vs 7249 ✓
    #   Check -104: 1.7685*10816-1658=19128-1658=17470 vs 17162 (off 1.8%)
    #   Check -120.7: 1.7685*14568-1658=25764-1658=24106 vs 22504 (off 7%)
    #   So quad 1.7685x^2-1658 works -62 to -104, then linear 320 beyond.
    #   At -104: quad 17470, linear 17162. Crossover ~-100.
    #   Use quad 1.7685x^2-1658 for -21.4 to -100, linear 320|x|-16116 for |x|>100.
    #   But near floor (-21.4 to -30) quad 1.7685 gives: -24: 1.7685*576-1658=1018.7-1658=-639. Way below floor!
    #   So need different quad near floor. Use 1.327x^2-629 for -21.4 to -40, then 1.7685x^2-1658 for -40 to -100.
    #   At -40: 1.327*1600-629=2123-629=1494; 1.7685*1600-1658=2829.6-1658=1171.6. Mismatch.
    #   Hmm. Let me just use 1.327x^2-629 for -21.4 to -50, then blend to 1.7685x^2-1658.
    #   Actually simpler: use 1.327x^2-629 up to -50, then 1.7685x^2-1658 for -50 to -100, then linear.
    #   At -50: 1.327*2500-629=3317.5-629=2688.5; 1.7685*2500-1658=4421.25-1658=2763.25. Close.
    #   At -62.7: 1.7685*3931-1658=6952-1658=5294 ✓
    #   Good.
    # - Positive side large x>=90: linear 430.95x-16155.6 [E12]
    #   Check E9 126.1: 430.95*126.1-16155.6=54343-16155.6=38187 ✓ (E9: 38187.3!)
    #   Check E9 111.7: 430.95*111.7-16155.6=48137-16155.6=31981 ✓ (E9: 31981.6!)
    #   Check E3 114: 430.95*114-16155.6=49128-16155.6=32972 ✓ (E3: 32972.8!)
    #   Check E3 102.8: 430.95*102.8-16155.6=44302-16155.6=28146 ✓ (E3: 28146.1!)
    #   Check E3 93.6: 430.95*93.6-16155.6=40337-16155.6=24181 vs 13835.8. Anomaly! Ignore.
    #   Check E9 92.1: 430.95*92.1-16155.6=39690-16155.6=23534 ✓ (E9: 23534.9!)
    #   Check E9 84.5: 430.95*84.5-16155.6=36415-16155.6=20259 ✓ (E9: 20259.7!)
    #   Wait 84.5 < 90 but linear works! Check E12 80: 430.95*80-16155.6=34476-16155.6=18320 ✓ (E12: 18320.4!)
    #   Check E12 70: 430.95*70-16155.6=30166.5-16155.6=14011 vs 14370. Off 2.5%.
    #   Check E12 60: 430.95*60-16155.6=25857-16155.6=9701 vs 10960. Off 11%.
    #   So linear works from ~75 up. Quad 2.3156x^2+41.66x+124.3 at 80: 18277 vs 18320 close.
    #   At 84.5 quad: 2.3156*7140+3520+124=16533+3520+124=20177 vs 20259 close.
    #   At 92.1 quad: 2.3156*8482+3837+124=19641+3837+124=23602 vs 23535 close.
    #   At 100 quad: 23156+4166+124=27446 vs 26939 (off 1.9%)
    #   At 111.7 quad: 2.3156*12477+4654+124=28892+4654+124=33670 vs 31982 (off 5%)
    #   So quad works to ~100, linear beyond. Crossover ~100.
    #   At 100: quad 27446, linear 430.95*100-16155.6=43095-16155.6=26939.4. Linear matches E12!
    #   So linear from 100 up. Quad below 100.
    #   At 95: quad 2.3156*9025+3958+124=20898+3958+124=24980 vs 24784.7 (off 0.8%)
    #   At 96: quad 2.3156*9216+4000+124=21341+4000+124=25465 vs 25215.6 (off 1%)
    #   At 92: quad 2.3156*8464+3833+124=19600+3833+124=23557 vs 23491.8 (off 0.3%)
    #   So quad good to ~96, linear from ~96. Use quad for x<96, linear for x>=96.
    #   At 96: quad 25465, linear 430.95*96-16155.6=41371-16155.6=25215.4. Linear matches E12!
    #   So crossover ~96. Use quad x<96, linear x>=96.
    #   Check 88: quad 2.3156*7744+3666+124=17932+3666+124=21722 vs 21768 ✓
    #   Check 90: quad 22629.7 vs 22629.9 ✓
    # - Positive mid: linear 126x-610 for x in [~4.5,24], quad 2.3156x^2+41.66x+124.3 for [24,96]
    #   At 24: linear 2414, quad 2.3156*576+1000+124=1334+1000+124=2458. Close.
    #   At 30: linear 3170, quad 3458. Quad matches E8/E10 (3458.1). Use quad from 24.
    #   At 20: linear 1910, quad 2.3156*400+833+124=926+833+124=1883. Linear matches E10 (1914.2).
    #   So crossover ~22. Use linear to 22, quad after.
    #   At 22: linear 126*22-610=2162, quad 2.3156*484+916.5+124=1121+916.5+124=2161.5. Match!
    #   Use linear x<22, quad x>=22.
    # - Positive small: floor until ~4.5, then rise. E6: 4.0->-12.9, 4.5->13.2, 4.8->34.3, 5.0->48.4
    #   Linear 126x-610 at 5: 20 vs 48.4. Off. 
    #   Slope from 4.5 to 5: (48.4-13.2)/0.5=70.4. From 5 to 6: (146-48.4)/1=97.6.
    #   From 6 to 7: 126. So slope ramps up. 
    #   Fit: 4.5->13.2, 5->48.4, 6->146, 7->272.1
    #   Use piecewise: 4.5-5: slope 70.4; 5-6: slope 97.6; 6+: slope 126.
    #   Actually 126x-610 at 6: 146 ✓, at 7: 272 ✓. So linear 126x-610 works from 6.
    #   For 4.5-6: interpolate. 4.5->13.2, 6->146: slope 88.5.
    #   f = 13.2 + 88.5*(x-4.5) for 4.5<=x<6
    #   At 5: 13.2+44.25=57.5 vs 48.4 (off 9). Acceptable.
    #   Floor end: 13.2 at 4.5. At 4.0: -12.9. So floor ends ~4.3.
    #   Use floor for x<4.3, then 4.3-6 interpolate, then linear.
    #   At 4.3: floor -20.4. At 4.5: 13.2. Slope (13.2+20.4)/0.2=168. Steep.
    #   Simplify: floor for x<4.3, then 4.3-6: f=-20.4+ (146+20.4)/1.7*(x-4.3)
    #   At 5: -20.4+97.9*0.7=48.1 ✓
    #   At 4.5: -20.4+97.9*0.2=-0.8 vs 13.2 (off). Hmm.
    #   Let me just use: floor x<4.3; 4.3-5: slope 168 from -20.4; 5-6: slope 97.6; 6+: 126x-610
    #   At 5: -20.4+168*0.7=97.2 vs 48.4. No.
    #   OK simpler: floor x<4.5; 4.5-6: f=13.2+88.5*(x-4.5); 6+: 126x-610
    #   At 4.5: 13.2 (E6: 13.2 ✓). At 4.0: floor -20.4 (E6: -12.9, off 7.5).
    #   Acceptable. Use this.
    
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
            continue
        ax = abs(x)
        if x < 0:
            if ax < 21.4:
                v = -20.4469
            elif ax < 50:
                v = 1.327 * x * x - 629.0
            elif ax < 100:
                v = 1.7685 * x * x - 1658.0
            else:
                v = 320.0 * ax - 16116.0
            out.append(max(-20.4469, v))
        else:
            if x < 4.5:
                v = -20.4469
            elif x < 6.0:
                v = 13.2 + 88.5 * (x - 4.5)
            elif x < 22.0:
                v = 126.0 * x - 610.0
            elif x < 96.0:
                v = 2.3156 * x * x + 41.66 * x + 124.3
            else:
                v = 430.95 * x - 16155.6
            out.append(v)
    return {"y": out}
