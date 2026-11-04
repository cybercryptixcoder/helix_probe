import math

def predict(probe):
    # Beliefs:
    # f(x) is a cubic-like polynomial for |x| <= ~64? Let's test.
    # E1: x=2.9 -> -1326.98 ; x=-6.0 -> 197.22 ; x=21.3 -> -8764.26
    # E2: x=1.2 -> -639.84 ; x=30.3 -> -12402.06
    # Check simple cubic: a*x^3 + b*x^2 + c*x + d
    # Use points: (2.9,-1326.98),(1.2,-639.84),(-6.0,197.22),(21.3,-8764.26)
    # Try to fit. Let's solve mentally? Instead, notice:
    # x=88.2 -> -35805.24 ; 88.2^3 = 686128.968 ; -35805.24/686128.968 ≈ -0.05218
    # x=66.0 -> -26832.0 ; 66^3=287496 ; ratio -0.0933
    # x=72.7 -> -29540.14 ; 72.7^3=384240.583 ; ratio -0.07688
    # Not pure cubic.
    # Try quadratic: x=88.2^2=7779.24 ; -35805.24/7779.24=-4.602
    # x=66^2=4356 ; -26832/4356=-6.16
    # Hmm.
    # Look at negative x: -20.3 -> 708.016 ; -61.7 -> 2186.824 ; -50.4 -> 1783.188
    # -24.3 -> 850.896 ; -6.0 -> 197.22 ; -55.8 -> 1976.076 ; -63.9 -> 2265.408
    # For negative x, y positive and roughly linear in |x|? 
    # -20.3: 708.016/20.3=34.877 ; -61.7: 2186.824/61.7=35.443 ; -50.4: 1783.188/50.4=35.381
    # -24.3: 850.896/24.3=35.016 ; -55.8: 1976.076/55.8=35.413 ; -63.9: 2265.408/63.9=35.453
    # -6.0: 197.22/6=32.87 (slightly off)
    # So for x<0: y ≈ 35.4 * |x|? But -6 gives 197.22 vs 212.4. Hmm.
    # Check x=-6: maybe y = -35.4*x + something? -35.4*(-6)=212.4, actual 197.22. 
    # Try y = a*x^2 + b*x? For x=-6: 36a - 6b = 197.22
    # x=-20.3: 412.09a -20.3b = 708.016
    # Solve: from first, b = (36a - 197.22)/6 = 6a - 32.87
    # 412.09a - 20.3(6a-32.87) = 708.016
    # 412.09a - 121.8a + 667.261 = 708.016
    # 290.29a = 40.755 => a=0.14039, b=6*0.14039-32.87=-32.0276
    # Check x=-61.7: 0.14039*3806.89 + (-32.0276)*(-61.7) = 534.4 + 1976.1 = 2510.5, actual 2186.8. Not great.
    # Try y = a*|x| + b for x<0: 
    # Using -20.3 and -61.7: slope = (2186.824-708.016)/(61.7-20.3)=1478.808/41.4=35.72
    # intercept: 708.016 - 35.72*20.3 = 708.016-725.116=-17.1
    # Check -50.4: 35.72*50.4-17.1=1800.3-17.1=1783.2 ✓ (actual 1783.188)
    # Check -24.3: 35.72*24.3-17.1=867.996-17.1=850.896 ✓
    # Check -55.8: 35.72*55.8-17.1=1993.176-17.1=1976.076 ✓
    # Check -63.9: 35.72*63.9-17.1=2282.508-17.1=2265.408 ✓
    # Check -6.0: 35.72*6-17.1=214.32-17.1=197.22 ✓
    # So for x<0: y = 35.72*|x| - 17.1 = -35.72*x - 17.1
    # For x>0: looks like y = a*x^2 + b*x + c? 
    # Use x=2.9 -> -1326.98 ; x=21.3 -> -8764.26 ; x=30.3 -> -12402.06
    # Try quadratic: 
    # 8.41a+2.9b+c=-1326.98
    # 453.69a+21.3b+c=-8764.26
    # 918.09a+30.3b+c=-12402.06
    # Subtract: 445.28a+18.4b=-7437.28 => 24.2a+b=-404.2 (divide by 18.4)
    # 464.4a+9b=-3637.8 => 51.6a+b=-404.2 (divide by 9)
    # So 24.2a+b=-404.2 and 51.6a+b=-404.2 => 27.4a=0 => a=0, b=-404.2
    # Then c: 8.41*0+2.9*(-404.2)+c=-1326.98 => -1172.18+c=-1326.98 => c=-154.8
    # Check x=1.2: -404.2*1.2-154.8=-485.04-154.8=-639.84 ✓
    # Check x=66: -404.2*66-154.8=-26677.2-154.8=-26832.0 ✓
    # Check x=88.2: -404.2*88.2-154.8=-35650.44-154.8=-35805.24 ✓
    # Check x=72.7: -404.2*72.7-154.8=-29385.34-154.8=-29540.14 ✓
    # Check x=104.5: -404.2*104.5-154.8=-42238.9-154.8=-42393.7 ✓
    # Check x=104.9: -404.2*104.9-154.8=-42400.58-154.8=-42555.38 ✓
    # Check x=123.6: -404.2*123.6-154.8=-49959.12-154.8=-50113.92 ✓
    # Check x=79.4: -404.2*79.4-154.8=-32093.48-154.8=-32248.28 ✓
    # Check x=103.0: -404.2*103-154.8=-41632.6-154.8=-41787.4 ✓
    # Check x=65.5: -404.2*65.5-154.8=-26475.1-154.8=-26629.9 ✓
    # Check x=30.3: -404.2*30.3-154.8=-12247.26-154.8=-12402.06 ✓
    # So for x>=0: y = -404.2*x - 154.8
    # For x<0: y = -35.72*x - 17.1
    # Wait, check x=0? Both give -154.8 vs -17.1. There's a discontinuity at 0.
    # Need to determine which side 0 belongs to. E1 has x=2.9 (positive) and x=-6.0 (negative).
    # No x=0 in evidence. The transition might be at x=0, or somewhere else.
    # Check if there's a region where behavior changes. Both formulas are linear.
    # Maybe the split is at some threshold, not 0.
    # Let's see: positive side formula works for x=1.2 (positive). Negative side for x=-6.0 (negative).
    # Is there a boundary? Maybe at x=0. 
    # But wait: what about x between -6 and 1.2? Unknown. 
    # Could be the split is at x=0. Let's assume x>=0 uses -404.2x-154.8, x<0 uses -35.72x-17.1.
    # Check continuity? At x=0: -154.8 vs -17.1, jump. So discontinuous at 0.
    # Alternatively, maybe the split is at some other point. But evidence only has positive and negative.
    # Could be the function is: if x<0: -35.72x-17.1; else: -404.2x-154.8.
    # Let's verify all points:
    # E1: 88.2 -> -404.2*88.2-154.8 = -35650.44-154.8 = -35805.24 ✓
    # 66.0 -> -26677.2-154.8 = -26832.0 ✓
    # -20.3 -> -35.72*(-20.3)-17.1 = 725.116-17.1 = 708.016 ✓
    # -61.7 -> -35.72*(-61.7)-17.1 = 2203.924-17.1 = 2186.824 ✓
    # 2.9 -> -404.2*2.9-154.8 = -1172.18-154.8 = -1326.98 ✓
    # -24.3 -> -35.72*(-24.3)-17.1 = 867.996-17.1 = 850.896 ✓
    # 72.7 -> -404.2*72.7-154.8 = -29385.34-154.8 = -29540.14 ✓
    # -50.4 -> -35.72*(-50.4)-17.1 = 1800.288-17.1 = 1783.188 ✓
    # -6.0 -> -35.72*(-6.0)-17.1 = 214.32-17.1 = 197.22 ✓
    # 21.3 -> -404.2*21.3-154.8 = -8609.46-154.8 = -8764.26 ✓
    # E2: 104.5 -> -404.2*104.5-154.8 = -42238.9-154.8 = -42393.7 ✓
    # 1.2 -> -404.2*1.2-154.8 = -485.04-154.8 = -639.84 ✓
    # -55.8 -> -35.72*(-55.8)-17.1 = 1993.176-17.1 = 1976.076 ✓
    # 65.5 -> -404.2*65.5-154.8 = -26475.1-154.8 = -26629.9 ✓
    # 30.3 -> -404.2*30.3-154.8 = -12247.26-154.8 = -12402.06 ✓
    # -63.9 -> -35.72*(-63.9)-17.1 = 2282.508-17.1 = 2265.408 ✓
    # 104.9 -> -404.2*104.9-154.8 = -42400.58-154.8 = -42555.38 ✓
    # 123.6 -> -404.2*123.6-154.8 = -49959.12-154.8 = -50113.92 ✓
    # 79.4 -> -404.2*79.4-154.8 = -32093.48-154.8 = -32248.28 ✓
    # 103.0 -> -404.2*103-154.8 = -41632.6-154.8 = -41787.4 ✓
    # All match exactly. So the model is:
    # if x < 0: y = -35.72*x - 17.1
    # else: y = -404.2*x - 154.8
    # The boundary at 0 is a guess (no evidence for x=0 exactly). Could be boundary at 0.
    # The problem mentions "There may be an interval inside the domain where the function behaves differently"
    # Here the two regions are x<0 and x>=0. The boundary is at 0.
    # We'll assume x>=0 uses the positive formula.
    # Also note: the coefficients might be exact fractions? -35.72 = -893/25? -404.2 = -2021/5? -17.1 = -171/10, -154.8 = -774/5.
    # But we'll use floats.
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xf = float(x)
            if xf < 0:
                y = -35.72 * xf - 17.1
            else:
                y = -404.2 * xf - 154.8
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
