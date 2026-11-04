import math

def predict(probe):
    # Beliefs (revised after E13):
    # - Far field (|x| >= ~13) is a smooth, nearly linear ramp in x:
    #   y ~ 0.0002*x + 0.022, rising from ~0.02 at x=-20 to ~0.05 at x=120 [E10,E9,E5,E7,E13].
    #   Small residual wiggles only; treat as linear. [E10,E13]
    # - There is a sharp "core" structure centered at origin, |x| < ~13.
    # - Core left lobe: rises from ~0.019 at x=-12 to peak ~0.078 at x=-1.5..-2,
    #   then falls steeply to ~0 at x=0. [E2,E6,E8,E12]
    # - Core right lobe: from ~0 at x=0 falls to a trough ~-0.088 near x=1.25,
    #   then rises back toward ~-0.02 at x=12. [E12,E6,E8]
    # - The core connects smoothly to the far-field ramp at |x|~12-13. [E10,E4]
    # - Noisy; outputs approximate.

    x = probe["x"]
    return {"y": [_f(v) for v in x]}


def _f(x):
    try:
        x = float(x)
    except Exception:
        return None
    if math.isnan(x) or math.isinf(x):
        return None

    ax = abs(x)
    if ax >= 13.0:
        return _background(x)
    return _core(x)


def _background(x):
    # Far field: near-linear ramp y ~ 0.0002*x + 0.022 [E10,E9,E5,E7,E13].
    # Check: x=-128 -> 0.022-0.0256=-0.0036? observed 0.0479. Not great at extremes.
    # Use quadratic fit through (-128,0.0479),(0,-0.0008),(128,0.0565):
    #   a=3.24e-6, b=3.36e-5, c=-0.0008
    # Check x=60: 0.0117+0.0020-0.0008=0.0129 vs observed 0.0198 (off)
    # Check x=120: 0.0467+0.0040-0.0008=0.0499 vs 0.0522 (ok)
    # Check x=-60: 0.0117-0.0020-0.0008=0.0089 vs 0.0277 (bad)
    # The negative side is higher than quadratic predicts. Try a better fit.
    # Points: (-128,0.0479),(-100,0.0394),(-60,0.0277),(-20,0.0162),
    #         (20,-0.0043),(60,0.0198),(100,0.0415),(120,0.0522),(128,0.0565)
    # This looks like y = a*x^2 + b*x + c with a~3.2e-6, b~3.4e-5, c~-0.0008
    # but negative side is systematically higher. Add a small odd term? 
    # Actually check: at x=-20: 3.24e-6*400 + 3.36e-5*(-20) -0.0008 = 0.0013-0.00067-0.0008=-0.0002 vs 0.0162. Off by 0.016.
    # At x=20: 0.0013+0.00067-0.0008=0.0012 vs -0.0043. Off by 0.005.
    # So there's an asymmetry: negative side higher. Maybe y = a*x^2 + b*x + c + d*|x|?
    # Let's just fit a quadratic in |x| plus linear in x.
    # y = A*x^2 + B*x + C + D*|x|
    # Use least squares mentally... simpler: fit y = p*x^2 + q*x + r for x>=0 and x<0 separately? 
    # Actually the data suggests roughly y ~ 0.0002*x + 0.022 for moderate range, 
    # with curvature at extremes. Let's use a cubic-ish or just piecewise.
    # Simplest good fit: y = 0.0002*x + 0.022 + 1.5e-6*x^2 (curvature up at extremes)
    # Check x=-128: -0.0256+0.022+0.0246=0.021 vs 0.0479 (bad)
    # Hmm. Let's just use the quadratic fit but add a correction for negative x.
    # Actually let's fit properly: 
    # Using points (-128,0.0479),(0,-0.0008),(128,0.0565) gave a=3.24e-6,b=3.36e-5,c=-0.0008
    # At x=-60: 0.0117-0.0020-0.0008=0.0089 vs 0.0277. Need +0.019.
    # At x=-20: -0.0002 vs 0.0162. Need +0.016.
    # At x=-100: 0.0324-0.0034-0.0008=0.0282 vs 0.0394. Need +0.011.
    # So negative side needs a bump of ~0.015 around x=-20 to -60, decaying.
    # This could be a broad Gaussian centered around x=-40? 
    # At x=-40: 0.0052-0.0013-0.0008=0.0031 vs 0.0219. Need +0.019.
    # At x=-80: 0.0207-0.0027-0.0008=0.0172 vs 0.0335. Need +0.016.
    # At x=-120: 0.0467-0.0040-0.0008=0.0419 vs 0.0455. Need +0.004.
    # So a broad bump centered around x=-50, amplitude ~0.02, width ~50.
    # Let's add: 0.02 * exp(-((x+50)/50)^2)
    # Check x=-20: 0.02*exp(-(30/50)^2)=0.02*exp(-0.36)=0.02*0.698=0.014. Good.
    # x=-60: 0.02*exp(-(10/50)^2)=0.02*0.96=0.019. Good.
    # x=-100: 0.02*exp(-(50/50)^2)=0.02*0.368=0.0074. vs need 0.011. Close.
    # x=-128: 0.02*exp(-(78/50)^2)=0.02*exp(-2.43)=0.0018. vs need 0.006. Ok.
    # x=0: 0.02*exp(-1)=0.0074. But at x=0 we want -0.0008. Hmm, this bump would affect x=0.
    # But x=0 is in the core, not background. For background we only use |x|>=13.
    # At x=13: 0.02*exp(-(63/50)^2)=0.02*exp(-1.59)=0.0041. 
    # At x=-13: 0.02*exp(-(37/50)^2)=0.02*exp(-0.55)=0.0115.
    # Hmm, this creates asymmetry. Let's check positive side.
    # Positive side: x=20: 0.0012 vs -0.0043. Need -0.0055.
    # x=60: 0.0129 vs 0.0198. Need +0.007.
    # x=100: 0.0324+0.0034-0.0008=0.035 vs 0.0415. Need +0.0065.
    # x=120: 0.0467+0.0040-0.0008=0.0499 vs 0.0522. Need +0.0023.
    # x=128: 0.0531+0.0043-0.0008=0.0566 vs 0.0565. Good.
    # So positive side needs a small bump around x=60-100, amplitude ~0.007.
    # Add: 0.007 * exp(-((x-80)/40)^2)
    # Check x=60: 0.007*exp(-(20/40)^2)=0.007*0.78=0.0055. Good.
    # x=100: 0.007*exp(-(20/40)^2)=0.0055. Good.
    # x=20: 0.007*exp(-(60/40)^2)=0.007*0.105=0.0007. vs need -0.0055. Still off.
    # At x=20 observed -0.0043, quadratic gives 0.0012. Off by -0.0055.
    # Hmm, maybe the quadratic fit is just not great. Let me refit.
    # Actually let's use a simpler approach: fit y = a*x^2 + b*x + c to all 9 points.
    # Sum x = -128-100-60-20+20+60+100+120+128 = 120
    # Sum x^2 = 16384+10000+3600+400+400+3600+10000+14400+16384 = 75168
    # Sum x^3 = -2097152-1000000-216000-8000+8000+216000+1000000+1728000+2097152 = 1600000
    # Sum x^4 = 268435456+100000000+12960000+160000+160000+12960000+100000000+207360000+268435456 = 868435456
    # Sum y = 0.0479+0.0394+0.0277+0.0162-0.0043+0.0198+0.0415+0.0522+0.0565 = 0.2969
    # Sum xy = -128*0.0479 -100*0.0394 -60*0.0277 -20*0.0162 +20*(-0.0043)+60*0.0198+100*0.0415+120*0.0522+128*0.0565
    # = -6.1312 -3.94 -1.662 -0.324 -0.086 +1.188 +4.15 +6.264 +7.232 = 6.6908
    # Sum x^2y = 16384*0.0479 +10000*0.0394 +3600*0.0277 +400*0.0162 +400*(-0.0043)+3600*0.0198+10000*0.0415+14400*0.0522+16384*0.0565
    # = 784.79 +394 +99.72 +6.48 -1.72 +71.28 +415 +751.68 +925.7 = 3446.93
    # Normal equations:
    # 9c + 120b + 75168a = 0.2969
    # 120c + 75168b + 1600000a = 6.6908
    # 75168c + 1600000b + 868435456a = 3446.93
    # From first: c = (0.2969 - 120b - 75168a)/9 = 0.03299 - 13.333b - 8352a
    # Sub into second: 120*(0.03299 - 13.333b - 8352a) + 75168b + 1600000a = 6.6908
    # 3.9588 - 1600b - 1002240a + 75168b + 1600000a = 6.6908
    # 73568b + 597760a = 2.732
    # Sub into third: 75168*(0.03299 - 13.333b - 8352a) + 1600000b + 868435456a = 3446.93
    # 2479.8 - 1002240b - 627840000a + 1600000b + 868435456a = 3446.93
    # 597760b + 240595456a = 967.13
    # Solve: from second eq: b = (2.732 - 597760a)/73568 = 3.713e-5 - 8.125a
    # Sub: 597760*(3.713e-5 - 8.125a) + 240595456a = 967.13
    # 22.19 - 4856800a + 240595456a = 967.13
    # 235738656a = 944.94
    # a = 4.008e-6
    # b = 3.713e-5 - 8.125*4.008e-6 = 3.713e-5 - 3.257e-5 = 4.56e-6
    # c = 0.03299 - 13.333*4.56e-6 - 8352*4.008e-6 = 0.03299 - 6.08e-5 - 0.03348 = -0.00055
    # So y = 4.008e-6*x^2 + 4.56e-6*x - 0.00055
    # Check x=-128: 4.008e-6*16384 + 4.56e-6*(-128) - 0.00055 = 0.06567 - 0.00058 - 0.00055 = 0.0645 vs 0.0479. Off by 0.017.
    # Check x=128: 0.06567 + 0.00058 - 0.00055 = 0.0657 vs 0.0565. Off by 0.009.
    # Check x=-60: 4.008e-6*3600 + 4.56e-6*(-60) - 0.00055 = 0.01443 - 0.00027 - 0.00055 = 0.0136 vs 0.0277. Off by 0.014.
    # Check x=60: 0.01443 + 0.00027 - 0.00055 = 0.01415 vs 0.0198. Off by 0.006.
    # Check x=-20: 4.008e-6*400 + 4.56e-6*(-20) - 0.00055 = 0.0016 - 0.00009 - 0.00055 = 0.00096 vs 0.0162. Off by 0.015.
    # Check x=20: 0.0016 + 0.00009 - 0.00055 = 0.00114 vs -0.0043. Off by -0.005.
    # Still not great. The negative side is consistently higher.
    # Let me try fitting with a |x| term: y = a*x^2 + b*x + c + d*|x|
    # This is getting complex. Let's just use a simpler piecewise linear fit.
    # From E10 data:
    # x: -128,-120,-100,-80,-60,-40,-30,-25,-15,-12,12,15,25,40,60,80,100,120,128
    # y: 0.0479,0.0455,0.0394,0.0335,0.0277,0.0219,0.0191,0.0177,0.0146,0.0187,-0.0208,-0.0146,0.0009,0.0089,0.0198,0.0307,0.0415,0.0522,0.0565
    # This looks like a smooth curve. Let me just interpolate linearly between these points.
    # That's the most reliable approach given the data.
    pts = [
        (-128, 0.0479), (-120, 0.0455), (-100, 0.0394), (-80, 0.0335),
        (-60, 0.0277), (-40, 0.0219), (-30, 0.0191), (-25, 0.0177),
        (-15, 0.0146), (-12, 0.0187), (12, -0.0208), (15, -0.0146),
        (25, 0.0009), (40, 0.0089), (60, 0.0198), (80, 0.0307),
        (100, 0.0415), (120, 0.0522), (128, 0.0565)
    ]
    # Linear interpolation
    if x <= pts[0][0]:
        # extrapolate using first two
        x0, y0 = pts[0]
        x1, y1 = pts[1]
        return y0 + (x - x0) * (y1 - y0) / (x1 - x0)
    if x >= pts[-1][0]:
        x0, y0 = pts[-2]
        x1, y1 = pts[-1]
        return y1 + (x - x1) * (y1 - y0) / (x1 - x0)
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i+1]
        if x0 <= x <= x1:
            return y0 + (x - x0) * (y1 - y0) / (x1 - x0)
    return 0.0


def _core(x):
    # Piecewise linear skeleton matching E2,E6,E8,E12.
    if x <= -6.0:
        # -12->0.0187, -6.5->0.0431: slope 0.00444
        return 0.0187 + (x + 12.0) * 0.00444
    elif x <= -1.5:
        # -6.5->0.0431, -1.5->0.078: slope 0.0078
        return 0.0431 + (x + 6.5) * 0.0078
    elif x <= -0.75:
        # -1.5->0.078, -0.75->0.0728: slope -0.00693
        return 0.078 + (x + 1.5) * (-0.00693)
    elif x <= -0.25:
        # -0.75->0.0728, -0.25->0.0229: slope -0.0998
        return 0.0728 + (x + 0.75) * (-0.0998)
    elif x <= 0.0:
        # -0.25->0.0229, 0->-0.0008: slope -0.0948
        return 0.0229 + (x + 0.25) * (-0.0948)
    elif x <= 0.25:
        # 0->-0.0008, 0.25->-0.0246: slope -0.0952
        return -0.0008 + x * (-0.0952)
    elif x <= 0.5:
        # 0.25->-0.0246, 0.5->-0.0484: slope -0.0952
        return -0.0246 + (x - 0.25) * (-0.0952)
    elif x <= 0.75:
        # 0.5->-0.0484, 0.75->-0.0819: slope -0.134
        return -0.0484 + (x - 0.5) * (-0.134)
    elif x <= 1.25:
        # 0.75->-0.0819, 1.25->-0.0877: slope -0.0116
        return -0.0819 + (x - 0.75) * (-0.0116)
    elif x <= 1.75:
        # 1.25->-0.0877, 1.75->-0.0686: slope 0.0382
        return -0.0877 + (x - 1.25) * 0.0382
    elif x <= 2.25:
        # 1.75->-0.0686, 2.25->-0.0551: slope 0.027
        return -0.0686 + (x - 1.75) * 0.027
    elif x <= 3.5:
        # 2.25->-0.0551, 3.5->-0.0452: slope 0.00792
        return -0.0551 + (x - 2.25) * 0.00792
    elif x <= 6.0:
        # 3.5->-0.0452, 6->-0.0371: slope 0.00324
        return -0.0452 + (x - 3.5) * 0.00324
    elif x <= 12.0:
        # 6->-0.0371, 12->-0.0208: slope 0.00272
        return -0.0371 + (x - 6.0) * 0.00272
    else:
        return -0.0208
