def predict(probe):
    # Observations from E1:
    # x=88.2 -> -838.72 ; x=66.0 -> -625.6 ; x=72.7 -> -689.92
    #   These look like y = -9.5*x roughly? 88.2*-9.5=-837.9 ✓ ; 66*-9.5=-627 ~ ; 72.7*-9.5=-690.65 ~
    #   More precisely: -838.72/88.2 = -9.509 ; -625.6/66 = -9.479 ; -689.92/72.7 = -9.490
    #   Hmm, maybe y = -9.5*x with small noise, or y = -(x*9.5)? Let's check others.
    # x=-20.3 -> 7.9802 ; x=-61.7 -> 7.9672 ; x=-24.3 -> 7.8563 ; x=-50.4 -> 8.3275
    #   These are all ~8, not linear. So there's a region where output ~8.
    # x=2.9 -> -19.84 ; x=-6.0 -> 65.6 ; x=21.3 -> -196.48
    #   -19.84/2.9 = -6.84 ; 65.6/-6 = -10.93 ; -196.48/21.3 = -9.22
    #   Not consistent. Maybe quadratic? 2.9^2=8.41, *-2.36=-19.84. -6^2=36, *1.82=65.6. 21.3^2=453.7, *-0.433=-196.5. No.
    # Let's look at x=-20.3, -61.7, -24.3, -50.4 all give ~8. That's a flat region.
    #   Range roughly -61.7 to -20.3 gives ~8. Maybe region [-64,-16]? 
    # x=-6 gives 65.6, x=2.9 gives -19.84, x=21.3 gives -196.48.
    #   Try y = -9.5*x + c? For x=2.9: -27.55+c=-19.84 -> c=7.71. x=-6: 57+c=65.6 -> c=8.6. x=21.3: -202.35+c=-196.48 -> c=5.87. Not constant.
    #   Try y = -9.5*x + 8? x=2.9: -27.55+8=-19.55 (obs -19.84, close). x=-6: 57+8=65 (obs 65.6, close). x=21.3: -202.35+8=-194.35 (obs -196.48, off by 2).
    #   Try y = -9.5*x + 8 with noise? For large x: 88.2: -837.9+8=-829.9 vs -838.72 (off 8.8). 66: -627+8=-619 vs -625.6 (off 6.6). 72.7: -690.65+8=-682.65 vs -689.92 (off 7.3).
    #   Hmm, for large positive x, y ≈ -9.5*x - 8? 88.2: -837.9-8=-845.9 vs -838.72. No.
    #   Let's fit large x: slope between 66 and 88.2: (-838.72+625.6)/(88.2-66) = -213.12/22.2 = -9.6. 
    #   Between 66 and 72.7: (-689.92+625.6)/6.7 = -64.32/6.7 = -9.6.
    #   So slope -9.6 for large x. Intercept: -625.6 - (-9.6*66) = -625.6+633.6 = 8. So y = -9.6*x + 8 for large x.
    #   Check 88.2: -9.6*88.2+8 = -846.72+8 = -838.72 ✓ EXACT!
    #   Check 72.7: -9.6*72.7+8 = -697.92+8 = -689.92 ✓ EXACT!
    #   Check 66: -9.6*66+8 = -633.6+8 = -625.6 ✓ EXACT!
    #   So for large x: y = -9.6*x + 8.
    # Now small x: x=2.9: -9.6*2.9+8 = -27.84+8 = -19.84 ✓ EXACT!
    #   x=-6: -9.6*-6+8 = 57.6+8 = 65.6 ✓ EXACT!
    #   x=21.3: -9.6*21.3+8 = -204.48+8 = -196.48 ✓ EXACT!
    #   So y = -9.6*x + 8 works for all except the flat region!
    # Flat region: x=-20.3: -9.6*-20.3+8 = 194.88+8 = 202.88, but obs 7.9802. So flat region overrides.
    #   x=-61.7: -9.6*-61.7+8 = 592.32+8 = 600.32, obs 7.9672. Flat.
    #   x=-24.3: -9.6*-24.3+8 = 233.28+8 = 241.28, obs 7.8563. Flat.
    #   x=-50.4: -9.6*-50.4+8 = 483.84+8 = 491.84, obs 8.3275. Flat.
    #   Flat values: 7.9802, 7.9672, 7.8563, 8.3275. Around 8, noisy. Maybe y = 8 + noise? Or a function of x?
    #   Let's see if flat value depends on x: -20.3->7.9802, -24.3->7.8563, -50.4->8.3275, -61.7->7.9672.
    #   Not monotonic. Could be 8 + small noise. Or maybe sin? Let's guess ~8 with noise.
    #   Actually maybe it's 8 + something small. Range 7.8563 to 8.3275. Center ~8.09. Hmm.
    #   Could be 8 + 0.1*sin(x)? -20.3: sin=-0.99 -> 7.9. -24.3: sin=-0.63 -> 7.94. -50.4: sin=0.77 -> 8.08. -61.7: sin=0.88 -> 8.09. Not quite.
    #   Let's just use 8 as approximation, or maybe the flat region is exactly 8 with noise.
    #   Actually the values: 7.9802, 7.9672, 7.8563, 8.3275. Mean = 8.0328. Could be 8 + noise.
    #   Let's check if it's 8 + 0.5*sin(x/10)? -20.3: sin(-2.03)=-0.896 -> 7.55. No.
    #   Maybe it's 8 + 0.5*cos(x)? -20.3: cos(-20.3)=0.36 -> 8.18. -24.3: cos=0.86 -> 8.43. -50.4: cos=0.44 -> 8.22. -61.7: cos=-0.32 -> 7.84. Close-ish but not exact.
    #   Let's try 8 + 0.4*sin(x/5): -20.3: sin(-4.06)=0.79 -> 8.32. -24.3: sin(-4.86)=0.99 -> 8.4. -50.4: sin(-10.08)=-0.61 -> 7.76. -61.7: sin(-12.34)=-0.23 -> 7.91. Not matching.
    #   Given noise, just use 8.0.
    # Boundaries of flat region: need to determine. We have flat at -61.7, -50.4, -24.3, -20.3.
    #   Non-flat at -6 (65.6 = -9.6*-6+8 ✓). So boundary between -20.3 and -6.
    #   Non-flat at 2.9. So flat region ends somewhere in (-20.3, -6).
    #   Upper end: -20.3 flat, -6 not flat. Could be -16? Let's guess boundary at -16.
    #   Lower end: -61.7 flat. Need to know if -64 or -128 etc. No data below -61.7. 
    #   Maybe region is [-64, -16]? Or [-128, -16]? Unknown. Let's guess [-64, -16] based on typical patterns.
    #   Actually could be symmetric or based on some threshold. Let's guess [-64, -16].
    #   Hmm, but -61.7 is flat, so lower bound <= -61.7. Could be -64.
    #   Let's use [-64, -16] as guess, mark with ?.
    # Also need to check: is there noise elsewhere? The linear fits were EXACT, so no noise outside flat region.
    #   Flat region values are noisy (not exact 8). So flat region has noise.
    #   Maybe flat region is 8 + noise (uniform or gaussian). We'll predict 8.
    # Actually wait, let me reconsider: maybe flat region is a different function. 
    #   Values: 7.9802, 7.9672, 7.8563, 8.3275. 
    #   Differences from 8: -0.0198, -0.0328, -0.1437, +0.3275.
    #   Could be 8 + 0.3*sin(x)? -20.3: sin=-0.99 -> 7.7. No.
    #   Could be 8 + 0.3*cos(x/3)? -20.3: cos(-6.77)=0.88 -> 8.26. -24.3: cos(-8.1)=-0.16 -> 7.95. -50.4: cos(-16.8)=-0.79 -> 7.76. -61.7: cos(-20.57)=0.55 -> 8.16. No.
    #   Just use 8.
    # Let me reconsider boundaries. Maybe the flat region is where x is negative and |x| large? 
    #   -20.3 flat, -24.3 flat, -50.4 flat, -61.7 flat. -6 not flat.
    #   So maybe x <= -16 or so. And maybe x >= -64? Unknown.
    #   Could be x in [-64, -16]. Let's go with that.
    # Actually, maybe it's simpler: the flat region might be [-64, -16] or maybe [-100, -16]. 
    #   Without data, guess [-64, -16].
    # Let me also consider: maybe flat region is exactly where -9.6*x+8 would be large? 
    #   At x=-16: -9.6*-16+8 = 153.6+8 = 161.6. At x=-64: 614.4+8=622.4.
    #   Maybe the function clamps to 8 when the linear value exceeds some threshold? 
    #   If linear value > 150, output 8? At x=-20.3: linear=202.88 > 150 -> 8 ✓. At x=-6: linear=65.6 < 150 -> 65.6 ✓.
    #   Threshold between 65.6 and 202.88. Could be 100? 150? 200?
    #   At x=-16: linear=161.6. If threshold is 150, then -16 would be flat. 
    #   At x=-14: linear=142.4 < 150 -> not flat.
    #   Hmm, this is a plausible mechanism: if -9.6*x+8 > threshold, output 8.
    #   But then for very negative x, linear is huge, output 8. That matches.
    #   What threshold? Between 65.6 (x=-6) and 202.88 (x=-20.3). 
    #   Could be 100? Then x where -9.6x+8=100 -> x=-9.58. So flat for x < -9.58.
    #   But -20.3 flat, -6 not flat. -9.58 is between. Plausible.
    #   Could be 128? x=-12.5. Could be 150? x=-14.79.
    #   Hmm. Let's think about what's natural. Maybe the function is:
    #   y = -9.6*x + 8 if -9.6*x+8 <= 8? No, that doesn't work.
    #   Actually maybe the flat region is when x is in some range like [-64,-16].
    #   Let me just go with region [-64, -16] -> 8, else -9.6*x+8.
    #   But wait, what about x < -64? If region is [-64,-16], then x=-100 would be -9.6*-100+8 = 968. 
    #   Is that plausible? Unknown. 
    #   Alternatively, maybe flat region is x <= -16 (all the way to -128). 
    #   Then x=-100 -> 8. 
    #   Which is more likely? The problem says "There may be an interval inside the domain where the function behaves differently". 
    #   "Interval inside the domain" suggests a bounded interval, not extending to -128.
    #   So [-64, -16] is a bounded interval. Let's go with that.
    #   But -61.7 is flat, so lower bound <= -61.7. Could be -64.
    #   Let's use [-64, -16].
    # Hmm, but actually let me reconsider. Maybe the flat region is [-64, -16] and value is 8.
    #   Or maybe the region is where x is in [-64, -16] and output is 8 + noise.
    #   I'll predict 8.
    # Let me also double check: is there any chance the flat region value is a function of x?
    #   -20.3 -> 7.9802
    #   -24.3 -> 7.8563
    #   -50.4 -> 8.3275
    #   -61.7 -> 7.9672
    #   If it were 8 + 0.1*sin(x), -20.3: sin=-0.99 -> 7.9. -24.3: sin=-0.63 -> 7.94. -50.4: sin=0.77 -> 8.08. -61.7: sin=0.88 -> 8.09. Not matching.
    #   If 8 + 0.2*cos(x/2): -20.3: cos(-10.15)=-0.72 -> 7.86. -24.3: cos(-12.15)=0.94 -> 8.19. -50.4: cos(-25.2)=0.99 -> 8.2. -61.7: cos(-30.85)=0.99 -> 8.2. No.
    #   Just use 8.
    # Actually, let me reconsider the whole thing. Maybe it's not -9.6*x+8.
    #   Let me re-verify: 88.2*-9.6 = -846.72, +8 = -838.72 ✓
    #   66*-9.6 = -633.6, +8 = -625.6 ✓
    #   72.7*-9.6 = -697.92, +8 = -689.92 ✓
    #   2.9*-9.6 = -27.84, +8 = -19.84 ✓
    #   -6*-9.6 = 57.6, +8 = 65.6 ✓
    #   21.3*-9.6 = -204.48, +8 = -196.48 ✓
    #   All exact. So linear part is definitely -9.6*x+8.
    # Flat region: -20.3, -24.3, -50.4, -61.7 all give ~8.
    #   So flat region is somewhere around there.
    #   Boundary between -20.3 and -6. Could be -16 (nice round). 
    #   Lower boundary: unknown, but -61.7 is flat. Could be -64 (nice round).
    #   Let's use [-64, -16].
    # Actually, maybe the region is [-64, -16] or maybe [-100, -16]. 
    #   I'll go with [-64, -16] and mark with ?.
    # Wait, could the flat region be where x is in [-64, -16]? Or maybe it's [-64, -16] with value 8.
    #   Let me also consider: maybe the flat region is [-64, -16] and the value is 8 + noise.
    #   I'll predict 8.
    # Let me write the code.
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if -64 <= x <= -16:
                ys.append(8.0)  # ? flat region, noisy around 8
            else:
                ys.append(-9.6 * x + 8.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
