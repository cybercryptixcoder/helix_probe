def predict(probe):
    # f is smooth and decreasing overall, saturating at both ends.
    # Left asymptote ~+74 for x <= ~-124 [E4: -124.4->74.2]; still rising at -102->62.4 [E3]
    # Right asymptote ~-70 for x >= ~120 [E2: 123.6->-70.3, 119.5->-69.6]
    # Middle is roughly linear, slope ~ -0.75 [E1: (88.2,-64)->(-50.4,34.8)]
    #   check: (34.8-(-64))/(88.2-(-50.4)) = 98.8/138.6 = 0.713
    # Intercept: at x=0, y ~ 0? E1: -6->6.6, 2.9->-18.6 (wiggle), 21.3->-45.8
    #   line through (-50.4,34.8) slope -0.713: y(0)=34.8-0.713*50.4=-1.1
    #   y(21.3) = -1.1 -0.713*21.3 = -16.3 vs observed -45.8 -> slope steeper in middle?
    # Recompute slope from E1 middle points: (-20.3,18.7),(21.3,-45.8): slope=-64.5/41.6=-1.55
    #   (-6.0,6.6),(21.3,-45.8): slope=-52.4/27.3=-1.92
    #   (-24.3,20.9),(-6.0,6.6): slope=-14.3/18.3=-0.78
    #   So slope varies: shallow near -20, steep near 0..20. A sigmoid-like steep middle.
    # Try: linear slope ~ -0.72 far out, steeper transition around x~10.
    # E4: -5.9->6.4, 12.5->-38.5: slope=-44.9/18.4=-2.44 (steep)
    # E4: 43->-54.6, 56.2->-58.2: slope=-3.6/13.2=-0.27 (shallow)
    # E4: 78.1->-62.1, 93.5->-64.9: slope=-2.8/15.4=-0.18 (shallow)
    # E3: 28.4->-49.1, 47.1->-56.2: slope=-7.1/18.7=-0.38
    # E3: -48.6->33.8, -16.9->16.9: slope=-16.9/31.7=-0.53
    # E3: -102.2->62.4, -48.6->33.8: slope=-28.6/53.6=-0.53
    # E2: -63.9->42.0, -55.8->37.7: slope=-4.3/8.1=-0.53
    # E2: 65.5->-59.9, 79.4->-62.4: slope=-2.5/13.9=-0.18
    # E2: 103->-66.6, 104.5->-66.9: slope=-0.3/1.5=-0.2
    # So: slope ~ -0.53 on left, steepens to ~-2.4 around x~5-15, then shallow ~-0.2 on right.
    # This is a sigmoid transition centered near x~5, from +high to -high, PLUS linear tails.
    # Model: y = A - B*tanh((x-c)/w) - k*x  (sigmoid transition + linear drift)
    # Far left: y ~ A + B - k*x (slope -k). Far right: y ~ A - B - k*x.
    # Left slope -0.53 => k=0.53. Right slope -0.2 => k=0.2. Inconsistent; use k~0.35?
    # Actually left tail slope ~-0.53, right tail ~-0.2. Use piecewise or average.
    # Let's fit: at x=-124.4, y=74.2; x=123.6, y=-70.3.
    # Try y = C - D*tanh((x-c)/w) - k*x with k=0.35, c=5, w=12.
    # x=-124: tanh~-1 => C+D+0.35*124 = C+D+43.4 =74.2 => C+D=30.8
    # x=123.6: tanh~1 => C-D-0.35*123.6 = C-D-43.3 = -70.3 => C-D=-27.0
    # => C=1.9, D=28.9
    # Check x=21.3: tanh((21.3-5)/12)=tanh(1.36)=0.876 => y=1.9-28.9*0.876-0.35*21.3=1.9-25.3-7.5=-30.9 vs -45.8. Too high.
    # Steeper/earlier transition. Try c=8, w=10.
    # x=21.3: tanh(1.33)=0.869 => similar. Need more negative.
    # The middle is steeper than tanh alone. Maybe two sigmoids or steeper.
    # E1: 2.9->-18.6 (wiggle noted), 21.3->-45.8, -6->6.6
    # Slope from -6 to 21.3 is -1.92, from -20.3 to -6 is -0.78.
    # Try logistic: y = lo + (hi-lo)/(1+exp((x-mid)/s)) with linear tails.
    # Let's just use a piecewise-linear-ish smooth: 
    # Use y = p - q*x - r*tanh((x-c)/w) with steeper w.
    # Fit three points: (-124.4,74.2),(21.3,-45.8),(123.6,-70.3)
    # Let k=0.3, c=10, w=8.
    # x=-124: tanh(-16.75)=-1 => p+q*124.4+r = 74.2
    # x=123.6: tanh(14.2)=1 => p-q*123.6-r = -70.3
    # x=21.3: tanh(1.41)=0.887 => p-0.3*21.3-0.887r = -45.8 => p-6.39-0.887r=-45.8 => p-0.887r=-39.4
    # From 1&2: 2p + q*0.8 = 3.9 => p ~ 1.95 - 0.4q
    # Sub: 1.95-0.4q-0.887r=-39.4 => 0.4q+0.887r=41.35
    # From 1: p+124.4q+r=74.2 => 1.95-0.4q+124.4q+r=74.2 => 124q+r=72.25
    # => r=72.25-124q. Sub: 0.4q+0.887(72.25-124q)=41.35 => 0.4q+64.1-110q=41.35 => -109.6q=-22.75 => q=0.208, r=72.25-25.8=46.5, p=1.95-0.083=1.87
    # Check x=-20.3: tanh(-3.79)=-0.999 => y=1.87+0.208*20.3+46.5*0.999=1.87+4.22+46.5=52.6 vs 18.7. WAY off.
    # Left side isn't saturating that fast; -20.3 is still mid-range.
    # E1: -20.3->18.7, -24.3->20.9, -50.4->34.8, -61.7->40.8
    # Slope -50.4 to -61.7: (40.8-34.8)/(-61.7+50.4)=6/-11.3=-0.53
    # Slope -24.3 to -50.4: (34.8-20.9)/(-50.4+24.3)=13.9/-26.1=-0.53
    # Slope -20.3 to -24.3: (20.9-18.7)/(-24.3+20.3)=2.2/-4=-0.55
    # So left is linear slope -0.53 from -61.7 to -20.3. Then steepens.
    # E4: -61.3->40.6, -25.9->21.7: slope=(21.7-40.6)/(-25.9+61.3)=-18.9/35.4=-0.53 ✓
    # E4: -25.9->21.7, -5.9->6.4: slope=(6.4-21.7)/(-5.9+25.9)=-15.3/20=-0.765
    # E4: -5.9->6.4, 12.5->-38.5: slope=-44.9/18.4=-2.44
    # So transition steepens around x~0-10.
    # Right side: E2: 65.5->-59.9, 79.4->-62.4: slope=-0.18
    # E3: 47.1->-56.2, 58.8->-58.7: slope=-2.5/11.7=-0.21
    # E4: 43->-54.6, 56.2->-58.2: slope=-0.27
    # So right is linear slope ~-0.2 from ~43 onward.
    # E3: 28.4->-49.1, 47.1->-56.2: slope=-0.38 (transitioning)
    # E2: 30.3->-49.8, 65.5->-59.9: slope=-10.1/35.2=-0.29
    # So: left linear slope -0.53 (x<-20), steep transition (x~-10 to 30), right linear slope -0.2 (x>45).
    # Model as: y = a - b*x for x < x1; smooth transition; y = c - d*x for x > x2.
    # Use a smooth blend: y = L(x)*(1-s) + R(x)*s where s=sigmoid((x-m)/w)
    # L(x) = a - 0.53*x, R(x) = c - 0.2*x
    # Match at transition: at x=-20, L=18.7 => a=18.7-0.53*20=18.7-10.6=8.1... wait a-0.53*(-20)=a+10.6=18.7 => a=8.1
    # Check L(-61.7)=8.1+0.53*61.7=8.1+32.7=40.8 ✓
    # R: at x=65.5, R=-59.9 => c-0.2*65.5=c-13.1=-59.9 => c=-46.8
    # Check R(123.6)=-46.8-24.7=-71.5 vs -70.3, close. R(43)=-46.8-8.6=-55.4 vs -54.6 ✓
    # Transition center: where L=R: 8.1-0.53x = -46.8-0.2x => 54.9=0.33x => x=166? That's wrong.
    # Hmm L and R cross at x=166, but transition is around x~10.
    # At x=10: L=8.1-5.3=2.8, R=-46.8-2=-48.8. Observed ~? E4: 12.5->-38.5. Between.
    # So blend s at x=12.5 should give -38.5: 2.8*(1-s)+(-48.8)*s = -38.5 => 2.8-51.6s=-38.5 => s=0.80
    # At x=-5.9: L=8.1+3.1=11.2, R=-46.8+1.2=-45.6. Observed 6.4. s: 11.2-56.8s=6.4 => s=0.084
    # At x=21.3: L=8.1-11.3=-3.2, R=-46.8-4.3=-51.1. Observed -45.8. s: -3.2-47.9s=-45.8 => s=0.89
    # At x=28.4: L=8.1-15.1=-7.0, R=-46.8-5.7=-52.5. Observed -49.1. s: -7-45.5s=-49.1 => s=0.925
    # At x=43: L=8.1-22.8=-14.7, R=-46.8-8.6=-55.4. Observed -54.6. s: -14.7-40.7s=-54.6 => s=0.98
    # At x=-20.3: L=18.7, R=-42.7. Observed 18.7. s=0
    # At x=-24.3: L=20.9, R=-42.0. Observed 20.9. s=0
    # So s=0 at x=-20, s=0.084 at -5.9, s=0.80 at 12.5, s=0.89 at 21.3, s=0.98 at 43.
    # Sigmoid: s=1/(1+exp(-(x-m)/w)). s=0.084 at -5.9: -(x-m)/w = ln(0.084/0.916)=-2.39 => (-5.9-m)/w=2.39
    # s=0.80 at 12.5: (12.5-m)/w=ln(4)=1.386
    # => 12.5-m=1.386w, -5.9-m=2.39w => 18.4 = -1.0w => w negative? 
    # 12.5-m=1.386w and -5.9-m=2.39w => subtract: 18.4 = -1.004w => w=-18.3. Inconsistent (s should increase with x).
    # Recheck: s=0.084 at x=-5.9 means (x-m)/w = ln(0.084/0.916)=-2.39, so (-5.9-m)/w=-2.39
    # s=0.80 at 12.5: (12.5-m)/w=1.386
    # => 12.5-m=1.386w, -5.9-m=-2.39w => 18.4=3.776w => w=4.87, m=12.5-6.75=5.75
    # Check s at 21.3: (21.3-5.75)/4.87=3.19 => s=0.96 vs 0.89. Close-ish.
    # s at 43: (43-5.75)/4.87=7.65 => s~1.0 ✓
    # s at -20.3: (-26)/4.87=-5.3 => s~0.005 ✓
    # Good. So m=5.75, w=4.87.
    # But wait, at x=2.9 E1 gives -18.6 (wiggle). L(2.9)=8.1-1.5=6.6, R=-47.4. s=(2.9-5.75)/4.87=-0.585 => s=0.358. y=6.6*0.642+(-47.4)*0.358=4.2-17.0=-12.8 vs -18.6. Off by 6.
    # E1 x=2.9 noted as wiggle. Maybe noise or a small bump. Ignore.
    # Check E1 x=21.3: L=-3.2,R=-51.1,s=0.96 => -3.2*0.04-51.1*0.96=-0.13-49.1=-49.2 vs -45.8. Off by 3.4.
    # Check E4 x=12.5: L=1.5,R=-49.3,s=0.80 => 0.3-39.4=-39.1 vs -38.5 ✓
    # Check E3 x=28.4: L=-7.0,R=-52.5,s=0.99 => -52.0 vs -49.1. Off 3.
    # Reasonable. Let me tune m,w slightly. Use m=6, w=5.
    # Check x=21.3: s=(15.3)/5=3.06=>0.955 => -3.2*0.045-51.1*0.955=-0.14-48.8=-48.9 vs -45.8
    # Slightly high. Maybe R slope steeper or transition wider. Use w=6.
    # x=21.3: s=15.3/6=2.55=>0.928 => -3.2*0.072-51.1*0.928=-0.23-47.4=-47.6 vs -45.8. Better.
    # x=12.5: s=6.5/6=1.08=>0.747 => 1.5*0.253-49.3*0.747=0.38-36.8=-36.4 vs -38.5. Off 2.
    # x=-5.9: s=-11.9/6=-1.98=>0.121 => 11.2*0.879-45.6*0.121=9.8-5.5=4.3 vs 6.4. Off 2.
    # Good enough. Use m=6, w=6.
    # Also check far left: x=-124.4: s~0 => L=8.1+0.53*124.4=8.1+65.9=74.0 vs 74.2 ✓
    # x=-102.2: L=8.1+54.2=62.3 vs 62.4 ✓
    # x=-63.9: L=8.1+33.9=42.0 vs 42.0 ✓
    # Far right: x=123.6: s~1 => R=-46.8-24.7=-71.5 vs -70.3. Off 1.2.
    # x=119.5: R=-46.8-23.9=-70.7 vs -69.6. Off 1.1.
    # x=104.5: R=-46.8-20.9=-67.7 vs -66.9. Off 0.8.
    # Slightly too negative. Adjust c=-46.0: R(123.6)=-70.7 vs -70.3 ✓, R(65.5)=-59.1 vs -59.9 (off 0.8)
    # Use c=-46.5: R(123.6)=-71.2, R(65.5)=-59.6. Compromise c=-46.3.
    # Final: L(x)=8.1-0.53x, R(x)=-46.3-0.2x, s=sigmoid((x-6)/6)
    import math
    def f(x):
        L = 8.1 - 0.53*x
        R = -46.3 - 0.2*x
        s = 1.0/(1.0+math.exp(-(x-6.0)/6.0))
        return L*(1.0-s) + R*s
    out = []
    for x in probe.get("x", []):
        try:
            out.append(f(float(x)))
        except Exception:
            out.append(None)
    return {"y": out}
