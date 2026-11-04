def predict(probe):
    # Model: y = 4.76*x + a smooth localized bump near x=0 [E2,E3,E4,E5,E6]
    # Away from origin, pure linear slope ~4.76 [E2: -464.46/-100=4.6446 ... 475.62/100=4.7562]
    # Actually slope varies slightly: check large |x|: 475.6174/100=4.7562, -464.4556/-100=4.6446
    # Hmm asymmetric. Let's fit linear on large points and add origin bump.
    # E4: at x=0 y=3.9155; linear through origin would give 0. So bump at 0 ~ +3.9
    # E6 shows bump: y(0.2)=4.9996, y(-0.2)=2.9898. Linear part ~4.76*0.2=0.95, so bump ~4.05 at +0.2, ~2.04 at -0.2
    # y(0.5)=6.5856 vs 4.76*0.5=2.38 -> bump 4.2; y(-0.5)=1.9577 vs -2.38 -> bump 4.34
    # y(1)=8.9349 vs 4.76 -> bump 4.17; y(-1)=-0.2396 vs -4.76 -> bump 4.52
    # y(2)=13.6499 vs 9.52 -> bump 4.13; y(-2)=-5.1471 vs -9.52 -> bump 4.37
    # y(3)=18.3544 vs 14.28 -> bump 4.07; y(-3)=-9.8956 vs -14.28 -> bump 4.38
    # y(4)=23.0684 vs 19.04 -> bump 4.03; y(-4)=-14.5911 vs -19.04 -> bump 4.45
    # y(6)=32.4965 vs 28.56 -> bump 3.94; y(8)=41.9246 vs 38.08 -> bump 3.84
    # So bump ~4.0-4.4, roughly constant then decaying. Looks like a plateau bump ~4.2 for |x|<5, decaying.
    # Actually bump seems slightly larger on negative side. Could be y = 4.76*x + 4.2*exp(-x^2/50)? 
    # Let's estimate: at x=8 bump=3.84, at x=0 ~3.9? Wait y(0)=3.9155 so bump=3.9155.
    # Hmm at x=0 bump=3.92, at x=8 bump=3.84. Nearly constant! 
    # But at x=20: y=98.4932, 4.76*20=95.2 -> bump 3.29
    # x=40: 192.7743 vs 190.4 -> bump 2.37
    # x=60: 287.0553 vs 285.6 -> bump 1.46
    # x=100: 475.6174 vs 476 -> bump -0.38
    # x=-100: -464.4556 vs -476 -> bump +11.5?? That's odd. Slope maybe not 4.76.
    # Let's fit slope from far points: (475.6174-(-464.4556))/(100-(-100))=940.073/200=4.7004
    # Then intercept: 475.6174-4.7004*100=5.577. Hmm.
    # Check x=60: 4.7004*60+5.577=287.6 vs 287.0553 ok
    # x=-60: -282.02+5.577=-276.45 vs -276.99 ok
    # x=20: 94.008+5.577=99.58 vs 98.49 slightly off
    # x=-20: -94.008+5.577=-88.43 vs -89.52 off
    # So there's curvature. Let's use slope 4.7, intercept 5.5, plus correction.
    # Actually simpler: fit quadratic? Let's check E2 points:
    # x=-100:-464.4556, -80:-370.7228, -60:-276.9899, -40:-183.2571, -20:-89.5243, -10:-42.676
    # differences: 93.73, 93.73, 93.73, 93.73, 46.85 (per 20,20,20,20,10)
    # So slope between -100 and -80: 4.6865; -80 to -60: 4.6865; -60 to -40: 4.6865; -40 to -20: 4.6865; -20 to -10: 4.685
    # Very linear on negative side with slope 4.6865!
    # Positive: 10:51.3527, 20:98.4932 diff 47.14/10=4.714; 20->40: 94.28/20=4.714; 40->60:94.28/20=4.714; 60->80:94.28/20=4.714; 80->100:94.28/20=4.714
    # So positive slope 4.714, negative slope 4.6865. Slight asymmetry.
    # Intercept: at x=10: 51.3527-47.14=4.21; at x=-10: -42.676+46.865=4.189
    # So y ≈ 4.7*x + 4.2 for large |x|? Check x=100: 470+4.2=474.2 vs 475.6 close. x=-100:-470+4.2=-465.8 vs -464.46 close.
    # So actually the "bump" is a constant offset ~4.2, not localized! 
    # But E4 at x=0: y=3.9155, and 4.7*0+4.2=4.2 close. At x=5: 4.7*5+4.2=27.7 vs 27.78 ok!
    # At x=-5: -23.5+4.2=-19.3 vs -19.2559 ok!
    # At x=30: 141+4.2=145.2 vs 145.63 ok
    # So it's just y = 4.7*x + 4.2 approximately, with slight slope asymmetry.
    # Let's refine: positive slope 4.714, negative slope 4.6865, intercept ~4.2
    # Check E6 small: x=0.2: 4.714*0.2+4.2=5.14 vs 4.9996; x=-0.2: -0.937+4.2=3.26 vs 2.99
    # x=1: 4.714+4.2=8.91 vs 8.93 ok; x=-1: -4.6865+4.2=-0.4865 vs -0.2396 off by 0.25
    # x=2: 9.43+4.2=13.63 vs 13.65 ok; x=-2: -9.37+4.2=-5.17 vs -5.147 ok
    # x=4: 18.86+4.2=23.06 vs 23.07 ok; x=-4: -18.75+4.2=-14.55 vs -14.59 ok
    # x=8: 37.7+4.2=41.9 vs 41.92 ok
    # Good enough. Slight nonlinearity near 0 maybe.
    # Let's use: y = 4.7*x + 4.2 + small correction
    # Actually E1: x=2.9: 4.7*2.9+4.2=17.83 vs 17.8834 ok
    # x=-6: -28.2+4.2=-24 vs -23.9374 ok
    # x=21.3: 100.11+4.2=104.31 vs 104.62 ok
    # x=-20.3: -95.41+4.2=-91.21 vs -90.93 ok
    # Great, y=4.7*x+4.2 fits well.
    # Refine slope: use 4.7, intercept 4.2. Check E2 x=100: 474.2 vs 475.62 (off 1.4). 
    # Maybe slope 4.71: 471+4.2=475.2 vs 475.62. x=-100: -471+4.2=-466.8 vs -464.46 off -2.3
    # Asymmetric slope: use 4.714 for x>0, 4.6865 for x<0.
    # x=100: 471.4+4.2=475.6 ok; x=-100: -468.65+4.2=-464.45 ok!
    # x=60: 282.84+4.2=287.04 vs 287.055 ok; x=-60: -281.19+4.2=-276.99 ok!
    # x=20: 94.28+4.2=98.48 vs 98.49 ok; x=-20: -93.73+4.2=-89.53 vs -89.52 ok!
    # Excellent. So y = 4.714*x+4.2 for x>=0, y=4.6865*x+4.2 for x<0.
    # Check E6 x=0.2: 0.9428+4.2=5.14 vs 4.9996 (off 0.14); x=-0.2: -0.9373+4.2=3.26 vs 2.99 (off 0.27)
    # Small discrepancy near origin. Maybe intercept slightly lower near 0, or smooth transition.
    # At x=0: 4.2 vs 3.9155 (off 0.28). So intercept dips near 0.
    # Let's add small correction: subtract 0.28*exp(-x^2/2)? At x=0: -0.28 -> 3.92 ok. At x=1: -0.28*0.606=-0.17 -> 8.91-0.17=8.74 vs 8.93 off. Hmm.
    # Maybe just use intercept 4.0 and slope slightly higher? 
    # Try y=4.72*x+4.0 for x>0: x=100:472+4=476 vs 475.62; x=0:4.0 vs 3.92; x=1:8.72 vs 8.93
    # Let's keep it simple: piecewise slope with intercept 4.1, and small dip at origin.
    # Actually the discrepancy is small (<0.3). Use y = slope*x + 4.1 + 0.1*tanh(|x|) ? 
    # Simpler: y = slope*x + 4.2 - 0.3*exp(-x*x/4)
    # x=0: 4.2-0.3=3.9 vs 3.92 ok; x=1: 4.714+4.2-0.3*0.778=8.68 vs 8.93 off 0.25
    # Hmm. Let's just do y = slope*x + 4.2 with tiny origin correction, or accept small error.
    # Given match was 0.94, main fix is adding the intercept 4.2 (v1 had intercept ~4.5 but slope 4.76).
    # v1: slope 4.76, intercept ~4.5. At x=0: 4.5 vs 3.92. At x=100: 480.5 vs 475.6.
    # New: piecewise slope 4.714/4.6865, intercept 4.2. Much better.
    # Add small origin dip: -0.28*exp(-x^2/1.5) for |x|<3?
    # At x=0: -0.28 -> 3.92 ok; x=0.5: 4.714*0.5+4.2-0.28*0.846=2.357+4.2-0.237=6.32 vs 6.586 off 0.27
    # x=-0.5: -2.343+4.2-0.237=1.62 vs 1.958 off 0.34
    # Hmm the bump is wider. Let's use exp(-x^2/8): x=0.5: 0.969 -> -0.271; x=1: 0.882 -> -0.247
    # x=1: 4.714+4.2-0.247=8.67 vs 8.93 off 0.26
    # The data near origin: y(0)=3.9155, y(1)=8.9349, y(-1)=-0.2396
    # Linear from 0 to 1: slope 5.02; from -1 to 0: slope 4.155
    # So near origin slope is steeper on positive side, shallower on negative.
    # This is getting complex. Let's just fit a smooth function.
    # Try y = a*x + b + c*x^2? 
    # Use E6 points to fit: 
    # Actually simplest good model: piecewise linear with intercept 4.2, plus small correction.
    # Let me just use: y = 4.7*x + 4.2 + 0.3*sin(x*0.5)*exp(-|x|/10)? Too hacky.
    # Given exam is on sealed probes, a good global fit matters. Let's use:
    # y = 4.7*x + 4.2 for |x|>5, and interpolate near origin.
    # Actually let's just fit a cubic or use the piecewise slope with intercept 4.2 and accept ~0.2 error near origin.
    # Better: fit y = m*x + b + c*exp(-x^2/s) with m=4.7, b=4.2, c=-0.3, s=2
    # x=0: 4.2-0.3=3.9 ok; x=1: 4.7+4.2-0.3*0.606=8.72 vs 8.93; x=2: 9.4+4.2-0.3*0.135=13.56 vs 13.65
    # x=-1: -4.7+4.2-0.18=-0.68 vs -0.24 off 0.44
    # The negative side near origin is higher than linear. y(-1)=-0.24, linear -4.7+4.2=-0.5. So bump +0.26.
    # y(-0.5)=1.958, linear -2.35+4.2=1.85, bump +0.11
    # y(-2)=-5.147, linear -9.4+4.2=-5.2, bump +0.05
    # So negative side has small positive bump near origin ~0.3 at x=-1.
    # Positive side: y(1)=8.93, linear 8.9, bump +0.03. y(0.5)=6.586, linear 6.55, bump +0.04.
    # So mostly linear except small negative-side bump near x=-1.
    # This is minor. Let's use piecewise slope + intercept 4.2, plus small correction term.
    # Final: y = (4.714 if x>=0 else 4.6865)*x + 4.2 - 0.28*exp(-x*x/1.0) + 0.3*exp(-(x+1)**2/1.0)
    # Check x=0: 4.2-0.28+0.3*0.368=4.2-0.28+0.11=4.03 vs 3.92 ok
    # x=1: 4.714+4.2-0.28*0.368+0.3*0.018=8.91-0.103+0.005=8.81 vs 8.93
    # x=-1: -4.6865+4.2-0.103+0.3=-0.49+0.3=-0.19 vs -0.24 ok
    # x=-0.5: -2.343+4.2-0.28*0.779+0.3*0.607=1.857-0.218+0.182=1.82 vs 1.958
    # Meh. Good enough. Let's simplify: just piecewise slope + 4.2, small origin dip.
    # I'll go with: y = m*x + 4.2 - 0.25*exp(-x*x/1.5) + 0.25*exp(-(x+0.8)**2/1.5)
    # Actually let me just use a clean fit: y = 4.7*x + 4.2 + 0.3*exp(-(x+1)**2/2) - 0.3*exp(-x*x/2)
    # x=0: 4.2-0.3+0.3*0.607=4.08 vs 3.92
    # I'll keep it simpler and accept small error. The main improvement is intercept 4.2 and correct slopes.
    import math
    def f(x):
        m = 4.714 if x >= 0 else 4.6865
        y = m*x + 4.2
        # small origin correction
        y += -0.28*math.exp(-x*x/1.5)
        y += 0.28*math.exp(-(x+1.0)**2/1.5)
        return y
    return {"y": [f(x) for x in probe["x"]]}
