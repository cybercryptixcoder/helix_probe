import math

def predict(probe):
    # Mechanism: f(x) = 4.7*x + 4.25 + 0.0001*x^2 - bump(x), where bump is a
    # narrow even Gaussian centered at 0.
    # - Linear slope ~4.7 [E1, E4, E5, E7]
    # - Additive offset ~4.25 in mid-range [E1, E5, E7]
    # - Quadratic correction 0.0001*x^2 fits large |x| [E1, E4]
    # - Narrow even dip near 0: at x=0 actual is ~3.9155, model base 4.25,
    #   so dip ~0.33 at center [E6, E8]
    # - Dip shape: from E8, deviations from base:
    #   x=0: 3.9155 vs 4.25 -> -0.3345
    #   x=0.01: 3.9719 vs 4.2500 -> -0.278
    #   x=0.03: 4.0841 vs 4.2501 -> -0.166
    #   x=0.1: 4.4652 vs 4.2510 -> +0.214 (above base!)
    #   x=0.18: 4.8931 vs 4.2532 -> +0.640
    #   x=0.25: 5.2658 vs 4.2563 -> +1.010
    #   x=0.45: 6.3306 vs 4.2702 -> +2.060
    #   x=0.6: 7.0798 vs 4.2860 -> +2.794
    #   x=0.9: 8.4665 vs 4.3310 -> +4.135
    #   x=1.2: 9.8779 vs 4.3944 -> +5.484
    #   x=2.2: 14.5914 vs 4.7348 -> +9.857
    # Hmm, this suggests the base linear model is wrong on positive side.
    # Let's reconsider: fit actual data directly.
    # From E8 positive: 0->3.9155, 0.6->7.0798, 1.2->9.8779, 2.2->14.5914
    # Slope 0 to 0.6: (7.0798-3.9155)/0.6 = 5.274
    # Slope 0.6 to 1.2: (9.8779-7.0798)/0.6 = 4.663
    # Slope 1.2 to 2.2: (14.5914-9.8779)/1.0 = 4.714
    # Negative: -0.6->1.6036, -0.9->0.3127, -1.2->-1.3505
    # Slope -0.6 to -0.9: (0.3127-1.6036)/(-0.3) = 4.303
    # Slope -0.9 to -1.2: (-1.3505-0.3127)/(-0.3) = 5.544
    # Asymmetric! Positive side steeper near 0.
    # 
    # Reconsider: maybe f(x) = 4.7*x + 4.25 + 0.0001*x^2 + odd_correction
    # where odd_correction is a smooth step-like feature near 0.
    # At x=0: 3.9155, base 4.25, so correction = -0.3345
    # At x=0.6: 7.0798, base 4.25+2.82+0.000036 = 7.0700, corr = +0.010
    # At x=1.2: 9.8779, base 4.25+5.64+0.000144 = 9.8901, corr = -0.012
    # At x=2.2: 14.5914, base 4.25+10.34+0.000484 = 14.5905, corr = +0.001
    # At x=-0.6: 1.6036, base 4.25-2.82+0.000036 = 1.4300, corr = +0.174
    # At x=-0.9: 0.3127, base 4.25-4.23+0.000081 = 0.0201, corr = +0.293
    # At x=-1.2: -1.3505, base 4.25-5.64+0.000144 = -1.3899, corr = +0.039
    # At x=-0.45: 2.128, base 4.25-2.115+0.00002 = 2.1350, corr = -0.007
    # At x=-0.25: 2.8048, base 4.25-1.175+0.000006 = 3.0750, corr = -0.270
    # At x=-0.18: 3.0678, base 4.25-0.846+0.000003 = 3.4040, corr = -0.336
    # At x=-0.1: 3.4123, base 4.25-0.47 = 3.7800, corr = -0.368
    # At x=-0.03: 3.7539, base 4.25-0.141 = 4.1090, corr = -0.355
    # At x=-0.01: 3.8591, base 4.25-0.047 = 4.2030, corr = -0.344
    # At x=0.01: 3.9719, base 4.25+0.047 = 4.2970, corr = -0.325
    # At x=0.03: 4.0841, base 4.25+0.141 = 4.3910, corr = -0.307
    # At x=0.1: 4.4652, base 4.25+0.47 = 4.7200, corr = -0.255
    # At x=0.18: 4.8931, base 4.25+0.846 = 5.0960, corr = -0.203
    # At x=0.25: 5.2658, base 4.25+1.175 = 5.4250, corr = -0.159
    # At x=0.45: 6.3306, base 4.25+2.115 = 6.3650, corr = -0.034
    # At x=0.6: 7.0798, base 7.0700, corr = +0.010
    # At x=0.9: 8.4665, base 4.25+4.23+0.000081 = 8.4801, corr = -0.014
    # At x=1.2: 9.8779, base 9.8901, corr = -0.012
    # At x=2.2: 14.5914, base 14.5905, corr = +0.001
    #
    # So correction is a localized even-ish dip near 0 (negative on both sides),
    # roughly -0.35 at center, decaying to 0 by |x|~0.5, but slightly asymmetric.
    # Actually it looks fairly even: at +0.1 corr=-0.255, at -0.1 corr=-0.368.
    # At +0.25 corr=-0.159, at -0.25 corr=-0.270.
    # At +0.6 corr=+0.01, at -0.6 corr=+0.174.
    # Hmm, the negative side has larger magnitude dip. Slightly asymmetric.
    # But E6/E7 earlier fit well with even Gaussian -0.33*exp(-(x/0.4)^2).
    # Let's check that against E8:
    # x=0: -0.33, base 4.25 -> 3.92 (actual 3.9155) ok
    # x=0.1: -0.33*exp(-0.0625) = -0.310, base 4.72 -> 4.41 (actual 4.4652) off by 0.055
    # x=0.25: -0.33*exp(-0.39) = -0.224, base 5.425 -> 5.201 (actual 5.2658) off by 0.065
    # x=0.45: -0.33*exp(-1.266) = -0.093, base 6.365 -> 6.272 (actual 6.3306) off by 0.059
    # x=0.6: -0.33*exp(-2.25) = -0.035, base 7.07 -> 7.035 (actual 7.0798) off by 0.045
    # x=-0.1: -0.310, base 3.78 -> 3.47 (actual 3.4123) off by 0.058
    # x=-0.25: -0.224, base 3.075 -> 2.851 (actual 2.8048) off by 0.046
    # x=-0.6: -0.035, base 1.43 -> 1.395 (actual 1.6036) off by 0.209
    # x=-0.9: -0.002, base 0.0201 -> 0.018 (actual 0.3127) off by 0.295
    # x=-1.2: -0.00003, base -1.3899 -> -1.390 (actual -1.3505) off by 0.039
    #
    # So the -0.9 point is an outlier for the even Gaussian model. 
    # Actual -0.9 is 0.3127, model base is 0.0201. Difference +0.293.
    # But at -1.2 actual is -1.3505, base -1.3899, difference +0.039.
    # That's a strange bump at -0.9. Could be noise? Or a real feature.
    # Check E6: x=-1: -0.2396, base 4.25-4.7 = -0.45, diff = +0.21
    # x=-0.75: 1.047, base 4.25-3.525 = 0.725, diff = +0.322
    # x=-0.5: 1.9577, base 4.25-2.35 = 1.90, diff = +0.058
    # x=-1.5: -2.9318, base 4.25-7.05 = -2.80, diff = -0.132
    # x=-2: -5.1471, base 4.25-9.4 = -5.15, diff = +0.003
    # x=-2.5: -7.5056, base 4.25-11.75 = -7.50, diff = -0.006
    # So there's a positive bump around x=-0.75 to -0.9, magnitude ~0.3.
    # And a negative dip at x=0, magnitude ~0.33.
    # 
    # This looks like an odd-ish feature: negative dip at 0, positive bump at -0.8.
    # Could be a derivative-of-Gaussian (odd function) shape.
    # Let's model correction as: -0.33*exp(-(x/0.4)^2) + 0.35*exp(-((x+0.8)/0.35)^2)
    # Check x=-0.9: -0.33*exp(-5.06) + 0.35*exp(-(0.1/0.35)^2) = -0.002 + 0.35*0.921 = 0.320 (actual 0.293) ok
    # x=-0.75: -0.33*exp(-3.52) + 0.35*exp(-(0.05/0.35)^2) = -0.010 + 0.35*0.980 = 0.333 (actual 0.322) ok
    # x=-1: -0.33*exp(-6.25) + 0.35*exp(-(0.2/0.35)^2) = -0.001 + 0.35*0.721 = 0.251 (actual 0.21) ok
    # x=-0.6: -0.33*exp(-2.25) + 0.35*exp(-(0.2/0.35)^2) = -0.035 + 0.251 = 0.216 (actual 0.174) ok-ish
    # x=-0.5: -0.33*exp(-1.5625) + 0.35*exp(-(0.3/0.35)^2) = -0.069 + 0.35*0.480 = 0.099 (actual 0.058) ok
    # x=-1.2: -0.33*exp(-9) + 0.35*exp(-(0.4/0.35)^2) = 0 + 0.35*0.271 = 0.095 (actual 0.039) ok-ish
    # x=-1.5: -0.33*exp(-14) + 0.35*exp(-(0.7/0.35)^2) = 0 + 0.35*0.018 = 0.006 (actual -0.132) hmm off
    # x=-2: 0 + 0.35*exp(-(1.2/0.35)^2) = 0 (actual 0.003) ok
    # x=0: -0.33 + 0.35*exp(-(0.8/0.35)^2) = -0.33 + 0.35*0.0054 = -0.328 (actual -0.3345) ok
    # x=0.1: -0.310 + 0.35*exp(-(0.9/0.35)^2) = -0.310 + 0.35*0.0013 = -0.310 (actual -0.255) off by 0.055
    # x=0.25: -0.224 + 0 = -0.224 (actual -0.159) off by 0.065
    # x=0.45: -0.093 (actual -0.034) off by 0.059
    # x=0.6: -0.035 (actual +0.010) off by 0.045
    # x=0.9: -0.002 (actual -0.014) ok
    # x=1.2: 0 (actual -0.012) ok
    #
    # The positive side dip is a bit too deep. Maybe make the dip narrower or shallower.
    # Try dip amplitude 0.28, width 0.35:
    # x=0: -0.28 + 0.0054*0.35/0.33... let's just use -0.28*exp(-(x/0.35)^2) + 0.35*exp(-((x+0.8)/0.35)^2)
    # x=0: -0.28 + 0.35*0.0054 = -0.278 (actual -0.3345) too shallow
    # 
    # Alternatively, the dip might be asymmetric: deeper on negative side.
    # Let's just use: -0.33*exp(-(x/0.4)^2) for the dip, plus the bump at -0.8.
    # The residual on positive side is ~0.05 which is small.
    # 
    # Actually, let me reconsider. The E8 data has some noise. The match was 0.90.
    # The main errors were at x=-0.9 (0.295 off), x=-0.6 (0.209 off), x=-0.25 (0.046 off).
    # Adding the bump at -0.8 fixes the biggest errors.
    # 
    # Let me also check E6 with the bump:
    # x=-0.75: base 0.725, dip -0.010, bump 0.333 -> 1.048 (actual 1.047) 
    # x=-0.5: base 1.90, dip -0.069, bump 0.099 -> 1.930 (actual 1.9577) ok
    # x=-1: base -0.45, dip -0.001, bump 0.251 -> -0.200 (actual -0.2396) ok
    # x=-1.5: base -2.80, dip 0, bump 0.006 -> -2.794 (actual -2.9318) off by 0.14
    # x=-2: base -5.15, dip 0, bump 0 -> -5.15 (actual -5.1471) ok
    # x=0.5: base 6.60, dip -0.069, bump 0 -> 6.531 (actual 6.5856) ok
    # x=0.75: base 7.775, dip -0.010, bump 0 -> 7.765 (actual 7.7752) ok
    # x=1: base 8.95, dip -0.001, bump 0 -> 8.949 (actual 8.9349) ok
    # x=1.5: base 11.30, dip 0, bump 0 -> 11.30 (actual 11.2924) ok
    # x=2: base 13.65, dip 0, bump 0 -> 13.65 (actual 13.6499) ok
    # x=2.5: base 16.00, dip 0, bump 0 -> 16.00 (actual 16.0022) ok
    # x=3.5: base 20.70, dip 0, bump 0 -> 20.70 (actual 20.7114) ok
    # x=4: base 23.05, dip 0, bump 0 -> 23.05 (actual 23.0684) ok
    # x=-2.5: base -7.50, dip 0, bump 0 -> -7.50 (actual -7.5056) ok
    # 
    # Good. Let's also check E7:
    # x=-0.4: base 4.25-1.88 = 2.37, dip -0.33*exp(-1) = -0.121, bump 0.35*exp(-(0.4/0.35)^2) = 0.35*0.271 = 0.095 -> 2.344 (actual 2.2982) ok
    # x=-0.35: base 4.25-1.645 = 2.605, dip -0.33*exp(-0.766) = -0.153, bump 0.35*exp(-(0.45/0.35)^2) = 0.35*0.192 = 0.067 -> 2.519 (actual 2.4672) ok
    # x=-0.2: base 4.25-0.94 = 3.31, dip -0.33*exp(-0.25) = -0.257, bump 0.35*exp(-(0.6/0.35)^2) = 0.35*0.053 = 0.019 -> 3.072 (actual 2.9898) ok
    # x=-0.12: base 4.25-0.564 = 3.686, dip -0.33*exp(-0.09) = -0.302, bump 0.35*exp(-(0.68/0.35)^2) = 0.35*0.023 = 0.008 -> 3.392 (actual 3.3237) ok
    # x=-0.08: base 4.25-0.376 = 3.874, dip -0.33*exp(-0.04) = -0.317, bump 0.35*exp(-(0.72/0.35)^2) = 0.35*0.014 = 0.005 -> 3.562 (actual 3.5007) ok
    # x=0.08: base 4.25+0.376 = 4.626, dip -0.317, bump 0 -> 4.309 (actual 4.3563) ok
    # x=0.12: base 4.814, dip -0.302, bump 0 -> 4.512 (actual 4.5737) ok
    # x=0.2: base 5.19, dip -0.257, bump 0 -> 4.933 (actual 4.9996) ok
    # x=0.35: base 5.895, dip -0.153, bump 0 -> 5.742 (actual 5.7982) ok
    # x=0.4: base 6.13, dip -0.121, bump 0 -> 6.009 (actual 6.0644) ok
    # 
    # All within ~0.06. Good.
    # 
    # So the model is:
    # f(x) = 4.7*x + 4.25 + 0.0001*x^2 - 0.33*exp(-(x/0.4)^2) + 0.35*exp(-((x+0.8)/0.35)^2)
    # 
    # The bump at -0.8 is an odd-ish feature. It's a localized positive bump on the negative side.
    # This is a real feature (not noise) since it appears in both E6 and E8.
    # 
    # Let me double check the large-x behavior with this model. The bump and dip are localized near 0, so they don't affect large x. Good.
    # 
    # Let me also verify E1 and E2 aren't broken. The corrections are tiny at large |x|.
    # 
    # Final model.

    x = probe["x"]
    out = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            out.append(None)
            continue
        val = (4.7*v + 4.25 + 0.0001*v*v
               - 0.33*math.exp(-(v/0.4)**2)
               + 0.35*math.exp(-((v+0.8)/0.35)**2))
        out.append(round(val, 4))
    return {"y": out}
