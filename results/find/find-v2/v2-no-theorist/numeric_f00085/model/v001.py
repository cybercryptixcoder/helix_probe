def predict(probe):
    # Observations from E1:
    # f(88.2)=27090.784, f(66.0)=15014.0187, f(-20.3)=1545.2188,
    # f(-61.7)=13550.6196, f(2.9)=-22.8021, f(-24.3)=2154.0941,
    # f(72.7)=18241.8226, f(-50.4)=9077.3007, f(-6.0)=-22.8021,
    # f(21.3)=1532.7222
    # Pattern: large positive x -> large positive y (roughly x^2-ish).
    # Negative x -> positive y too (e.g. -61.7 -> 13550, -50.4 -> 9077).
    # Small |x| (2.9, -6.0) -> -22.8021 (a floor / constant).
    # Looks like f(x) = max(x^2 * a + b, c) or a smooth quadratic with a floor.
    # Check: 88.2^2 = 7779.24; 27090.784/7779.24 ≈ 3.482
    #        66.0^2 = 4356; 15014.0187/4356 ≈ 3.447
    #        72.7^2 = 5285.29; 18241.8226/5285.29 ≈ 3.451
    #        61.7^2 = 3806.89; 13550.6196/3806.89 ≈ 3.560
    #        50.4^2 = 2540.16; 9077.3007/2540.16 ≈ 3.573
    #        24.3^2 = 590.49; 2154.0941/590.49 ≈ 3.648
    #        21.3^2 = 453.69; 1532.7222/453.69 ≈ 3.378
    #        20.3^2 = 412.09; 1545.2188/412.09 ≈ 3.750
    # Roughly y ≈ 3.5*x^2 for |x| large, but small x gives -22.8.
    # Try y = 3.5*x^2 - 22.8? For x=2.9: 3.5*8.41-22.8 = 6.6, not -22.8.
    # Maybe y = max(3.5*x^2 + c, -22.8021)? For x=2.9: 3.5*8.41=29.4, too big.
    # Try y = a*x^2 + b with floor. Fit using 88.2 and 66.0:
    #   a*7779.24 + b = 27090.784
    #   a*4356 + b = 15014.0187
    #   a*(3423.24) = 12076.7653 -> a ≈ 3.528, b ≈ -353.5
    # Check x=72.7: 3.528*5285.29-353.5 = 18295, close to 18241.8.
    # Check x=61.7: 3.528*3806.89-353.5 = 13079, observed 13550. Off.
    # Check x=50.4: 3.528*2540.16-353.5 = 8608, observed 9077. Off.
    # Check x=24.3: 3.528*590.49-353.5 = 1729, observed 2154. Off.
    # Check x=20.3: 3.528*412.09-353.5 = 1100, observed 1545. Off.
    # Check x=21.3: 3.528*453.69-353.5 = 1247, observed 1532. Off.
    # Hmm, ratio y/x^2 varies: 3.48, 3.45, 3.45, 3.56, 3.57, 3.65, 3.38, 3.75.
    # Not a clean quadratic. Maybe y = a*x^2 + b*x + c.
    # Let's solve with three points: (88.2,27090.784),(66,15014.0187),(2.9,-22.8021)
    # Actually the small values 2.9 and -6.0 both give exactly -22.8021, suggesting
    # a floor (ReLU-like) at -22.8021.
    # Try y = max(a*x^2 + b*x + c, -22.8021).
    # Use 88.2, 66, 72.7 to solve quadratic:
    # 7779.24a + 88.2b + c = 27090.784
    # 4356a + 66b + c = 15014.0187
    # 5285.29a + 72.7b + c = 18241.8226
    # Subtract eq2 from eq1: 3423.24a + 22.2b = 12076.7653
    # Subtract eq2 from eq3: 929.29a + 6.7b = 3227.8039
    # From second: b = (3227.8039 - 929.29a)/6.7
    # Plug: 3423.24a + 22.2*(3227.8039-929.29a)/6.7 = 12076.7653
    # 22.2/6.7 = 3.31343; 3.31343*3227.8039 = 10695.6; 3.31343*929.29 = 3079.0
    # 3423.24a + 10695.6 - 3079.0a = 12076.7653
    # 344.24a = 1381.17 -> a = 4.012
    # b = (3227.8039 - 929.29*4.012)/6.7 = (3227.8 - 3728.3)/6.7 = -74.7
    # c = 15014.0187 - 4356*4.012 - 66*(-74.7) = 15014 - 17476 + 4930 = 2468
    # Check x=61.7: 4.012*3806.89 - 74.7*61.7 + 2468 = 15273 - 4609 + 2468 = 13132, obs 13550. Off by 400.
    # Check x=50.4: 4.012*2540.16 - 74.7*50.4 + 2468 = 10191 - 3765 + 2468 = 8894, obs 9077. Off by 180.
    # Check x=24.3: 4.012*590.49 - 74.7*24.3 + 2468 = 2369 - 1815 + 2468 = 3022, obs 2154. Off.
    # Not great. The MLP approximates something; maybe it's x^2 scaled with a soft floor.
    # Given uncertainty, best guess: y ≈ max(k*x^2 + m, floor) with k~3.5, floor~-22.8.
    # But the fit isn't clean. Let me try y = a*|x|^p form.
    # log(27090.784/15014.0187) = log(1.8044) = 0.590
    # log(88.2/66) = log(1.3364) = 0.290
    # p = 0.590/0.290 = 2.03 -> p≈2. Good, quadratic.
    # So y ≈ a*x^2 + b with floor. The variation suggests maybe a*x^2 + b|x| + c.
    # Let me just fit least squares mentally... hard. Use a*x^2 + b with floor.
    # From 88.2: a*7779.24 + b = 27090.784
    # From 24.3: a*590.49 + b = 2154.0941
    # Subtract: a*7188.75 = 24936.69 -> a = 3.469, b = 2154.0941 - 3.469*590.49 = 2154 - 2048 = 106
    # Check 66: 3.469*4356+106 = 15117, obs 15014. Close.
    # Check 72.7: 3.469*5285.29+106 = 18441, obs 18242. Close.
    # Check 61.7: 3.469*3806.89+106 = 13312, obs 13551. Off 240.
    # Check 50.4: 3.469*2540.16+106 = 8918, obs 9077. Off 160.
    # Check 21.3: 3.469*453.69+106 = 1680, obs 1533. Off 150.
    # Check 20.3: 3.469*412.09+106 = 1535, obs 1545. Close!
    # Check 2.9: 3.469*8.41+106 = 135, obs -22.8. Way off -> floor.
    # Check -6.0: same, floor.
    # So floor at -22.8021 for small |x|. Where does floor end?
    # At x=20.3, y=1545 > floor. At x=2.9, y=-22.8 = floor.
    # Try x where 3.469*x^2+106 = -22.8 -> x^2 = -37 -> impossible.
    # So floor isn't from this quadratic. Maybe y = max(a*x^2 + b, c) with c=-22.8
    # and the quadratic crosses c at some x. 3.469x^2+106 = -22.8 never. 
    # So the floor must be a separate regime: for |x| < threshold, y = -22.8.
    # Threshold between 2.9 and 20.3. Unknown. Guess ~10?
    # Actually maybe it's y = a*x^2 + b for |x|>t, else -22.8.
    # Or maybe y = max(a*x^2 + b, -22.8) with different a,b.
    # Let's fit a*x^2+b using 20.3 and 88.2:
    # 7779.24a+b=27090.784; 412.09a+b=1545.2188
    # 7367.15a = 25545.565 -> a=3.467, b=1545.2188-3.467*412.09=1545-1429=116
    # Check 2.9: 3.467*8.41+116 = 145, not -22.8. So floor regime.
    # The floor regime: |x| small -> -22.8. Boundary unknown.
    # Given MLP, maybe it's a smooth function. But observed exactly -22.8021 twice
    # suggests a hard floor (ReLU). So y = max(g(x), -22.8021) where g(x) ~ 3.47x^2+116?
    # But g(2.9)=145 > -22.8, so max would give 145, not -22.8. Contradiction.
    # Unless g(x) = 3.47x^2 - 22.8 for small x... no.
    # Alternative: y = 3.47*x^2 + 116 for |x|>t, and -22.8 for |x|<t.
    # That's a piecewise function. t between 2.9 and 20.3.
    # Hmm, but MLP wouldn't do hard piecewise. Maybe it's y = a*x^2 + b*sin(...)...
    # Given limited data, best guess: y = 3.47*x^2 + 116 for |x| >= 15, else -22.8.
    # Actually let me reconsider: maybe y = 3.5*x^2 - 22.8 for all x, but for small x
    # it's clipped? 3.5*2.9^2-22.8 = 29.4-22.8 = 6.6, not -22.8.
    # What if y = max(3.5*x^2 - 22.8, -22.8)? For x=2.9: max(6.6,-22.8)=6.6. No.
    # What if y = 3.5*x^2 - 22.8 but with a different form for small x?
    # The two -22.8021 values (x=2.9, x=-6.0) are suspiciously identical.
    # Maybe the function is y = 3.5*x^2 - 22.8 for |x|>some, and constant -22.8 for |x|<some.
    # I'll go with: y = 3.47*x^2 + 116 for |x| > 10, else -22.8021.
    # This is a guess; mark with ?.
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if abs(x) < 10:
                out.append(-22.8021)
            else:
                out.append(3.47 * x * x + 116.0)
        except Exception:
            out.append(None)
    return {"y": out}
