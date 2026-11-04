import math

def predict(probe):
    # Model: f(x) looks roughly linear with slope ~4.5 for large |x|, but
    # near x=0 the output is much smaller in magnitude than linear predicts.
    # E1: x=-1.2 -> y=-1.35 (linear slope 4.5 would give -5.4), so there's
    # a dip/flattening near 0. Large values: -93.6->-434 (slope 4.64),
    # 88.9->423 (4.76), 67.5->322 (4.78), -62.7->-289 (4.62),
    # 38.8->187 (4.82), 73.9->352 (4.77), -104->-483 (4.65),
    # -120.7->-561 (4.65). Slope ~4.7, slightly larger for positive x.
    # The near-zero point is suppressed. Best guess: f(x) = a*x + b*tanh(c*x)
    # or similar odd-ish function with reduced slope near 0.
    # Fit: try f(x) = A*x + B*tanh(x) with A~4.5, B~? 
    # At x=-1.2: A*(-1.2)+B*tanh(-1.2) = -1.35 -> -1.2A - 0.834B = -1.35
    # At x=88.9: 88.9A + B*1 = 423.29
    # From large: A ~ 4.7, then 88.9*4.7=417.8, B~5.5
    # Check x=-1.2: -5.64 - 0.834*5.5 = -5.64-4.59=-10.2, too big.
    # So tanh doesn't fit. Maybe f(x)=A*x for |x|>threshold, and near 0
    # something like x^3-ish or a small linear region.
    # At x=-1.2, y=-1.35 -> slope 1.125 near zero.
    # Try piecewise: slope ~1.1 near 0, slope ~4.7 outside.
    # Transition? We only have one near-zero point. Use a smooth blend:
    # f(x) = 4.7*x - 3.6*x*exp(-x^2/s^2)? At x=-1.2: 4.7*-1.2=-5.64,
    # need -1.35, so correction +4.29 at x=-1.2. 
    # Let f(x)=4.7*x - 3.6*x*g(x) where g(0)=1, g large->0.
    # At x=-1.2: -5.64 + 3.6*1.2*g = -1.35 -> 4.32*g=4.29 -> g=0.993.
    # So g barely decays at 1.2. Hmm, that means correction nearly full.
    # Actually slope near 0 = 4.7-3.6=1.1. Good.
    # Need g(1.2)~0.99, so decay scale > 1.2. But at x=38.8 need g~0:
    # 4.7*38.8=182.4, observed 187.1, so correction is negative? 
    # 187.1-182.4=4.7, so f slightly above 4.7x. So slope maybe 4.8.
    # Let's just use slope 4.75 with a near-zero dip.
    # f(x)=4.75*x - 3.65*x*exp(-(x/2.5)^2)
    # At x=-1.2: -5.7 + 3.65*1.2*exp(-0.23)=-5.7+4.38*0.794=-5.7+3.48=-2.22. Not -1.35.
    # Need more dip. exp(-(x/1.5)^2): at 1.2 exp(-0.64)=0.527, corr=3.65*1.2*0.527=2.31, f=-3.39. Worse.
    # The dip must be very localized. exp(-(x/0.8)^2): at 1.2 exp(-2.25)=0.105, corr=0.46, f=-5.24. No.
    # Contradiction: to get -1.35 at x=-1.2 with slope 4.75 need corr 4.35,
    # i.e. g(1.2)=4.35/(3.65*1.2)=0.993. So g stays ~1 at 1.2 then drops fast.
    # That's like a plateau then cliff - unusual. Maybe f is not odd.
    # Alternative: f(x) = 4.75*x + small offset, but near 0 there's a
    # different regime entirely (the "interval where it behaves differently").
    # Perhaps |x|<~2: f(x)=1.1*x. Else f(x)=4.75*x + c.
    # Check continuity: at x=2, 1.1*2=2.2 vs 4.75*2=9.5. Discontinuous, unlikely.
    # Given MLP approximation, smooth transitions. Use a sigmoid blend:
    # f(x) = 4.75*x - 3.65*x*sigmoid((|x|-t)/w) ... 
    # Simplest robust guess: f(x)=4.75*x - 3.65*x*tanh((x/1.0)^2)? 
    # At x=1.2: tanh(1.44)=0.894, corr=3.65*1.2*0.894=3.92, f=-5.7+3.92=-1.78. Close-ish.
    # At x=38.8: tanh huge=1, corr=3.65*38.8=141.6, f=184.3-141.6=42.7. Way off!
    # No - the correction must vanish for large x, not saturate.
    # So use exp(-(x/w)^2) with w such that at 1.2 it's ~0.99 -> w large,
    # but then at 38.8 it's still ~1 -> wrong.
    # This means the near-zero behavior is NOT a smooth odd correction.
    # Reconsider: maybe f(x)=4.75*x + b where b varies, or the function
    # is like 4.75*x - 3.65*sin-like... 
    # Actually check: is it possible f(x)=4.75*x exactly except tiny x?
    # -1.2*4.75=-5.7 vs -1.35. Big deviation only at small x.
    # Perhaps f(x) = 4.75*x for |x|>3, and for |x|<3 a cubic: f=k*x^3.
    # At 1.2: k*1.728=-1.35 -> k=-0.78. At x=3: -0.78*27=-21 vs 4.75*3=14.25. Discontinuous.
    # Blend: f(x)=4.75*x*tanh(x/1.5)? At 1.2: 4.75*1.2*tanh(0.8)=5.7*0.664=3.78. No.
    # f(x)=4.75*x*tanh(x/0.5): at 1.2 tanh(2.4)=0.984, f=5.61. No.
    # Need f(1.2)=-1.35, i.e. factor 0.237. tanh(x/0.5) at 1.2=0.984 too big.
    # tanh(x/3): at 1.2 tanh(0.4)=0.38, f=2.17. 
    # tanh(x/5): 0.236, f=1.35! Sign: x negative -> f negative. 
    # f(x)=4.75*x*tanh(x/5)? At x=1.2: 4.75*1.2*tanh(0.24)=5.7*0.235=1.34. 
    # At x=-1.2: -1.34. Matches -1.35!
    # Check large: x=88.9: tanh(17.8)=1, f=4.75*88.9=422.3 vs 423.3. 
    # x=67.5: 4.75*67.5=320.6 vs 322.4. 
    # x=38.8: 184.3 vs 187.1. Slightly low; slope maybe 4.8.
    # x=-93.6: 4.8*-93.6=-449 vs -434. Hmm slope 4.64 there.
    # Let's fit slope: average |y/x| for large: 
    # 434.46/93.6=4.642, 423.29/88.9=4.761, 322.41/67.5=4.776,
    # 289.64/62.7=4.619, 187.12/38.8=4.823, 352.58/73.9=4.771,
    # 483.2/104=4.646, 561.47/120.7=4.652.
    # Positive x slope ~4.77, negative x slope ~4.64. Slight asymmetry.
    # Use f(x)=4.77*x*tanh(x/5) for x>=0, 4.64*x*tanh(x/5) for x<0.
    # Or a*x*tanh(x/5) with a=4.7 plus small linear asymmetry.
    # Keep simple: a=4.7, plus 0.07*x for x>0.
    # Actually asymmetry could be offset. Use f(x)=4.7*x*tanh(x/5)+0.06*x.
    # At x=88.9: 4.7*88.9+0.06*88.9=417.8+5.3=423.1. 
    # At x=-93.6: -439.9-5.6=-445.5 vs -434. Too negative.
    # Use offset only positive: f=4.7*x*tanh(x/5)+0.06*max(x,0).
    # x=-93.6: -439.9 vs -434. off by 6.
    # Try a=4.66 for negative: -436.2. Good.
    # Let a=4.66, pos add 0.11*x: x=88.9: 414.3+9.8=424.1. good.
    # x=67.5: 314.6+7.4=322.0 good.
    # x=38.8: 180.8+4.3=185.1 vs 187.1.
    # x=73.9: 344.4+8.1=352.5 good.
    # x=-62.7: -292.2 vs -289.6.
    # x=-104: -484.6 vs -483.2 good.
    # x=-120.7: -562.5 vs -561.5 good.
    # Good enough. Use tanh(x/5) factor.
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            base = 4.66 * x * math.tanh(x / 5.0)
            if x > 0:
                base += 0.11 * x
            out.append(base)
        except Exception:
            out.append(None)
    return {"y": out}
