def predict(probe):
    # Model: f(x) = x^5 (fifth power). Evidence [E1]:
    #   (-1.2)^5 = -2.48832... but observed -11.8166 -> not x^5.
    # Try x^5 * something? Check ratios.
    # Let's test x^5:
    #   (-93.6)^5 = -7.18e9, observed 1.48e12 -> ratio ~ -206
    #   (-1.2)^5 = -2.488, observed -11.8166 -> ratio ~ 4.75
    # Not constant. Try x^6? sign wrong for negatives.
    # Observed signs: negative x -> positive y (for -93.6,-62.7,-104,-120.7),
    #   but -1.2 -> negative, -12.9 -> positive.
    # Hmm -1.2 gives -11.8166, -12.9 gives +9.88e6.
    # Try x^5 * x = x^6? (-1.2)^6=2.986 positive, no.
    # Try x^7? (-1.2)^7=-3.58, observed -11.8. ratio 3.3
    # (-12.9)^7 = -6.0e7, observed +9.9e6. sign mismatch.
    # Let's compute x^5 for each and compare:
    #   x=-93.6: x^5=-7.18e9, y=1.48e12
    #   x=88.9: x^5=5.55e9, y=1.08e12
    #   x=67.5: x^5=1.40e9, y=2.07e11
    #   x=-62.7: x^5=-9.69e8, y=1.34e11
    #   x=-1.2: x^5=-2.488, y=-11.8166
    #   x=-12.9: x^5=-3.57e5, y=9.89e6
    #   x=38.8: x^5=8.79e7, y=7.39e9
    #   x=73.9: x^5=2.20e9, y=3.55e11
    #   x=-104: x^5=-1.22e10, y=2.80e12
    #   x=-120.7: x^5=-2.56e10, y=6.81e12
    # Ratios y/x^5:
    #   -93.6: -206.2
    #   88.9: 194.1
    #   67.5: 147.9
    #   -62.7: -138.2
    #   -1.2: 4.75
    #   -12.9: -27.7
    #   38.8: 84.1
    #   73.9: 161.4
    #   -104: -229.5
    #   -120.7: -266.0
    # Ratios ~ proportional to x? ratio/x:
    #   -93.6: 2.203
    #   88.9: 2.184
    #   67.5: 2.191
    #   -62.7: 2.204
    #   -1.2: -3.96  <- outlier
    #   -12.9: 2.147
    #   38.8: 2.168
    #   73.9: 2.184
    #   -104: 2.207
    #   -120.7: 2.204
    # So y ~ 2.2 * x^6 for |x| large. Check x=-1.2: 2.2*2.986=6.57, observed -11.8. Sign wrong!
    # x=-12.9: 2.2*4.6e6=1.01e7, observed 9.89e6. Close (2.15*x^6).
    # So for |x|>~2, y ~ 2.2*x^6? But -1.2 gives negative.
    # Wait x^6 always positive. -1.2 -> -11.8 is negative. So not x^6.
    # Reconsider: maybe y = 2.2*x^5*|x|? = 2.2*x^6*sign(x)? For -1.2: 2.2*2.986*(-1)=-6.57, still not -11.8.
    # Try y = x^5 * (2.2*x + something)? For -1.2: x^5=-2.488, y=-11.8 -> factor 4.75.
    # 2.2*x = -2.64, +? = 4.75 -> ? = 7.39. Hmm.
    # Actually maybe y = x^5*(2.2x) + small term. For -1.2: 2.2*(-1.2)*(-2.488)=6.57 positive, no.
    # Let's try y = 2.2*x^6 + correction. -1.2: 6.57 vs -11.8. diff -18.4.
    # Maybe there's a region near 0 behaving differently (the "interval").
    # For |x|>=~10, y ≈ 2.2*x^6 with sign... but x^6 positive and all large-|x| y positive. Yes all large |x| give positive y. Good, x^6.
    # Check exact: 2.2*x^6 for x=-93.6: 2.2*6.72e11=1.478e12 vs 1.4817e12. ratio 2.205.
    # x=88.9: x^6=4.93e11, *2.2=1.085e12 vs 1.0775e12. ratio 2.185.
    # Slight variation. Maybe coefficient is exactly? Let's fit: y/x^6:
    #   -93.6: 2.2053
    #   88.9: 2.1853
    #   67.5: 2.1911
    #   -62.7: 2.2046
    #   -12.9: 2.1476
    #   38.8: 2.1680
    #   73.9: 2.1843
    #   -104: 2.2074
    #   -120.7: 2.2042
    # Not constant; varies with |x|. Larger |x| -> ~2.205, smaller -> less.
    # Maybe y = 2.2*x^6 + lower order? Try y = 2.2*x^6 + a*x^5 + ...
    # Or y = x^5*(2.2x + c). y/x^5 = 2.2x + c:
    #   -93.6: -206.2 = 2.2*(-93.6)+c = -205.9+c -> c=-0.3
    #   88.9: 194.1 = 195.6+c -> c=-1.5
    #   67.5: 147.9 = 148.5+c -> c=-0.6
    #   -62.7: -138.2 = -137.9+c -> c=-0.3
    #   -12.9: -27.7 = -28.4+c -> c=0.7
    #   38.8: 84.1 = 85.4+c -> c=-1.3
    #   73.9: 161.4 = 162.6+c -> c=-1.2
    #   -104: -229.5 = -228.8+c -> c=-0.7
    #   -120.7: -266.0 = -265.5+c -> c=-0.5
    # c roughly -0.5 to -1.5, noisy. Maybe y = 2.2*x^6 - x^5? c=-1.
    # Check -1.2: 2.2*x^6 - x^5 = 6.57 - (-2.488)=9.06, observed -11.8. No.
    # The -1.2 point is the outlier. Maybe region |x|<2 differs.
    # For -1.2: y=-11.8166. x^5=-2.488. y/x^5=4.75. Hmm 4.75 ~ ? 
    # Maybe y=x^5*(2.2x-1) for large, but near 0 different.
    # Actually maybe the function is x^5*(2.2x) + x^5*(-1)?? = 2.2x^6 - x^5.
    # For -1.2: 6.57+2.488=9.06, no.
    # Let's just fit a polynomial through all points? Risky.
    # Given noise, best guess: y = 2.2*x^6 - x^5 for |x|>=2, and something else near 0.
    # But -1.2 is the only small point. Let's check if -1.2 fits y=2.2x^6-x^5: 9.06 vs -11.8. No.
    # Try y = x^5*(2.2x+1)? -1.2: -2.488*(-2.64+1)=-2.488*(-1.64)=4.08, no.
    # Try y = x^5*(2.2x) - x^5... same.
    # Maybe -1.2: y=-11.8166, and 11.8166/2.488=4.75. 4.75 = 2.2*(-1.2)+? = -2.64+? -> ?=7.39. weird.
    # Could be y = x^5 * (2.2x) but with x^5 computed... no.
    # Let me reconsider: maybe it's not x^6. Try y = 2.2*x^5*|x|? = 2.2*x^6*sign? no, x^5*|x| = x^6*sign(x)... for -1.2: 2.2*2.986*(-1)=-6.57.
    # Hmm.
    # Given uncertainty, model as y = 2.2*x**6 - x**5 (best fit for large), with note the near-zero point is off.
    # Actually let me try pure 2.2*x^6 for -1.2: 6.57 vs -11.8. Bad.
    # The sign of -1.2 output is negative, meaning odd-ish near 0. Maybe region |x|<2: y = x^5 * 4.75? = -11.8. 4.75 ~ ?
    # I'll model |x|>=2: 2.2*x^6 - x^5; |x|<2: something. But only one data point.
    # Best: use 2.2*x^6 - x^5 everywhere (fits 9/10 well), accept -1.2 error.
    import math
    out = []
    for x in probe["x"]:
        out.append(2.2 * x**6 - x**5)
    return {"y": out}
