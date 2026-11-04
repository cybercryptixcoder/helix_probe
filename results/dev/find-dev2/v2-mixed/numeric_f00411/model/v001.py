def predict(probe):
    # f(x) = 2.7 * x  (linear through origin) [E1]
    # Check: 88.2*2.7=238.14 vs 238.72; 66*2.7=178.2 vs 181.0
    # Hmm, not exact. Let's check ratios: 238.72/88.2=2.7066, 181/66=2.7424,
    # -38.58/-20.3=1.9005, -146.22/-61.7=2.3699, 16.94/2.9=5.84,
    # -48.98/-24.3=2.0156, 198.42/72.7=2.7293, -116.84/-50.4=2.3183,
    # -1.4/-6.0=0.2333, 64.78/21.3=3.0413
    # Ratios vary wildly -> not pure linear. Try f(x)=x*2.7 rounded? No.
    # Try f(x) = round(x*2.7)? 88.2*2.7=238.14 -> 238.72 no.
    # Maybe f(x) = x*2.7 + noise. Or f(x)=x*e? e=2.718: 88.2*2.718=239.7 no.
    # Look: 2.9 -> 16.94. 16.94/2.9=5.84. -6.0 -> -1.4.
    # Try f(x) = x + something? 88.2->238.72 diff 150.52. Not constant.
    # Try f(x)=x^2/... no, negative x gives negative y.
    # Try f(x) = x*2.7 with rounding to 2 decimals? 88.2*2.7=238.14, no.
    # Maybe f(x)=x*2.7 but x perturbed? 
    # Let's fit: slope via (238.72-181)/(88.2-66)=57.72/22.2=2.6
    # (181-64.78)/(66-21.3)=116.22/44.7=2.6
    # (64.78-16.94)/(21.3-2.9)=47.84/18.4=2.6
    # (16.94-(-1.4))/(2.9-(-6))=18.34/8.9=2.06 hmm
    # (-1.4-(-38.58))/(-6-(-20.3))=37.18/14.3=2.6
    # (-38.58-(-48.98))/(-20.3-(-24.3))=10.4/4=2.6
    # (-48.98-(-116.84))/(-24.3-(-50.4))=67.86/26.1=2.6
    # (-116.84-(-146.22))/(-50.4-(-61.7))=29.38/11.3=2.6
    # (-146.22-198.42)/(-61.7-72.7)=-344.64/-134.4=2.564 hmm
    # Mostly slope 2.6. Intercept: 66*2.6=171.6, y=181 -> b=9.4
    # 21.3*2.6=55.38, y=64.78 -> b=9.4
    # 2.9*2.6=7.54, y=16.94 -> b=9.4
    # -6*2.6=-15.6, y=-1.4 -> b=14.2 hmm off
    # -20.3*2.6=-52.78, y=-38.58 -> b=14.2
    # -24.3*2.6=-63.18, y=-48.98 -> b=14.2
    # -50.4*2.6=-131.04, y=-116.84 -> b=14.2
    # -61.7*2.6=-160.42, y=-146.22 -> b=14.2
    # 72.7*2.6=189.02, y=198.42 -> b=9.4
    # 88.2*2.6=229.32, y=238.72 -> b=9.4
    # So b=9.4 for x>=~0, b=14.2 for x<0? Check -6: 14.2 yes.
    # Boundary near 0. At x=0? unknown.
    # Try: f(x)=2.6x+9.4 for x>=0, 2.6x+14.2 for x<0
    # Check -6: 2.6*-6+14.2=-15.6+14.2=-1.4 ✓
    # Check 2.9: 2.6*2.9+9.4=7.54+9.4=16.94 ✓
    # Great fit! But maybe it's a step at 0. Or maybe b depends on sign.
    # Could also be f(x)=2.6x+9.4+4.8*(x<0). 
    # Or maybe f(x)=2.6x+9.4 for x>=0 and 2.6x+14.2 for x<0.
    # Alternatively f(x)=2.6x+9.4+4.8*[x<0].
    # Let's also consider: maybe it's 2.6x+9.4 everywhere but with a floor/step.
    # Actually check x=0 boundary unknown. I'll use x<0 -> +14.2, x>=0 -> +9.4.
    out = []
    for x in probe["x"]:
        try:
            if x < 0:
                y = 2.6 * x + 14.2
            else:
                y = 2.6 * x + 9.4
            out.append(round(y, 2))
        except Exception:
            out.append(None)
    return {"y": out}
