import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Main mechanism: for most x, f(x) = x^3 + 2*x - 50 (approximately).
    #   Check: f(0) = -48.6 ~ -50? Actually E10 gives f(0) = -48.6, so constant ~ -48.6.
    #   Let's fit: x^3 + 2x + c. At x=0 -> c = -48.6. At x=1: 1+2-48.6 = -45.6, E2 gives -46.6.
    #   Hmm. Try x^3 + 2x - 49.6? x=1 -> -46.6 matches E2. x=0 -> -49.6, but E10 says -48.6.
    #   Try x^3 + x - 48.6: x=1 -> -46.6 ok, x=0 -> -48.6 ok. x=2 -> 8+2-48.6=-38.6 but E2 says -32.2.
    #   Try x^3 + 2x - 48.6: x=1 -> -45.6 (E2 says -46.6). Off by 1.
    #   Let's derive from data: x=2 -> -32.2, x=3 -> 2.4, x=5 -> 163.4.
    #   x^3 = 8, 27, 125. Differences: -32.2-8=-40.2; 2.4-27=-24.6; 163.4-125=38.4.
    #   Not linear. Try cubic with all terms: fit a*x^3+b*x+c.
    #   x=2: 8a+2b+c=-32.2
    #   x=3: 27a+3b+c=2.4
    #   x=5: 125a+5b+c=163.4
    #   Subtract: 19a+b=34.6; 98a+2b=161.0 -> 49a+b=80.5. So 30a=45.9 -> a=1.53.
    #   b=34.6-19*1.53=34.6-29.07=5.53. c=-32.2-8*1.53-2*5.53=-32.2-12.24-11.06=-55.5.
    #   Check x=10: 1530+55.3-55.5=1529.8, E2 says 1465.4. Not exact.
    #
    # Actually many outputs look like x^3 + something. Check x=100: 1e6, E2 gives 7772.97 (in the special region).
    # x=90: 729000, E4 gives 966137.4. x=80: 512000, E4 gives 680143.4.
    # Differences: 966137.4-729000=237137.4; 680143.4-512000=168143.4.
    # For x^3+2x-48.6: x=80 -> 512000+160-48.6=512111.4, not 680143.4.
    # Hmm, maybe f(x) = x^3 + 2x - 48.6 doesn't match large.
    # x=80: 680143.4. 680143.4 - 512000 = 168143.4. That's about 2*80^2 + ...? 2*6400=12800 no.
    # Let's check x=60: 216000, E4 gives 288935.4. Diff = 72935.4.
    # x=40: 64000, E4 gives 86767.4. Diff = 22767.4.
    # x=30: 27000, E4 gives 37073.4. Diff=10073.4.
    # x=25: 15625, E4 gives 21661.4. Diff=6036.4.
    # x=20: 8000, E2 gives 11239.4. Diff=3239.4.
    # x=15: 3375, E4 gives 4832.4. Diff=1457.4.
    # x=12: 1728, E4 gives 2509.8. Diff=781.8.
    # x=10: 1000, E2 gives 1465.4. Diff=465.4.
    # x=8: 512, E2 gives 751.4. Diff=239.4.
    # x=6: 216, E4 gives 305.4. Diff=89.4.
    # x=5: 125, E2 gives 163.4. Diff=38.4.
    # x=4: 64, E2 gives 65.0. Diff=1.0.
    # x=3: 27, E2 gives 2.4. Diff=-24.6.
    # x=2: 8, E2 gives -32.2. Diff=-40.2.
    # x=1: 1, E2 gives -46.6. Diff=-47.6.
    # Diff sequence: -47.6, -40.2, -24.6, 1.0, 38.4, 89.4, 239.4, 465.4, 781.8, 1457.4, 3239.4, 6036.4, 10073.4, 22767.4, 72935.4, 168143.4
    # Differences of diff: 7.4, 15.6, 25.6, 37.4, 51, 150, 226, 316.4, 675.6, 1782, 2797, 4037, 12694, 50168, 95208.
    # Looks like diff ~ 2x^2? x=20: 800, actual 3239. No.
    # Try diff = 2x^2 - 50? x=20: 800-50=750 no.
    # Try f(x) = x^3 + 2x^2 - 48.6? x=20: 8000+800-48.6=8751.4 no.
    # Try f(x)= x^3 + 2x - 48.6 + something.
    # Actually check f(x) = x^3 + 2x - 48.6 for x=100: 1000000+200-48.6=1000151.4, but E2 gives 7772.97 (special region).
    # Check x=95: 857375+190-48.6=857516.4, E6 gives 1135144.4. Off.
    # Hmm. Let's look at x=90: 729000, E4 gives 966137.4. 966137.4/729000=1.325.
    # x=80: 680143.4/512000=1.328.
    # x=60: 288935.4/216000=1.337.
    # x=40: 86767.4/64000=1.356.
    # x=30: 37073.4/27000=1.373.
    # x=25: 21661.4/15625=1.386.
    # x=20: 11239.4/8000=1.405.
    # x=15: 4832.4/3375=1.432.
    # x=12: 2509.8/1728=1.452.
    # x=10: 1465.4/1000=1.465.
    # x=8: 751.4/512=1.468.
    # x=6: 305.4/216=1.414.
    # x=5: 163.4/125=1.307.
    # x=4: 65/64=1.016.
    # Hmm ratio ~1.3-1.4 for large. 
    # Try f(x)= a*x^3 + b*x^2 + c*x + d.
    # Use x=80,60,40,20.
    # 512000a+6400b+80c+d=680143.4
    # 216000a+3600b+60c+d=288935.4
    # 64000a+1600b+40c+d=86767.4
    # 8000a+400b+20c+d=11239.4
    # Subtract: 296000a+2800b+20c=391208
    # 152000a+2000b+20c=202168
    # 56000a+1200b+20c=75528
    # Subtract: 144000a+800b=189040 -> 180a+b=236.3
    # 96000a+800b=126640 -> 120a+b=158.3
    # 60a=78 -> a=1.3. b=236.3-180*1.3=236.3-234=2.3.
    # 56000*1.3+1200*2.3+20c=75528 -> 72800+2760+20c=75528 -> 20c=-32 -> c=-1.6.
    # d=11239.4-8000*1.3-400*2.3-20*(-1.6)=11239.4-10400-920+32=-48.6.
    # So f(x)=1.3x^3+2.3x^2-1.6x-48.6 for large x? Check x=10: 1300+230-16-48.6=1465.4. Matches E2!
    # Check x=5: 162.5+57.5-8-48.6=163.4. Matches!
    # Check x=3: 35.1+20.7-4.8-48.6=2.4. Matches!
    # Check x=1: 1.3+2.3-1.6-48.6=-46.6. Matches E2!
    # Check x=0: -48.6. Matches E10!
    # Check x=-1: -1.3+2.3+1.6-48.6=-46.0. Matches E2!
    # Check x=-2: -10.4+9.2+3.2-48.6=-46.6. Matches E2!
    # Check x=-10: -1300+230+16-48.6=-1102.6. Matches E2!
    # Check x=-20: -10400+920+32-48.6=-9496.6. Matches E2!
    # Check x=-100: -1300000+23000+160-48.6=-1276888.6. Matches E2!
    # Check x=-128: -1300000*1.28... let's compute: 1.3*(-128)^3 = 1.3*(-2097152)=-2726297.6; 2.3*16384=37683.2; -1.6*(-128)=204.8; -48.6. Sum=-2726297.6+37683.2+204.8-48.6=-2688458.2. Matches E10!
    #
    # So base formula: f(x) = 1.3*x^3 + 2.3*x^2 - 1.6*x - 48.6
    #
    # Special region: around x in [97.6, 117.5] (approx), f(x) ~ 7773 (constant-ish, noisy).
    # From E12: x=97.6 -> 7772.8954, x=97.65 -> 7773.0225... so boundary between 97.55 and 97.6.
    # E14: 97.55 -> 7773.0156 (special), 97.6 -> 7772.8954 (special). 97.5 -> 7772.9333 (special). 
    # E8: 97.5 -> 1226576.9625 (normal!), 98 -> 7772.8742 (special). So boundary between 97.5 and 97.55.
    # E12: 97.6 special. So boundary ~97.5-97.6. Let's say x > 97.5 enters special.
    # Actually E8: 97.5 -> normal. E12: 97.6 -> special. So boundary in (97.5, 97.6].
    # E14: 97.55 -> special. So boundary in (97.5, 97.55].
    # Upper boundary: E12: 117.6 -> 2145865.3968 (normal). 117.4 -> 7772.9333 (special).
    # E14: 117.5 -> 7772.9333 (special), 117.55 -> 7773.0815 (special), 117.6 -> 2145865.3968 (normal).
    # E8: 117.5 -> 7773.0521 (special), 118 -> 2167729.4 (normal).
    # So special region: 97.5 < x < 117.6 (approx). Let's say 97.5 < x < 117.6.
    # Actually E12: 117.4 special, 117.6 normal. E14: 117.55 special, 117.6 normal. So boundary in (117.55, 117.6].
    # Let's use 97.5 < x < 117.6.
    #
    # Inside special region: f(x) ~ 7773 with small noise. Values range 7772.76 to 7773.10.
    # Mean ~ 7772.93. Use 7772.93 as prediction. Noise is small.
    # Actually maybe it's a constant 7773 plus noise. Let's use 7773.0.
    # But E6: x=100 -> 7773.0054, x=105 -> 7772.8653, etc. Mean ~7772.93.
    # Let's use 7772.93.

    x = probe["x"]
    result = []
    for xi in x:
        if xi is None:
            result.append(None)
            continue
        if 97.5 < xi < 117.6:
            # Special region: near-constant noisy value
            result.append(7772.93)
        else:
            # Base cubic formula
            y = 1.3 * xi**3 + 2.3 * xi**2 - 1.6 * xi - 48.6
            result.append(y)
    return {"y": result}
