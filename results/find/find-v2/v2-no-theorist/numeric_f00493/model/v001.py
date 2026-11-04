def predict(probe):
    # f(x) is dominated by a steep power law with sign-dependent behavior [E1,E2,E3]
    # For |x|>=1: y ~ -sign(x)*|x|^p with p around 6.5-7 [E2]
    #   check: x=100 -> -4.9e11 => |x|^p ~ 4.9e11 => p ~ log(4.9e11)/log(100) ~ 5.85
    #   x=64 -> -3.34e10 => p ~ log(3.34e10)/log(64) ~ 5.87
    #   x=32 -> -5.1e8 => p ~ log(5.1e8)/log(32) ~ 5.83
    #   x=16 -> -7.66e6 => p ~ log(7.66e6)/log(16) ~ 5.82
    #   x=8 -> -1.15e5 => p ~ log(1.15e5)/log(8) ~ 5.44 (noisy)
    #   So p ~ 5.85, coefficient ~ -1 for positive x
    # For negative x: y is positive and slightly larger magnitude [E2]
    #   x=-100 -> +5.09e11, x=-64 -> +3.54e10, x=-32 -> +5.7e8
    #   ratio neg/pos ~ 1.037 consistently
    # For |x|<1: y is small, positive for negative x, negative for positive x [E2]
    #   x=0.5 -> -0.0, x=-0.5 -> +6.24, x=0.25 -> -0.0, x=-0.25 -> +5.11
    #   Hmm, negative small x gives ~5-6, positive small x gives ~0
    #   x=1 -> -4.3, x=-1 -> +6.1
    #   x=1.2 -> -6.4 [E3]
    # There's a region near |x|<~1.5 that behaves differently [E2,E3]
    # For |x|>=~2: strong power law [E1,E3]
    #   E1: x=88.2 -> -2.3e11; 88.2^5.85 ~ ?  log10: 5.85*1.945=11.38 -> 2.4e11. good
    #   x=66 -> -4.03e10; 66^5.85: 5.85*1.8195=10.64 -> 4.4e10. good
    #   x=2.9 -> -247.7; 2.9^5.85: 5.85*0.4624=2.705 -> 507. off by 2x
    #   x=21.3 -> -4.28e7; 21.3^5.85: 5.85*1.3284=7.77 -> 5.9e7. good
    # So p~5.85, coeff ~ -1 for x>0, +1.037 for x<0, valid for |x|>=~2
    # For |x|<~2: small values, sign flips: positive x -> small negative, negative x -> small positive ~5-6
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ax = abs(x)
            if ax >= 2.0:
                p = 5.85
                if x > 0:
                    y = -(ax ** p)
                else:
                    y = 1.037 * (ax ** p)
            else:
                # small region: negative x -> ~+5.5, positive x -> ~0 to -6
                if x < 0:
                    y = 5.5
                else:
                    y = -5.0 * x
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
