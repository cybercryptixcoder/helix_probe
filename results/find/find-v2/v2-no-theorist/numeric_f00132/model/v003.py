def predict(probe):
    # Model: y = m*x + b, piecewise linear with a smooth transition near origin.
    # Far-field slopes: positive ~4.714, negative ~4.6865 [E2,E8,E10]
    # Far-field intercept ~4.2 [E2,E4,E8]
    # Near origin the function is smooth and monotone, no dip/bump: it's a smooth
    # transition between the two linear regimes [E12,E14,E16]. The v2 dip+bump
    # correction was wrong; the data show a clean monotone curve.
    # Fit: y(0)=3.9155, y(1)=8.9349, y(-1)=-0.2396, y(0.5)=6.5856, y(-0.5)=1.9577
    # A good fit: y = 4.7*x + 4.2 + c*tanh(x/s) style transition, or use a
    # smooth blend of the two lines with a sigmoid.
    # Let's fit: y = a*x + b + d*tanh(x/t) where a=(4.714+4.6865)/2=4.70025,
    # d=(4.714-4.6865)/2=0.01375, b=4.2. But near origin the curve is steeper.
    # Check E12: y(0)=3.9155 (b would be 4.2, off 0.28). y(0.1)=4.4652.
    # Slope near 0 positive: (4.4652-3.9155)/0.1=5.497. Negative: (3.9155-3.4123)/0.1=5.032.
    # So near origin slope ~5.2, larger than far-field 4.7. There's a smooth
    # steepening near 0. This looks like y = 4.7*x + 4.2 + A*tanh(x/s)*something?
    # Actually a simple fit: y = 4.7*x + 4.2 + 0.3*tanh(x/0.5)? 
    # x=0: 4.2 vs 3.9155. Need lower at 0.
    # Try y = 4.7*x + 3.9 + 0.3*tanh(x/0.5):
    # x=0: 3.9 vs 3.9155 ok
    # x=0.5: 2.35+3.9+0.3*0.762=6.48 vs 6.586 ok
    # x=1: 4.7+3.9+0.3*0.964=8.89 vs 8.93 ok
    # x=-0.5: -2.35+3.9-0.228=1.32 vs 1.958 off 0.64. Bad.
    # The negative side is higher than symmetric. Asymmetric.
    # Let's fit separately. Positive side (x>=0):
    # y(0)=3.9155, y(0.1)=4.4652, y(0.2)=4.9996, y(0.5)=6.5856, y(1)=8.9349, y(2)=13.6499
    # Differences: 0.55,0.53,0.53,0.53,0.47,0.47 per 0.1... wait
    # 0->0.1: 0.5497; 0.1->0.2: 0.5344; 0.2->0.3: 0.5324; ... 0.9->1.0: 0.4684
    # So slope decreases from ~5.5 at 0 to ~4.7 far. Smooth.
    # Negative side: y(0)=3.9155, y(-0.1)=3.4123, y(-0.2)=2.9898, y(-0.5)=1.9577, y(-1)=-0.2396
    # 0->-0.1: -0.5032; -0.1->-0.2: -0.4225; -0.2->-0.3: -0.3633; ... -0.9->-1.0: -0.5521
    # Hmm slope magnitude ~5.0 near 0, dips to ~3.6 around -0.3, then back up.
    # That's non-monotone slope! Let's check: y(-0.3)=2.6265, y(-0.4)=2.2982 diff -0.3283
    # y(-0.4)->-0.5: -0.3405; -0.5->-0.6: -0.3541; -0.6->-0.7: -0.3575; -0.7->-0.8: -0.4251
    # -0.8->-0.9: -0.5083; -0.9->-1.0: -0.5521
    # So slope magnitude: 5.03,4.23,3.63,3.28,3.41,3.54,3.58,4.25,5.08,5.52
    # It dips around -0.35 then rises. That's a subtle S-shape / inflection.
    # This is consistent with a smooth transition between two linear regimes
    # with different slopes AND a slight offset. The MLP approximates a smooth
    # function; near origin it's a smooth blend.
    # Let's just fit a smooth function: y = 4.7*x + 4.2 + correction(x)
    # where correction is small and smooth. Use the data to fit a few terms.
    # Actually, let's try: y = 4.7*x + 4.2 + c1*exp(-x^2/s1) + c2*x*exp(-x^2/s2)
    # Simpler: fit a cubic spline-ish via tanh terms.
    # Let me try y = 4.7*x + 4.2 - 0.3*exp(-x^2/2) + 0.15*x*exp(-x^2/2)
    # x=0: 4.2-0.3=3.9 vs 3.9155 ok
    # x=0.5: 2.35+4.2-0.3*0.882+0.15*0.5*0.882=6.55-0.265+0.066=6.35 vs 6.586 off
    # Hmm.
    # Let's just do a direct smooth interpolation: use the fact that far field is
    # linear and near origin is a smooth curve. A good functional form:
    # y = m*x + b + A*tanh((x-x0)/w) won't capture the dip in slope.
    # Given the MLP nature, maybe it's y = 4.7*x + 4.2 + 0.5*sin(x)*exp(-|x|/3)?
    # x=0: 4.2 vs 3.9155. Need -0.28 at 0.
    # Try y = 4.7*x + 3.92 + 0.28*(1-exp(-x^2/0.5)) + ... 
    # Let me just fit a polynomial on small range and blend.
    # Simplest robust approach: piecewise with smooth blend using a sigmoid.
    # For x>0: y = 4.714*x + 4.2 - 0.28*exp(-x/0.3)? 
    # x=0: 4.2-0.28=3.92 ok; x=0.1: 0.4714+4.2-0.28*0.717=4.47 vs 4.465 ok!
    # x=0.2: 0.9428+4.2-0.28*0.513=4.999 vs 4.9996 ok!
    # x=0.5: 2.357+4.2-0.28*0.189=6.504 vs 6.586 off 0.08
    # x=1: 4.714+4.2-0.28*0.036=8.90 vs 8.93 ok
    # x=2: 9.428+4.2-0.28*0.0013=13.63 vs 13.65 ok
    # Great for positive side!
    # Negative side: y = 4.6865*x + 4.2 + correction
    # x=0: need 3.9155, so correction -0.2845
    # x=-0.1: -0.46865+4.2=3.731, need 3.4123, correction -0.319
    # x=-0.2: -0.9373+4.2=3.263, need 2.9898, correction -0.273
    # x=-0.3: -1.406+4.2=2.794, need 2.6265, correction -0.168
    # x=-0.5: -2.343+4.2=1.857, need 1.9577, correction +0.10
    # x=-1: -4.6865+4.2=-0.4865, need -0.2396, correction +0.247
    # x=-1.5: -7.03+4.2=-2.83, need -2.9318, correction -0.10
    # x=-2: -9.373+4.2=-5.173, need -5.1471, correction +0.026
    # So correction on negative side: -0.28 at 0, dips to -0.32 at -0.1, rises to +0.25 at -1, back to 0 at -2.
    # That's a wiggle. Could be exp terms.
    # Try correction = -0.28*exp(-x^2/0.1) + 0.3*exp(-(x+1)^2/0.8)
    # x=0: -0.28+0.3*0.287=-0.194 vs -0.2845
    # Hmm.
    # Let's try: correction = -0.3*exp(-x^2/0.15) + 0.28*exp(-(x+1)^2/0.6)
    # x=0: -0.3+0.28*0.189=-0.247 vs -0.2845
    # x=-0.1: -0.3*0.935+0.28*0.223=-0.2805+0.0624=-0.218 vs -0.319
    # Not great.
    # Given the complexity, maybe the true function is just a smooth MLP and
    # a simple approximation suffices. The far-field is what matters most for
    # sealed probes (random ordinary probes dominate). Near-origin error is small
    # in absolute terms.
    # Let me use a clean smooth fit: y = 4.7*x + 4.2 + a*tanh(x/w) + c*exp(-x^2/s)
    # Actually, let's just fit a cubic polynomial on [-2,2] blended with linear outside.
    # But simpler: use the positive-side formula for x>=0 and a similar for x<0.
    # Positive: y = 4.714*x + 4.2 - 0.28*exp(-x/0.3)  (works well)
    # Negative: fit y = 4.6865*x + 4.2 + corr(x)
    # Let's fit corr with two gaussians: corr = A*exp(-x^2/s) + B*exp(-(x+1)^2/t)
    # Using points: (-0.1,-0.319),(-0.5,0.10),(-1,0.247),(-2,0.026),(0,-0.2845)
    # At x=0: A + B*exp(-1/t) = -0.2845
    # At x=-1: A*exp(-1/s) + B = 0.247
    # At x=-0.5: A*exp(-0.25/s)+B*exp(-0.25/t)=0.10
    # At x=-2: A*exp(-4/s)+B*exp(-1/t)=0.026
    # Try s=0.5, t=1.0: exp(-1/0.5)=0.135, exp(-1)=0.368
    # A+0.368B=-0.2845; 0.135A+B=0.247
    # From first: A=-0.2845-0.368B. Sub: 0.135(-0.2845-0.368B)+B=0.247
    # -0.0384-0.0497B+B=0.247 -> 0.9503B=0.2854 -> B=0.300, A=-0.2845-0.110=-0.395
    # Check x=-0.5: -0.395*exp(-0.5)+0.300*exp(-0.25)=-0.395*0.607+0.300*0.779=-0.240+0.234=-0.006 vs 0.10. Off.
    # Try s=0.3,t=1.5: exp(-3.33)=0.0357, exp(-0.667)=0.513
    # A+0.513B=-0.2845; 0.0357A+B=0.247
    # A=-0.2845-0.513B; 0.0357(-0.2845-0.513B)+B=0.247
    # -0.01016-0.0183B+B=0.247 -> 0.9817B=0.2572 -> B=0.262, A=-0.2845-0.134=-0.419
    # x=-0.5: -0.419*exp(-0.833)+0.262*exp(-0.167)=-0.419*0.435+0.262*0.846=-0.182+0.222=0.040 vs 0.10
    # x=-2: -0.419*exp(-13.3)+0.262*exp(-0.667)=-0+0.262*0.513=0.134 vs 0.026. Off.
    # This is getting too fiddly. 
    # Let me step back. The far-field linear model is excellent (E13,E15 match 1.00).
    # The near-origin is a smooth monotone-ish curve. The v2 dip+bump was wrong.
    # A simple smooth model: y = 4.7*x + 4.2 + 0.3*tanh(x/0.7) - 0.3*exp(-x^2/2)?
    # Let's just use a smooth blend: y = 4.7*x + 4.2 + A*tanh(x/w) + B*x*exp(-x^2/s)
    # Actually, the cleanest: fit a smooth function that matches the data.
    # Let me use: y = 4.7*x + 4.2 + 0.35*tanh(x/0.4) - 0.35*tanh(x/2) ... no.
    # 
    # Given time, let me use a piecewise-linear with smooth sigmoid blend and
    # a small correction. The key insight: near origin slope is ~5.2, far is 4.7.
    # So y = 4.7*x + 4.2 + 0.5*tanh(x/0.5)*x? No, that changes slope.
    # Slope = 4.7 + d/dx[correction]. Near 0 slope ~5.2, so correction' ~0.5.
    # Correction goes from -0.28 at 0 to 0 at large x. If correction = -0.28*exp(-x^2/s),
    # correction' = 0.56*x/s*exp(-x^2/s). At x=0.1, s=0.5: 0.56*0.1/0.5*0.98=0.11. Too small.
    # Need correction' ~0.5 at x=0.1. So 0.56*0.1/s*exp(-0.01/s)=0.5 -> s small.
    # s=0.05: 0.56*0.1/0.05*exp(-0.2)=1.12*0.819=0.917. Too big.
    # s=0.1: 0.56*0.1/0.1*exp(-0.1)=0.56*0.905=0.507. 
    # So correction = -0.28*exp(-x^2/0.1) for positive side?
    # Check x=0.1: -0.28*0.905=-0.253; y=0.4714+4.2-0.253=4.418 vs 4.4652 ok
    # x=0.2: -0.28*exp(-0.4)=-0.188; y=0.9428+4.2-0.188=4.955 vs 4.9996 ok
    # x=0.5: -0.28*exp(-2.5)=-0.023; y=2.357+4.2-0.023=6.534 vs 6.586 ok
    # x=1: -0.28*exp(-10)=0; y=8.914 vs 8.93 ok
    # x=0: 4.2-0.28=3.92 vs 3.9155 ok!
    # Great, positive side: y = 4.714*x + 4.2 - 0.28*exp(-x^2/0.1)
    # Negative side: need correction -0.28 at 0, -0.32 at -0.1, -0.27 at -0.2, -0.17 at -0.3, +0.10 at -0.5, +0.25 at -1, 0 at -2.
    # Try correction = -0.28*exp(-x^2/0.1) + 0.3*exp(-(x+1)^2/0.5)
    # x=0: -0.28+0.3*exp(-2)=-0.28+0.041=-0.239 vs -0.2845
    # x=-0.1: -0.28*0.905+0.3*exp(-1.62)=-0.253+0.059=-0.194 vs -0.319
    # Not matching. The negative side has a deeper dip at -0.1.
    # Maybe the negative side is: y = 4.6865*x + 4.2 - 0.32*exp(-(x+0.1)^2/0.1) + 0.3*exp(-(x+1)^2/0.5)
    # x=0: -0.32*exp(-0.1)+0.3*exp(-2)=-0.290+0.041=-0.249 vs -0.2845
    # x=-0.1: -0.32+0.3*exp(-1.62)=-0.32+0.059=-0.261 vs -0.319
    # x=-0.5: -0.32*exp(-1.6)+0.3*exp(-0.5)=-0.065+0.182=0.117 vs 0.10 ok
    # x=-1: -0.32*exp(-8.1)+0.3=0.3 vs 0.247 ok-ish
    # x=-2: -0.32*exp(-36)+0.3*exp(-2)=0.041 vs 0.026 ok
    # Decent. Let me refine: use -0.35*exp(-(x+0.1)^2/0.08) + 0.28*exp(-(x+1)^2/0.6)
    # x=0: -0.35*exp(-0.125)+0.28*exp(-1.667)=-0.309+0.053=-0.256 vs -0.2845
    # x=-0.1: -0.35+0.28*exp(-1.35)=-0.35+0.073=-0.277 vs -0.319
    # Meh. Close enough given MLP noise.
    # Actually, let me reconsider: maybe the whole thing is one smooth function
    # and I should just fit a single formula. 
    # Let me try: y = 4.7*x + 4.2 + 0.3*tanh(x/0.5) - 0.3*exp(-x^2/0.5) ... 
    # I'll go with the piecewise approach with gaussian corrections, which fits
    # the data reasonably. The far-field is exact, near-origin within ~0.1.
    import math
    def f(x):
        if x >= 0:
            return 4.714*x + 4.2 - 0.28*math.exp(-x*x/0.1)
        else:
            return 4.6865*x + 4.2 - 0.32*math.exp(-(x+0.1)**2/0.1) + 0.28*math.exp(-(x+1.0)**2/0.6)
    return {"y": [f(x) for x in probe["x"]]}
