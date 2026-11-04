import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Observations:
    # - For large |x| the function is roughly linear with slope ~ -16.8 per unit x,
    #   passing near 0 at x=0.  [E1,E2,E3,E5]
    # - For x in roughly (-0.5, 0.5) there is a smooth "bump" region where f is
    #   positive and slowly varying, peaking near x=0 (~5.4) and dropping to ~0
    #   near x=±0.5.  [E4,E6]
    # - Outside that central interval the function is linear-ish: f(x) ≈ -16.8*x
    #   with a small offset.  [E2,E3,E5]
    # - There is a sharp transition at |x|≈0.5: at x=0.5 f≈0.87, at x=0.6 f≈0.87
    #   then continues linearly downward.  [E6]
    # - The function appears odd-ish? No: f(-x) ≠ -f(x) in the bump region
    #   (f(0)=5.42, f(-0.5)=6.84, f(0.5)=0.87).  So bump is asymmetric.
    # - Outside the bump, f(x) ≈ -16.8*x + small offset.  [E2: f(10)=-157.8,
    #   f(-10)=70.0; slope from 10 to 80: (-1340.8+157.8)/70 = -16.9]
    # - The bump region seems to be |x| < ~0.5, with a transition zone.

    x = probe["x"]
    ys = []
    for v in x:
        try:
            ys.append(_f(float(v)))
        except Exception:
            ys.append(None)
    return {"y": ys}


def _f(x):
    # Central bump region: |x| < 0.5
    # From E4/E6: f(0)=5.4186, f(0.1)=5.1041, f(0.2)=4.6858, f(0.3)=4.0718,
    # f(0.4)=3.2125, f(0.5)=0.8742 (transition)
    # Negative side: f(-0.1)=5.704, f(-0.2)=5.9894, f(-0.3)=6.2748,
    # f(-0.4)=6.5602, f(-0.5)=6.8447
    # So bump is roughly quadratic-ish on each side, asymmetric.
    # Outside: linear with slope ~ -16.8, offset ~ 0.
    # Fit linear outside using E2: f(10)=-157.8063 => slope*10+b = -157.8063
    # f(80)=-1340.7979 => slope*80+b = -1340.7979
    # slope = (-1340.7979+157.8063)/70 = -16.8999
    # b = -157.8063 + 168.999 = 11.19
    # Check f(-10) = 168.999+11.19 = 180? No, actual 69.99. So not same line.
    # Negative side: f(-10)=69.9949, f(-80)=543.2006
    # slope = (543.2006-69.9949)/(-70) = -6.7601
    # Hmm asymmetric slopes.
    # Wait check: f(-80)=543.2, f(-10)=70.0 => slope = (543.2-70)/(-80+10)= 473.2/-70 = -6.76
    # Positive side slope -16.9. So asymmetric linear.
    # At x=0 extrapolating positive line: 11.19; negative line: 69.99 - 6.76*10 = 2.39? 
    # f(-10)=69.9949, slope -6.76 => b = 69.9949+67.6=137.6? No.
    # Let's recompute: f(-10)=69.9949, f(-80)=543.2006.
    # slope = (543.2006-69.9949)/(-80-(-10)) = 473.2057/(-70) = -6.7601
    # b = 69.9949 - (-6.7601)*(-10) = 69.9949 - 67.601 = 2.394
    # So negative line: f(x) = -6.76*x + 2.39
    # Positive line: f(x) = -16.9*x + 11.19
    # Check f(1) from E2 = -5.3245. Positive line: -16.9+11.19=-5.71 close.
    # f(5) = -73.2881. Positive line: -84.5+11.19=-73.31 good.
    # f(-1)=9.3469. Negative line: 6.76+2.39=9.15 close.
    # f(-5)=36.1945. Negative line: 33.8+2.39=36.19 good!
    # So outside bump: positive side slope -16.9, negative side slope -6.76.
    # Bump region |x| < 0.5: smooth curve.
    # At x=0.5 f=0.8742, x=0.6 f=0.8742 (same!). Interesting.
    # E6: f(0.4)=3.2125, f(0.5)=0.8742, f(0.6)=0.8742, f(0.8)=-2.1698
    # Positive line at 0.6: -16.9*0.6+11.19=-10.14+11.19=1.05, but actual 0.8742.
    # At 0.8: -13.52+11.19=-2.33 vs actual -2.1698.
    # At 1.0: -16.9+11.19=-5.71 vs actual -5.3245.
    # So positive line is approximate, actual slightly different.
    # Let's fit positive line from E2 points 1,5,10,20,...,80.
    # f(1)=-5.3245, f(80)=-1340.7979
    # slope = (-1340.7979+5.3245)/79 = -16.9047
    # b = -5.3245+16.9047 = 11.5802
    # Check f(10): -169.047+11.58=-157.47 vs -157.8063 close.
    # Check f(20): -338.09+11.58=-326.51 vs -326.8051 close.
    # OK positive line: f(x) ≈ -16.905*x + 11.58
    # Negative line from E2: f(-1)=9.3469, f(-80)=543.2006
    # slope = (543.2006-9.3469)/(-79) = -6.7589
    # b = 9.3469 - (-6.7589)*(-1) = 9.3469-6.7589=2.588
    # Check f(-10): 67.589+2.588=70.177 vs 69.9949 close.
    # So negative line: f(x) ≈ -6.759*x + 2.588

    # Bump region: |x| <= 0.5
    # Positive: f(0)=5.4186, f(0.1)=5.1041, f(0.2)=4.6858, f(0.3)=4.0718,
    # f(0.4)=3.2125, f(0.5)=0.8742
    # This looks like a smooth curve, maybe cosine or quadratic.
    # Differences: -0.3145, -0.4183, -0.614, -0.8593, -2.3383
    # Accelerating drop near 0.5.
    # Negative: f(0)=5.4186, f(-0.1)=5.704, f(-0.2)=5.9894, f(-0.3)=6.2748,
    # f(-0.4)=6.5602, f(-0.5)=6.8447
    # Differences: +0.2854, +0.2854, +0.2854, +0.2854, +0.2845
    # Almost perfectly linear on negative side! slope ~ -2.854 per unit x (i.e., f increases as x decreases)
    # So for -0.5<=x<=0: f(x) = 5.4186 - 2.854*x
    # Check f(-0.5)=5.4186+1.427=6.8456 vs 6.8447 good.
    # For positive side 0<=x<=0.5: not linear. Maybe quadratic?
    # f(x) = a + b*x + c*x^2
    # f(0)=5.4186 => a=5.4186
    # f(0.2)=4.6858 => 5.4186+0.2b+0.04c=4.6858 => 0.2b+0.04c=-0.7328
    # f(0.4)=3.2125 => 5.4186+0.4b+0.16c=3.2125 => 0.4b+0.16c=-2.2061
    # Multiply first by 2: 0.4b+0.08c=-1.4656
    # Subtract: 0.08c = -0.7405 => c=-9.256
    # 0.2b = -0.7328-0.04*(-9.256)=-0.7328+0.3702=-0.3626 => b=-1.813
    # Check f(0.1): 5.4186-0.1813-0.09256=5.1447 vs 5.1041 close.
    # f(0.3): 5.4186-0.5439-0.833=4.0417 vs 4.0718 close.
    # f(0.5): 5.4186-0.9065-2.314=2.198 vs 0.8742 not great.
    # Maybe cubic or the transition at 0.5 is sharp.
    # Actually E6 shows f(0.5)=0.8742 and f(0.6)=0.8742, suggesting a plateau
    # or the bump ends at 0.5 and then linear resumes.
    # At x=0.5 positive line gives -16.905*0.5+11.58=3.13, actual 0.874.
    # At x=0.6 line gives 1.04, actual 0.874.
    # At x=0.8 line gives -1.94, actual -2.17.
    # So maybe positive line is slightly different. Let's fit from x>=1.
    # Actually maybe the bump extends to 0.5 and then linear from 0.5.
    # Let's use: for x>0.5, f(x) = -16.905*x + 11.58 (approx)
    # But f(0.5) actual 0.874, line gives 3.13. Discontinuity?
    # E6: f(0.5)=0.8742, f(0.6)=0.8742. That's suspicious - maybe noise or
    # the function has a flat spot. Let's just use smooth interpolation.
    # Given uncertainty, use piecewise:
    # x < -0.5: negative line: -6.759*x + 2.588
    # -0.5 <= x <= 0: 5.4186 - 2.854*x
    # 0 < x <= 0.5: quadratic 5.4186 - 1.813*x - 9.256*x^2
    # x > 0.5: positive line: -16.905*x + 11.58
    # But need continuity at 0.5: quadratic gives 2.198, line gives 3.13.
    # E6 says 0.874. Hmm.
    # Let's check E4: f(0.4)=3.2125, f(0.6)=0.8742. Big drop.
    # Maybe there's a sharp transition at 0.5.
    # Let's just use the quadratic up to 0.5 and then linear from 0.5 with
    # a jump? No, better to blend.
    # Given the MLP approximation, likely smooth. Let's use a sigmoid transition.
    # Simplest: use the observed values as anchor and interpolate linearly
    # between them for the bump region, and linear outside.
    # But must generalize.

    # Let's define anchor points from evidence and interpolate.
    # Actually, let's just build a piecewise linear model from the data points
    # we have, which should generalize reasonably.

    # Anchor points (x, f(x)) from E2,E4,E6:
    anchors = [
        (-80, 543.2006), (-70, 475.5998), (-60, 407.999), (-50, 340.3982),
        (-40, 272.7973), (-30, 205.1965), (-20, 137.5957), (-10, 69.9949),
        (-5, 36.1945), (-3, 22.6743), (-2.5, 19.2942), (-2, 15.9142),
        (-1.5, 12.5417), (-1.2, 10.5797), (-1, 9.3469), (-0.7, 7.6317),
        (-0.5, 6.8447), (-0.4, 6.5602), (-0.3, 6.2748), (-0.2, 5.9894),
        (-0.1, 5.704), (-0.05, 5.5613), (0, 5.4186), (0.05, 5.2759),
        (0.1, 5.1041), (0.15, 4.9028), (0.2, 4.6858), (0.25, 4.4171),
        (0.3, 4.0718), (0.35, 3.6502), (0.4, 3.2125), (0.5, 0.8742),
        (0.6, 0.8742), (0.8, -2.1698), (1, -5.3245), (1.2, -8.5666),
        (1.5, -13.7572), (2, -22.6804), (2.5, -31.1292), (3, -39.4742),
        (5, -73.2881), (7, -107.1067), (10, -157.8063), (20, -326.8051),
        (30, -495.8039), (40, -664.8027), (50, -833.8015), (60, -1002.8003),
        (70, -1171.7991), (80, -1340.7979),
        # From E1,E3,E5
        (2.9, -37.7888), (21.3, -348.775), (72.7, -1217.4288),
        (-6.0, 42.9545), (-20.3, 139.6237), (-24.3, 166.664),
        (-50.4, 343.1022), (-61.7, 419.4911), (66.0, -1104.1996),
        (88.2, -1479.3769), (104.5, -1754.845), (1.2, -8.5666),
        (-55.8, 379.6066), (65.5, -1095.7497), (30.3, -500.8739),
        (-63.9, 434.3633), (104.9, -1761.6049), (123.6, -2077.6327),
        (79.4, -1330.658), (103.0, -1729.4951),
        (-48.6, 330.934), (58.8, -982.5205), (102.1, -1714.2852),
        (47.1, -784.7919), (-7.1, 50.3906), (-102.2, 693.2744),
        (-16.9, 116.6394), (28.4, -468.7641), (105.7, -1775.1248),
        (119.5, -2008.3431),
    ]
    anchors.sort()

    # For x outside anchor range, extrapolate linearly.
    if x <= anchors[0][0]:
        x0, y0 = anchors[0]
        x1, y1 = anchors[1]
        slope = (y1 - y0) / (x1 - x0)
        return y0 + slope * (x - x0)
    if x >= anchors[-1][0]:
        x0, y0 = anchors[-2]
        x1, y1 = anchors[-1]
        slope = (y1 - y0) / (x1 - x0)
        return y1 + slope * (x - x1)

    # Linear interpolation between anchors
    for i in range(len(anchors) - 1):
        x0, y0 = anchors[i]
        x1, y1 = anchors[i + 1]
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return None
