import math

def predict(probe):
    # Beliefs:
    # 1. For x in the "outer" region (x < -9.4 or x > -9.4? Actually the transition is near -9.4), 
    #    the function is linear: y = 8.0 * x - 0? Let's check: at x=0, y=8.0; at x=1, y=-1.6? Wait E14: x=0 -> 8.0, x=1 -> -1.6, x=2 -> -11.2, x=3 -> -20.8, x=4 -> -30.4, x=5 -> -40.0. 
    #    That's y = 8.0 - 9.6*x? Check x=0: 8.0; x=1: -1.6; x=2: -11.2; x=3: -20.8; x=4: -30.4; x=5: -40.0. Yes y = 8.0 - 9.6*x.
    #    Check x=-1: 8.0 + 9.6 = 17.6 (E14: -1 -> 17.6). x=-2: 8+19.2=27.2 (E14: -2 -> 27.2). x=-3: 8+28.8=36.8 (E14: -3 -> 36.8). x=-4: 46.4 (E14: -4 -> 46.4). x=-5: 56.0 (E14: -5 -> 56.0). x=-6: 65.6 (E14: -6 -> 65.6). x=-7: 75.2 (E14: -7 -> 75.2). x=-8: 84.8 (E14: -8 -> 84.8). x=-9: 94.4 (E14: -9 -> 94.4). 
    #    So for x <= -9 (or maybe x < -9.4?), y = 8.0 - 9.6*x? Wait at x=-9, 8 - 9.6*(-9) = 8 + 86.4 = 94.4. Yes.
    #    But at x=-9.5, E4 gives 7.9742 (noise around 8). So there's a transition between -9.5 and -9.4.
    #    E18: x=-9.45 -> 7.9233 (noise ~8), x=-9.44 -> 8.095, x=-9.43 -> 8.0563, x=-9.42 -> 7.986, x=-9.415 -> 7.9759, x=-9.41 -> 8.0875, x=-9.405 -> 8.1443, x=-9.402 -> 7.8695, x=-9.401 -> 7.9539, x=-9.4 -> 8.0089, x=-9.399 -> 98.2304, x=-9.398 -> 98.2208, x=-9.395 -> 98.192, x=-9.39 -> 98.144...
    #    So the transition is exactly at x = -9.4. For x > -9.4 (i.e., x >= -9.399?), the linear formula y = 8.0 - 9.6*x applies. At x=-9.399: 8 - 9.6*(-9.399) = 8 + 90.2304 = 98.2304. Yes matches.
    #    For x < -9.4 (i.e., x <= -9.45? Actually E18 x=-9.45 gives 7.9233, x=-9.44 gives 8.095, x=-9.43 gives 8.0563, x=-9.42 gives 7.986, x=-9.415 gives 7.9759, x=-9.41 gives 8.0875, x=-9.405 gives 8.1443, x=-9.402 gives 7.8695, x=-9.401 gives 7.9539, x=-9.4 gives 8.0089. All these are around 8 with noise. So for x < -9.4, y is approximately 8 with noise (looks like random noise around 8, maybe uniform or normal). 
    #    Check E8: x=-9.45 -> 8.0895, -9.42 -> 8.0946, -9.4 -> 8.1987 (noise), -9.38 -> 98.048 (linear). So boundary is -9.4.
    #    Check E10: x=-9.5 -> 8.0191, -9.6 -> 7.855, -9.8 -> 8.0442, -10 -> 7.9041, -10.5 -> 7.9622, -12 -> 8.0775, -15 -> 7.9305, -20 -> 8.1241, -30 -> 7.9947, -40 -> 8.1796, -50 -> 8.0914, -60 -> 7.8257, -70 -> 7.9722, -80 -> 8.0326, -90 -> 8.1942, -100 -> 7.9385, -110 -> 8.0808, -120 -> 7.8307, -127.9 -> 7.8836, -128 -> 7.9417. All around 8 with noise.
    #    So for x < -9.4, y = 8 + noise. The noise looks like it's uniformly distributed? Let's check range: values from ~7.82 to ~8.19. That's roughly 8 ± 0.2. Maybe uniform(-0.2, 0.2) or normal. But we can't predict noise, so we should output 8.0? Or maybe the noise is deterministic? It looks random. The problem says "output could be noisy". We'll model it as 8.0 for x < -9.4.
    #    Actually, wait: E1: x=-20.3 -> 7.9922, x=-24.3 -> 8.0603, x=-50.4 -> 7.8572, x=-6.0 -> 65.6 (linear). E2: x=-100 -> 8.1549, -80 -> 8.032, -60 -> 8.0963, -40 -> 8.0406, -30 -> 8.0646, -20 -> 8.1059, -10 -> 8.0335, -5 -> 56.0 (linear). E3: x=-55.8 -> 7.8479, -63.9 -> 7.8709. E5: x=-7.1 -> 76.16 (linear), -102.2 -> 7.9718, -16.9 -> 7.9728. E7: x=-61.3 -> 7.9227, -124.4 -> 7.9624, -25.9 -> 8.1097. E9: x=-127.7 -> 8.1698, -1.6 -> 23.36 (linear), -65.6 -> 8.1751, -44.7 -> 7.9875, -79.1 -> 8.1245, -66.9 -> 7.9435. E11: x=-13.3 -> 7.9584, -107.4 -> 8.0908, -46.1 -> 7.9342, -100.1 -> 8.0475. E12: all around 8. E13: x=-14.1 -> 7.8648, -29.5 -> 7.9463, -53.7 -> 8.0391. E15: x=-79.5 -> 7.9874, -80.2 -> 7.8628. E17: x=-27.8 -> 7.9685, -57.4 -> 7.9174.
    #    So indeed for x < -9.4, y ≈ 8 with noise. We'll output 8.0.
    # 2. For x >= -9.4, the function is linear: y = 8.0 - 9.6*x? Wait check x=10: 8 - 96 = -88.0 (E2: 10 -> -88.0). x=20: 8 - 192 = -184.0 (E2: 20 -> -184.0). x=30: 8 - 288 = -280.0 (E2: 30 -> -280.0). x=40: 8 - 384 = -376.0 (E2: 40 -> -376.0). x=60: 8 - 576 = -568.0 (E2: 60 -> -568.0). x=80: 8 - 768 = -760.0 (E2: 80 -> -760.0). x=100: 8 - 960 = -952.0 (E2: 100 -> -952.0). x=120: 8 - 1152 = -1144.0 (E2: 120 -> -1144.0). x=-5: 8 + 48 = 56.0 (E2: -5 -> 56.0). x=-10: 8 + 96 = 104? But E2: -10 -> 8.0335 (noise). Wait, -10 is less than -9.4, so it should be 8.0. Indeed E2: -10 -> 8.0335. So the linear formula applies only for x >= -9.4.
    #    Check E1: x=88.2 -> 8 - 9.6*88.2 = 8 - 846.72 = -838.72 (matches). x=66.0 -> 8 - 633.6 = -625.6 (matches). x=2.9 -> 8 - 27.84 = -19.84 (matches). x=72.7 -> 8 - 697.92 = -689.92 (matches). x=21.3 -> 8 - 204.48 = -196.48 (matches). x=-6.0 -> 8 + 57.6 = 65.6 (matches). 
    #    E3: x=104.5 -> 8 - 1003.2 = -995.2 (matches). x=1.2 -> 8 - 11.52 = -3.52 (matches). x=65.5 -> 8 - 628.8 = -620.8 (matches). x=30.3 -> 8 - 290.88 = -282.88 (matches). x=104.9 -> 8 - 1007.04 = -999.04 (matches). x=123.6 -> 8 - 1186.56 = -1178.56 (matches). x=79.4 -> 8 - 762.24 = -754.24 (matches). x=103.0 -> 8 - 988.8 = -980.8 (matches).
    #    E5: x=58.8 -> 8 - 564.48 = -556.48 (matches). x=102.1 -> 8 - 980.16 = -972.16 (matches). x=47.1 -> 8 - 452.16 = -444.16 (matches). x=-7.1 -> 8 + 68.16 = 76.16 (matches). x=28.4 -> 8 - 272.64 = -264.64 (matches). x=105.7 -> 8 - 1014.72 = -1006.72 (matches). x=119.5 -> 8 - 1147.2 = -1139.2 (matches).
    #    E7: x=93.5 -> 8 - 897.6 = -889.6 (matches). x=78.1 -> 8 - 749.76 = -741.76 (matches). x=12.5 -> 8 - 120 = -112.0 (matches). x=56.2 -> 8 - 539.52 = -531.52 (matches). x=83.2 -> 8 - 798.72 = -790.72 (matches). x=43.0 -> 8 - 412.8 = -404.8 (matches). x=-5.9 -> 8 + 56.64 = 64.64 (matches).
    #    E9: x=-1.6 -> 8 + 15.36 = 23.36 (matches). x=94.1 -> 8 - 903.36 = -895.36 (matches). x=94.8 -> 8 - 910.08 = -902.08 (matches). x=17.3 -> 8 - 166.08 = -158.08 (matches). x=119.7 -> 8 - 1149.12 = -1141.12 (matches).
    #    E11: x=77.6 -> 8 - 744.96 = -736.96 (matches). x=2.0 -> 8 - 19.2 = -11.2 (matches). x=110.8 -> 8 - 1063.68 = -1055.68 (matches). x=13.1 -> 8 - 125.76 = -117.76 (matches). x=52.9 -> 8 - 507.84 = -499.84 (matches). x=12.1 -> 8 - 116.16 = -108.16 (matches).
    #    E13: x=80.5 -> 8 - 772.8 = -764.8 (matches). x=10.3 -> 8 - 98.88 = -90.88 (matches). x=118.7 -> 8 - 1139.52 = -1131.52 (matches). x=26.4 -> 8 - 253.44 = -245.44 (matches). x=22.4 -> 8 - 215.04 = -207.04 (matches). x=24.6 -> 8 - 236.16 = -228.16 (matches). x=19.4 -> 8 - 186.24 = -178.24 (matches).
    #    E15: x=28.9 -> 8 - 277.44 = -269.44 (matches). x=40.1 -> 8 - 384.96 = -376.96 (matches). x=65.9 -> 8 - 632.64 = -624.64 (matches). x=96.5 -> 8 - 926.4 = -918.4 (matches). x=108.4 -> 8 - 1040.64 = -1032.64 (matches). x=87.7 -> 8 - 841.92 = -833.92 (matches).
    #    E17: x=101.9 -> 8 - 978.24 = -970.24 (matches). x=108.3 -> 8 - 1039.68 = -1031.68 (matches). x=10.4 -> 8 - 99.84 = -91.84 (matches). x=52.6 -> 8 - 504.96 = -496.96 (matches). x=79.8 -> 8 - 766.08 = -758.08 (matches). x=89.5 -> 8 - 859.2 = -851.2 (matches). x=101.1 -> 8 - 970.56 = -962.56 (matches). x=23.0 -> 8 - 220.8 = -212.8 (matches).
    #    So the rule is: if x < -9.4: y = 8.0 (with noise, but we output 8.0). If x >= -9.4: y = 8.0 - 9.6*x.
    #    But wait: what about x exactly -9.4? E18: x=-9.4 -> 8.0089 (noise around 8). So -9.4 is still in the noisy region. So condition is x <= -9.4? Actually E18: x=-9.4 -> 8.0089, x=-9.399 -> 98.2304. So boundary is between -9.4 and -9.399. So for x <= -9.4, y=8.0 (noisy). For x > -9.4, linear. But what about x=-9.4 exactly? It's 8.0089, so it's in the noisy region. So condition: if x <= -9.4: y=8.0; else: y=8.0 - 9.6*x.
    #    Check E4: x=-9.5 -> 7.9742 (noisy), x=-9.0 -> 94.4 (linear). x=-9.0 > -9.4, so linear: 8 - 9.6*(-9) = 94.4. Yes.
    #    Check E6: x=-9.3 -> 97.28 (linear: 8 + 89.28 = 97.28). x=-9.3 > -9.4. Yes.
    #    Check E8: x=-9.45 -> 8.0895 (noisy), x=-9.42 -> 8.0946 (noisy), x=-9.4 -> 8.1987 (noisy), x=-9.38 -> 98.048 (linear: 8 + 90.048 = 98.048). Yes.
    #    So the model is simple: piecewise linear with a constant region for x <= -9.4.
    #    But wait: is there any other region? What about x very negative? E2: x=-120 -> 7.9942, x=-100 -> 8.1549, etc. All around 8. So constant 8 for x <= -9.4.
    #    What about x very positive? Linear continues. E2: x=120 -> -1144.0. So no other break.
    #    So the function is:
    #    f(x) = 8.0 if x <= -9.4 (with noise, but we output 8.0)
    #    f(x) = 8.0 - 9.6*x if x > -9.4
    #    But wait: the noise in the constant region: the outputs are not exactly 8.0, they vary. The problem says "output could be noisy". We are to predict what the box returns. Since we can't predict noise, we should output the expected value, which is 8.0. But maybe the noise is deterministic? Looking at the values, they seem random. We'll output 8.0.
    #    However, note that in E18, x=-9.4 gave 8.0089, x=-9.401 gave 7.9539, x=-9.402 gave 7.8695, etc. These are all around 8. So we'll output 8.0.
    #    But wait: what about x exactly -9.4? It's in the noisy region. So condition: if x <= -9.4: return 8.0; else: return 8.0 - 9.6*x.
    #    Let's double-check the boundary: E18: x=-9.4 -> 8.0089 (noisy), x=-9.399 -> 98.2304 (linear). So -9.4 is noisy, -9.399 is linear. So the boundary is at -9.4. So for x <= -9.4, noisy; for x > -9.4, linear.
    #    But what about x=-9.4001? That's less than -9.4, so noisy. x=-9.3999 is greater than -9.4, so linear. So the condition is x <= -9.4.
    #    However, note that in E4, x=-9.5 -> 7.9742 (noisy), x=-9.0 -> 94.4 (linear). So consistent.
    #    So the model is:
    #    if x <= -9.4: y = 8.0
    #    else: y = 8.0 - 9.6*x
    #    But wait: is there any chance that the constant region is actually 8.0 + noise, and the noise is uniform? We can't predict noise, so we output 8.0.
    #    Also, note that in the linear region, the outputs are exact (no noise). So the noise only appears in the constant region.
    #    So the final model:
    #    For each x in probe['x']:
    #        if x <= -9.4: y = 8.0
    #        else: y = 8.0 - 9.6*x
    #    Return {'y': [y1, y2, ...]}
    #    But wait: the problem says "There may be an interval inside the domain where the function behaves differently; if so, your model should capture that interval and what happens in it." So the interval is x <= -9.4, where it's constant 8.0 (with noise). That's the interval.
    #    Also, check if there is any other break: E2 includes x=-120, -100, etc., all around 8. So no other break.
    #    So the model is complete.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            xf = float(x)
        except (TypeError, ValueError):
            ys.append(None)
            continue
        if xf <= -9.4:
            ys.append(8.0)
        else:
            ys.append(8.0 - 9.6 * xf)
    return {"y": ys}
