def predict(probe):
    # Observations:
    # - For x>0: y is negative and grows in magnitude roughly like -x^3 (E2: x=128 -> -51892, x=100 -> -40574, x=80 -> -32490)
    #   Check ratios: 51892/128^3=0.0247; 40574/100^3=0.0406; 32490/80^3=0.0635. Not pure cubic.
    #   Try -x^2: 51892/16384=3.17; 40574/10000=4.06; 32490/6400=5.08. Not pure quadratic.
    #   Try -x^2.5: 128^2.5=185363 -> 0.28; 100^2.5=100000 -> 0.41; 80^2.5=57243 -> 0.57. Hmm.
    # - For x<0: y is positive and grows like |x|^2 roughly (E2: x=-128 -> 4555, x=-100 -> 3555, x=-80 -> 2840)
    #   4555/16384=0.278; 3555/10000=0.355; 2840/6400=0.444. Not pure quadratic.
    # - At x=0: y=-5401.17 (big negative jump!)
    # - Near x=0+: x=1 -> -559, x=3 -> -1367, x=5 -> -2176, x=10 -> -4197
    #   These look like -5401 + something. x=1: -559 = -5401+4842; x=3: -1367=-5401+4034; x=5:-2176=-5401+3225
    #   Differences: 4842, 4034, 3225 for x=1,3,5. Hmm not linear.
    # - Near x=0-: x=-1 -> 18.62, x=-3 -> 90.06, x=-5 -> 161.5, x=-10 -> 340.1
    #   These look like ~ -18.62*x? x=-1:18.62; x=-3:55.86 (actual 90.06); not linear.
    #   Try x^2: 1->18.62, 9->90.06 (ratio 10), 25->161.5 (ratio 6.46), 100->340.1 (ratio 3.4). Not quadratic.
    #   Try |x|^1.5: 1->18.62, 5.196->90.06 (17.3), 11.18->161.5 (14.4), 31.6->340.1 (10.8). Hmm.
    #   Try |x|^1.2: 1->18.62, 3.7->90.06 (24.3), 6.9->161.5 (23.4), 15.8->340.1 (21.5). Closer!
    #   Try |x|^1.1: 1->18.62, 3.35->90.06 (26.9), 5.87->161.5 (27.5), 12.6->340.1 (27). Very close!
    #   So for x<0 small: y ≈ 27*|x|^1.1? Check x=-1: 27*1=27 (actual 18.62). Hmm.
    #   Try y = a*|x|^b: log(18.62)=2.924, log(90.06)=4.500, log(161.5)=5.085, log(340.1)=5.829
    #   log|x|: 0, 1.099, 1.609, 2.303
    #   Slope between first two: (4.5-2.924)/1.099=1.434; next: (5.085-4.5)/0.510=1.147; next: (5.829-5.085)/0.694=1.072
    #   Not constant. Maybe y = a*|x| + b*|x|^2? 
    #   Let's try y = a*|x|^2 + b*|x|: x=-1: a+b=18.62; x=-3: 9a+3b=90.06; x=-5: 25a+5b=161.5
    #   From first: b=18.62-a. 9a+3(18.62-a)=90.06 -> 6a+55.86=90.06 -> a=5.7, b=12.92
    #   Check x=-5: 25*5.7+5*12.92=142.5+64.6=207.1 (actual 161.5). Not great.
    # - For x>0 small: x=1:-559, x=3:-1367, x=5:-2176, x=10:-4197
    #   Differences from -5401: 4842, 4034, 3225, 1204
    #   Hmm, maybe y = -5401 + a*x^b? log(4842)=8.485, log(4034)=8.303, log(3225)=8.079, log(1204)=7.093
    #   log x: 0, 1.099, 1.609, 2.303
    #   Slope: (8.303-8.485)/1.099=-0.166; (8.079-8.303)/0.510=-0.439; (7.093-8.079)/0.694=-1.42. Not power.
    #   Maybe y = -5401 + a*x + b*x^2? x=1: a+b=4842; x=3: 3a+9b=4034; x=5: 5a+25b=3225
    #   From first: a=4842-b. 3(4842-b)+9b=4034 -> 14526+6b=4034 -> b=-1748.7, a=6590.7
    #   Check x=5: 5*6590.7+25*(-1748.7)=32953.5-43717.5=-10764 (actual 3225). No.
    # - For x>0 large: x=30:-12280, x=40:-16322, x=50:-20364, x=80:-32490, x=100:-40574, x=128:-51892
    #   Differences: -4042, -4042, -12126 (for 30 more), -8084 (for 20 more), -11318 (for 28 more)
    #   Per unit: 30->40: -404.2; 40->50: -404.2; 50->80: -404.2; 80->100: -404.2; 100->128: -404.2
    #   LINEAR! y = -404.2*x + c. At x=30: -12280 = -12126+c -> c=-154. 
    #   Check x=128: -404.2*128-154 = -51737.6-154 = -51891.6 ✓ (actual -51892.4)
    #   Check x=100: -40420-154=-40574 ✓
    #   Check x=80: -32336-154=-32490 ✓
    #   So for x>=30 (or maybe x>some threshold): y = -404.2*x - 154
    #   Check x=10: -4042-154=-4196 ✓ (actual -4196.8)!
    #   Check x=5: -2021-154=-2175 ✓ (actual -2175.8)!
    #   Check x=3: -1212.6-154=-1366.6 ✓ (actual -1367.4)!
    #   Check x=1: -404.2-154=-558.2 ✓ (actual -559)!
    #   Check x=0: -154 (actual -5401.17). ✗ So x=0 is special.
    #   So for x>0: y = -404.2*x - 154. But at x=0 it's -5401.17.
    #   Wait, maybe x=0 is a discontinuity. Let's check x=-1: 404.2-154=250.2 (actual 18.62). No.
    # - For x<0 large: x=-30:1054.5, x=-40:1411.7, x=-80:2840.5, x=-100:3554.9, x=-128:4555.06
    #   Differences: 357.2 (10 units), 1428.8 (40 units), 714.4 (20 units), 1000.16 (28 units)
    #   Per unit: 35.72, 35.72, 35.72, 35.72. LINEAR!
    #   y = 35.72*|x| + c. At x=-30: 1071.6+c=1054.5 -> c=-17.1
    #   Check x=-128: 4572.16-17.1=4555.06 ✓
    #   Check x=-100: 3572-17.1=3554.9 ✓
    #   Check x=-80: 2857.6-17.1=2840.5 ✓
    #   Check x=-40: 1428.8-17.1=1411.7 ✓
    #   Check x=-10: 357.2-17.1=340.1 ✓
    #   Check x=-5: 178.6-17.1=161.5 ✓
    #   Check x=-3: 107.16-17.1=90.06 ✓
    #   Check x=-1: 35.72-17.1=18.62 ✓
    #   So for x<0: y = 35.72*|x| - 17.1 = -35.72*x - 17.1
    #   Check x=0: -17.1 (actual -5401.17). ✗
    # So the function is piecewise linear:
    #   x < 0: y = -35.72*x - 17.1
    #   x > 0: y = -404.2*x - 154
    #   x = 0: y = -5401.17 (special value, or maybe there's a tiny interval)
    # Let's verify with E1 data:
    # x=88.2: -404.2*88.2-154 = -35650.44-154 = -35804.44 (actual -35805.24) ✓ close
    # x=66: -404.2*66-154 = -26677.2-154 = -26831.2 (actual -26832) ✓
    # x=-20.3: -35.72*(-20.3)-17.1 = 725.116-17.1 = 708.016 ✓ exact!
    # x=-61.7: -35.72*(-61.7)-17.1 = 2203.924-17.1 = 2186.824 ✓ exact!
    # x=2.9: -404.2*2.9-154 = -1172.18-154 = -1326.18 (actual -1326.98) ✓ close
    # x=-24.3: -35.72*(-24.3)-17.1 = 868.0-17.1 = 850.9 ✓
    # x=72.7: -404.2*72.7-154 = -29385.34-154 = -29539.34 (actual -29540.14) ✓
    # x=-50.4: -35.72*(-50.4)-17.1 = 1800.288-17.1 = 1783.188 ✓ exact!
    # x=-6: -35.72*(-6)-17.1 = 214.32-17.1 = 197.22 ✓ exact!
    # x=21.3: -404.2*21.3-154 = -8609.46-154 = -8763.46 (actual -8764.26) ✓
    # Excellent! The small discrepancies (~0.8) suggest slightly different constants. Let me refine.
    # For x>0: from x=1:-559 and x=128:-51892.4: slope = (-51892.4+559)/127 = -404.2. 
    #   intercept: -559 = -404.2*1 + c -> c = -154.8
    #   Check x=128: -404.2*128-154.8 = -51737.6-154.8 = -51892.4 ✓
    #   Check x=88.2: -404.2*88.2-154.8 = -35650.44-154.8 = -35805.24 ✓ EXACT!
    #   Check x=66: -404.2*66-154.8 = -26677.2-154.8 = -26832 ✓ EXACT!
    #   Check x=2.9: -404.2*2.9-154.8 = -1172.18-154.8 = -1326.98 ✓ EXACT!
    #   Check x=21.3: -404.2*21.3-154.8 = -8609.46-154.8 = -8764.26 ✓ EXACT!
    #   Check x=72.7: -404.2*72.7-154.8 = -29385.34-154.8 = -29540.14 ✓ EXACT!
    # For x<0: from x=-1:18.62 and x=-128:4555.06: slope = (4555.06-18.62)/127 = 35.72
    #   intercept: 18.62 = 35.72*1 + c -> c = -17.1
    #   Check x=-20.3: 35.72*20.3-17.1 = 725.116-17.1 = 708.016 ✓ EXACT!
    #   Check x=-61.7: 35.72*61.7-17.1 = 2203.924-17.1 = 2186.824 ✓ EXACT!
    #   Check x=-50.4: 35.72*50.4-17.1 = 1800.288-17.1 = 1783.188 ✓ EXACT!
    #   Check x=-6: 35.72*6-17.1 = 214.32-17.1 = 197.22 ✓ EXACT!
    #   Check x=-24.3: 35.72*24.3-17.1 = 868.0-17.1 = 850.9 ✓ EXACT!
    # So the model is:
    #   x < 0: y = 35.72*|x| - 17.1
    #   x > 0: y = -404.2*x - 154.8
    #   x = 0: y = -5401.17 (special)
    # What about x=0? Maybe there's a tiny interval around 0 where it's different, or maybe just x=0.
    # Given the data, I'll treat x=0 as special. But maybe the "special interval" is very narrow.
    # Actually, maybe the function is: y = a*x + b for x<0, y = c*x + d for x>0, and at x=0 it's a spike.
    # Or maybe the interval is [-epsilon, epsilon] where it's -5401.17. Without more data, I'll assume just x=0.
    # Actually, let's reconsider: maybe the "different interval" is a narrow band around 0. 
    # But we only have x=0 as evidence. I'll treat x=0 as special.
    # Wait - could it be that the function has a discontinuity at 0, and the value at 0 is -5401.17?
    # Or could the interval be something like [-0.5, 0.5]? We don't have data. I'll say x==0 special.
    
    def f(x):
        if x < 0:
            return 35.72 * (-x) - 17.1
        elif x > 0:
            return -404.2 * x - 154.8
        else:
            return -5401.17
    return {"y": [f(x) for x in probe["x"]]}
