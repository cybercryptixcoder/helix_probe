import math

def predict(probe):
    # Model hypotheses (v2):
    # - Ordinary range: f(x) = c * x^5 with c ≈ 0.1139 for x>0 and c ≈ -0.1139 for x<0 [E6]
    #   Check E6: 10^5*0.1139=11390000 ✓ (obs 11386930); 120^5*0.1139≈2.83e12 ✓; -120^5*(-0.1139)≈-8.54e11 ✓
    #   Check E5: 102.1^5*0.1139≈1.26e12 ✓; -102.2^5*(-0.1139)≈-3.83e11 ✓
    #   Check E3: 123.6^5*0.1139≈3.28e12 ✓; -63.9^5*(-0.1139)≈-3.67e10 ✓
    #   Check E1: 88.2^5*0.1139≈6.07e11 ✓; -61.7^5*(-0.1139)≈-3.08e10 ✓
    # - The coefficient is the SAME magnitude both signs: c=0.1139, sign follows x^5 (odd function) [E6]
    # - Special interval near zero (|x| ≲ 1.0) with a different small-amplitude behavior [E2,E4]
    #   Anchors from E2/E4; smooth bump, sign-asymmetric.
    # - Boundary: at |x|=1.2 the x^5 term already fits (249.2 = 1.2^5*0.1139*... check: 1.2^5*0.1139≈0.283, no)
    #   Actually 1.2^5*0.1139≈0.283, but obs 249.2. So special interval extends past 1.2? Recheck:
    #   1.2^5=2.488, *0.1139=0.283. Obs 249.2. So |x|=1.2 is NOT pure power law.
    #   Hmm, but 1.5^5*0.1139=0.865, obs 867.67 -> ratio 1003. So there's a scale factor issue.
    #   Let me recompute c from E6: 10^5*c=11386930 -> c=1.138693. 120^5=2.48832e10, *1.138693=2.833e10? No, 2.83e10 not 2.83e12.
    #   Wait: 120^5 = 2.48832e10. Obs 2.831879e12. Ratio = 113.8. So c=113.8? Then 10^5*113.8=1.138e7 ✓.
    #   So c ≈ 113.87, not 0.1139! Fix: c=113.87.
    #   Check E1: 88.2^5=5.34e9, *113.87=6.08e11 ✓. -61.7^5=-8.94e8, *113.87=-1.018e11? obs -3.08e10. Hmm.
    #   -61.7^5: 61.7^2=3806.89, ^4=1.449e7, *61.7=8.94e8. *113.87=1.018e11. Obs -3.08e10. Ratio 0.30.
    #   So negative side has different coefficient? E6: -120^5=-2.488e10, obs -8.537e11, ratio 34.3. 
    #   Positive 120: ratio 113.8. So sign-dependent coefficient: c+≈113.87, c-≈34.3? 
    #   Check E6 -10: -10^5=-1e5, obs -3613823, ratio 36.1. -20: -3.2e6, obs -1.123e8, ratio 35.1.
    #   -40: -1.024e8, obs -3.545e9, ratio 34.6. -60: -7.776e8, obs -2.68e10, ratio 34.5.
    #   -80: -3.277e9, obs -1.127e11, ratio 34.4. -100: -1e10, obs -3.434e11, ratio 34.3.
    #   So c- ≈ 34.4 (slightly decreasing). Positive: 10:113.87, 20:113.7, 40:113.7, 60:113.7, 80:113.7, 100:113.8, 120:113.8. c+≈113.7.
    #   Hmm but E1 -61.7 gave ratio 0.30*113.87=34.2 ✓ consistent with c-=34.4.
    #   E5 -102.2: -102.2^5=-1.115e10, obs -3.828e11, ratio 34.3 ✓.
    #   E3 -63.9: -63.9^5=-1.065e9, obs -3.669e10, ratio 34.5 ✓.
    #   E4 -8: -32768, obs -1202334, ratio 36.7. -6: -7776, obs -292914, ratio 37.7. -5:-3125,obs -120306,ratio 38.5.
    #   -4.5: -1845, obs -72100, ratio 39.1. -3.5: -525, obs -21429, ratio 40.8. -2.5: -97.66, obs -4307, ratio 44.1.
    #   -1.5: -7.59, obs -380.9, ratio 50.2. So c- grows toward small |x| — special interval blending.
    #   Positive small: 1.5^5=7.59, obs 867.67, ratio 114.3. 2.5^5=97.66, obs 11499, ratio 117.7.
    #   3.5^5=525.2, obs 61001, ratio 116.2. So c+≈114-117 near small, ~113.7 large.
    #   So c+ ≈ 114, c- ≈ 34.4 in ordinary range. Special interval |x| < ~1.
    # - Special interval anchors from E2/E4 (|x| < 1.0):
    anchors = [
        (-1.0, -37.091), (-0.8, 5.8605), (-0.6, 22.3562), (-0.5, 26.692),
        (-0.3, 27.3822), (-0.25, 27.77), (-0.1, 23.8483), (0.0, 21.28),
        (0.1, 11.4473), (0.25, -3.2851), (0.3, -7.9163), (0.5, -22.9553),
        (0.6, -24.6466), (0.8, -3.3302), (1.0, 70.35),
    ]

    def special(x):
        if x <= anchors[0][0]:
            return anchors[0][1]
        if x >= anchors[-1][0]:
            return anchors[-1][1]
        for i in range(len(anchors) - 1):
            x0, y0 = anchors[i]
            x1, y1 = anchors[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return 0.0

    def power(x):
        c = 114.0 if x >= 0 else 34.4
        return c * (x ** 5)

    ys = []
    for x in probe.get("x", []):
        if x is None:
            ys.append(None)
            continue
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if abs(x) < 1.0:
            ys.append(special(x))
        else:
            ys.append(power(x))
    return {"y": ys}
