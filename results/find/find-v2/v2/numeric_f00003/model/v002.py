import math

def predict(probe):
    # Evidence summary:
    # E1: large |x| follows a quadratic; small |x| sits at a flat floor -20.4469.
    # E2: floor -20.4469 holds for x in [-12, 3]; at x=6 y=146.0188, x=9 y=524.3653,
    #     x=12 y=902.7117, x=15 y=1281.0582, x=18 y=1659.4047.
    #     These positive-side points are perfectly linear: slope = (1659.4047-146.0188)/(18-6)
    #     = 1513.3859/12 = 126.1155; intercept at x=6: 146.0188 - 6*126.1155 = -610.674.
    #     Check x=9: 9*126.1155 - 610.674 = 524.3655 (obs 524.3653). x=12: 902.712 (obs 902.7117).
    #     So for x >= ~4.5 the function is LINEAR, not quadratic.
    # E1 large positives (66->12950.8, 72.7->15366.1, 88.2->21854.2) are quadratic-ish,
    #     so there must be a second switch from linear to quadratic at larger x.
    # Fit quadratic through (66,12950.8364),(72.7,15366.0691),(88.2,21854.2087):
    #   a*4356+66b+c=12950.8364
    #   a*5285.29+72.7b+c=15366.0691
    #   a*7779.24+88.2b+c=21854.2087
    #   Eq2-Eq1: 929.29a+6.7b=2415.2327
    #   Eq3-Eq2: 2493.95a+15.5b=6488.1396
    #   From first: b=(2415.2327-929.29a)/6.7=360.4825-138.7a
    #   Sub: 2493.95a+15.5*(360.4825-138.7a)=6488.1396
    #   2493.95a+5587.48-2149.85a=6488.1396 -> 344.1a=900.66 -> a=2.6174
    #   b=360.4825-138.7*2.6174=360.4825-363.03=-2.55
    #   c=12950.8364-2.6174*4356-(-2.55)*66=12950.8364-11401.4+168.3=1717.7
    #   Check x=66: 2.6174*4356-2.55*66+1717.7=11401.4-168.3+1717.7=12950.8 ✓
    #   So positive quadratic: 2.6174x^2 - 2.55x + 1717.7.
    # Negative side (E1): (-61.7,5086.1272),(-50.4,2995.4039),(-24.3,166.2134),(-20.3,-15.8672)
    #   Fit quadratic through (-61.7,5086.1272),(-50.4,2995.4039),(-24.3,166.2134):
    #   3806.89a-61.7b+c=5086.1272
    #   2540.16a-50.4b+c=2995.4039
    #   590.49a-24.3b+c=166.2134
    #   Eq1-Eq2: 1266.73a-11.3b=2090.7233
    #   Eq2-Eq3: 1949.67a-26.1b=2829.1905
    #   From first: b=(1266.73a-2090.7233)/11.3=112.1a-185.02
    #   Sub: 1949.67a-26.1*(112.1a-185.02)=2829.1905
    #   1949.67a-2925.81a+4829.02=2829.1905 -> -976.14a=-1999.83 -> a=2.0487
    #   b=112.1*2.0487-185.02=229.66-185.02=44.64
    #   c=166.2134-2.0487*590.49-44.64*(-24.3)=166.2134-1209.7+1084.75=41.26
    #   Check -20.3: 2.0487*412.09+44.64*(-20.3)+41.26=844.25-906.19+41.26=-20.68 (obs -15.87, off)
    #   Check -50.4: 2.0487*2540.16+44.64*(-50.4)+41.26=5204.0-2250.0+41.3=2995.3 ✓
    #   Check -61.7: 2.0487*3806.89+44.64*(-61.7)+41.26=7799.5-2754.3+41.3=5086.5 ✓
    #   So negative quadratic: 2.0487x^2 + 44.64x + 41.26, valid for x <= ~-20.
    # Floor: -20.4469 for x in [-12, 3] (E2) and also at -6, 2.9 (E1).
    #   At -20.3 obs -15.8672, above floor; negative quad gives -20.68. So the floor region
    #   ends before -20.3, and the negative quadratic takes over around x ~ -20.
    #   Find where neg quad = floor: 2.0487x^2+44.64x+41.26 = -20.4469
    #   2.0487x^2+44.64x+61.7069=0 -> x = [-44.64 ± sqrt(1992.7-505.7)]/4.0974
    #   = [-44.64 ± sqrt(1487.0)]/4.0974 = [-44.64 ± 38.56]/4.0974
    #   Roots: (-44.64+38.56)/4.0974 = -1.484 ; (-44.64-38.56)/4.0974 = -20.31
    #   So neg quad crosses floor at x ≈ -20.31. For x < -20.31, neg quad > floor. ✓
    #   At x=-20.3 neg quad ≈ -20.68 < floor, so floor applies. But obs -15.87 > floor!
    #   Hmm, obs at -20.3 is -15.87, which is ABOVE floor but neg quad gives -20.68.
    #   The quadratic fit is slightly off near the transition. Use the fit but accept error there.
    # Positive side switch: floor vs linear. Linear L(x)=126.1155x-610.674.
    #   L(x)=floor: 126.1155x-610.674=-20.4469 -> x=590.227/126.1155=4.680.
    #   So for x > 4.68 linear applies (E2: x=6 gives 146 > floor ✓, x=3 gives -232 < floor ✓).
    # Linear vs quadratic switch: L(x)=Q(x) where Q=2.6174x^2-2.55x+1717.7.
    #   2.6174x^2-2.55x+1717.7 = 126.1155x-610.674
    #   2.6174x^2-128.6655x+2328.374=0
    #   disc=16554.8-4*2.6174*2328.374=16554.8-24377.6=-7822.8 <0 -> no real intersection!
    #   So linear is always below quadratic? At x=66: L=126.1155*66-610.674=7716.9, Q=12950.8.
    #   At x=18: L=1659.4, Q=2.6174*324-45.9+1717.7=848.0+1671.8=2519.8. Q>L.
    #   So quadratic is always above linear for large x. That means the linear region must
    #   transition to quadratic at some point where they cross — but they don't cross.
    #   Reconsider: maybe the "linear" region is actually a different quadratic that happens
    #   to look linear over [6,18]. Let's check curvature: differences 378.35, 378.35, 378.35, 378.35
    #   — perfectly linear. So it IS linear on [6,18].
    #   Then there must be a switch from linear to quadratic somewhere > 18.
    #   At x=66 obs 12950.8. Linear would give 126.1155*66-610.674=7716.9. So quadratic.
    #   Find switch: Q(x)=L(x) has no solution, so maybe the switch is a hard boundary.
    #   Guess: linear for 4.68 < x < some B, quadratic for x > B. Need B.
    #   Without more data, guess B where linear and quadratic are closest, or a round number.
    #   Actually maybe the positive side is: max(linear, quadratic)? At x=18: max(1659,2520)=2520≠obs.
    #   So no. It's piecewise: linear on [~4.68, B], quadratic on [B, ∞).
    #   Pick B such that at B, values are continuous-ish. Q(20)=2.6174*400-51+1717.7=1047+1666.7=2713.7
    #   L(20)=126.1155*20-610.674=1911.6. Q(30)=2355.7-76.5+1717.7=3996.9; L(30)=3172.8.
    #   Q(40)=4187.8-102+1717.7=5803.5; L(40)=4433.9. Q(50)=6543.5-127.5+1717.7=8133.7; L(50)=5695.1.
    #   Q(60)=9422.6-153+1717.7=10987.3; L(60)=6956.3. Q(66)=12950.8; L(66)=7716.9.
    #   The gap grows. Hard to pin B. Guess B=30 (?) — mark uncertain.
    #   Actually, maybe the whole positive side is quadratic and the "linear" region in E2 is
    #   a separate middle regime. Let's just use piecewise with a guessed boundary.
    # Negative side: floor for x in [-20.31, 4.68], neg quad for x < -20.31.
    # Positive side: floor up to 4.68, linear 4.68..B, quadratic B..inf. Guess B=30.
    x = probe.get("x", [])
    ys = []
    FLOOR = -20.4469
    for v in x:
        if v is None:
            ys.append(None)
            continue
        try:
            v = float(v)
        except Exception:
            ys.append(None)
            continue
        if v < -20.31:
            y = 2.0487*v*v + 44.64*v + 41.26
        elif v <= 4.68:
            y = FLOOR
        elif v <= 30.0:
            y = 126.1155*v - 610.674
        else:
            y = 2.6174*v*v - 2.55*v + 1717.7
        ys.append(y)
    return {"y": ys}
