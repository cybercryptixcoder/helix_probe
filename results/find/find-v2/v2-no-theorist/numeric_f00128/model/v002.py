def predict(probe):
    # y is a smooth, nearly linear function of x with slight curvature [E1, E2].
    # Slope ~ -12.66 per unit x, intercept ~ +5.4 at x=0 [E2].
    # Curvature is small; a quadratic fit captures it well [E2].
    # Fit quadratic through E2 points: y = a*x^2 + b*x + c
    # Using (0,5.4186), (100,-1678.7955), (-100,678.4023):
    #   c = 5.4186
    #   10000a + 100b = -1684.2141
    #   10000a - 100b = 672.9837
    #   => 20000a = -1011.2304 => a = -0.05056152
    #   => 100b = -1684.2141 - 10000*(-0.05056152) = -1684.2141 + 505.6152 = -1178.5989
    #   => b = -11.785989
    # Check at x=50: a*2500 + b*50 + c = -126.404 - 589.299 + 5.419 = -710.28 (obs -833.8)
    # Hmm, off. Try cubic? Let's refit with more points via least squares mentally.
    # Actually check slope between consecutive E2 points:
    # -100->-80: (543.2-678.4)/20 = -6.76
    # -80->-40: (272.8-543.2)/40 = -6.76
    # -40->-30: (205.2-272.8)/10 = -6.76
    # -30->-15: (103.8-205.2)/15 = -6.76
    # -15->-10: (70.0-103.8)/5 = -6.76
    # -10->-3: (22.67-70.0)/7 = -6.76
    # -3->0: (5.42-22.67)/3 = -5.75  <- changes!
    # 0->5: (-73.29-5.42)/5 = -15.74
    # 5->10: (-157.8+73.29)/5 = -16.90
    # 10->15: (-242.3+157.8)/5 = -16.90
    # 15->30: (-495.8+242.3)/15 = -16.90
    # 30->40: (-664.8+495.8)/10 = -16.90
    # 40->50: (-833.8+664.8)/10 = -16.90
    # 50->60: (-1002.8+833.8)/10 = -16.90
    # 60->75: (-1256.3+1002.8)/15 = -16.90
    # 75->80: (-1340.8+1256.3)/5 = -16.90
    # 80->90: (-1509.8+1340.8)/10 = -16.90
    # 90->100: (-1678.8+1509.8)/10 = -16.90
    # 100->110: (-1847.8+1678.8)/10 = -16.90
    # So: slope is -6.76 for x < ~0, and -16.90 for x > ~0!
    # There's a kink near x=0. Piecewise linear!
    # Left: y = -6.76*x + c_left. At x=0, y=5.42 => c_left=5.42
    #   Check x=-100: -6.76*(-100)+5.42 = 681.4 (obs 678.4) close
    #   Check x=-80: 540.8+5.42=546.2 (obs 543.2) close
    #   Slope maybe -6.76 exactly? (543.2-678.4)/(-80+100) = -135.2/20 = -6.76
    #   At x=-100: 678.4 = -6.76*(-100)+c => c = 678.4-676 = 2.4
    #   At x=-80: 543.2 = 540.8+c => c=2.4
    #   At x=-40: 272.8 = 270.4+c => c=2.4
    #   At x=-3: 22.67 = 20.28+c => c=2.39
    #   So left: y = -6.76*x + 2.4 for x <= 0
    # Right: slope -16.90. At x=5: -73.29 = -16.90*5+c => c = -73.29+84.5 = 11.21
    #   At x=10: -157.8 = -169+c => c=11.2
    #   At x=110: -1847.8 = -1859+c => c=11.2
    #   So right: y = -16.90*x + 11.2 for x >= 0
    # At x=0: left gives 2.4, right gives 11.2. Observed 5.42. Hmm.
    # Maybe there's a smooth transition near 0. Or the kink is at some x0.
    # Let's find intersection: -6.76x+2.4 = -16.90x+11.2 => 10.14x = 8.8 => x=0.868
    # At x=0.868: y = -6.76*0.868+2.4 = -3.47. But obs at 0 is 5.42.
    # So not a simple kink. Maybe there's a smooth curve near 0.
    # Actually maybe it's a smooth function overall, like tanh-ish or a smooth blend.
    # Let's reconsider: slopes are constant far from 0 but transition near 0.
    # This looks like a smooth step in slope: y' = -6.76 + (-16.90+6.76)*sigmoid(x/w)
    # Or simpler: y = a*x + b + c*softplus-like.
    # Given MLP approximation, likely something like y = -11.83*x + 5.42 - 5.07*tanh(x/2)? 
    # Let's just fit a smooth function. Try: y = A*x + B + C*tanh(x/D)
    # As x->+inf: slope A + C/D. As x->-inf: slope A - C/D.
    # A+C/D = -16.90, A-C/D = -6.76 => A = -11.83, C/D = -5.07
    # At x=0: y=B=5.42
    # Need C*tanh(x/D) to give the transition. At x=5: -73.29 = -11.83*5+5.42+C*tanh(5/D)
    #   -73.29 = -59.15+5.42+C*tanh(5/D) => -19.56 = C*tanh(5/D)
    # At x=10: -157.8 = -118.3+5.42+C*tanh(10/D) => -44.92 = C*tanh(10/D)
    # At x=15: -242.3 = -177.45+5.42+C*tanh(15/D) => -70.27 = C*tanh(15/D)
    # Ratio tanh(10/D)/tanh(5/D) = 44.92/19.56 = 2.297
    # Ratio tanh(15/D)/tanh(10/D) = 70.27/44.92 = 1.564
    # Try D=2: tanh(2.5)=0.9866, tanh(5)=0.9999 => ratio 1.013, no
    # Try D=5: tanh(1)=0.7616, tanh(2)=0.9640 => ratio 1.266, tanh(3)=0.9951 ratio 1.032
    # Try D=3: tanh(5/3)=0.9311, tanh(10/3)=0.9975 ratio 1.071
    # Hmm ratios too small. Need slower saturation. Try D=10: tanh(0.5)=0.4621, tanh(1)=0.7616 ratio 1.648
    #   tanh(1.5)=0.9051 ratio 1.188. Close-ish to 1.564? Not quite.
    # Try D=8: tanh(0.625)=0.5546, tanh(1.25)=0.8483 ratio 1.530, tanh(1.875)=0.9542 ratio 1.125
    # Ratio 1.53 close to 2.297? No.
    # Hmm, maybe not tanh. Let's just use piecewise linear with a smooth blend, or fit quadratic on each side.
    # Actually simplest robust: piecewise linear with kink at x=0, using observed values.
    # At x=0 obs 5.42. Left slope -6.76, right slope -16.90.
    # Left: y = 5.42 - 6.76*x (for x<=0). Check x=-3: 5.42+20.28=25.7 (obs 22.67) off by 3
    #   x=-10: 5.42+67.6=73.0 (obs 70.0) off by 3
    #   x=-100: 5.42+676=681.4 (obs 678.4) off by 3
    # So left intercept should be 2.4 not 5.42. But at x=0 obs is 5.42.
    # There's a jump/discontinuity? Or steep transition between -3 and 0.
    # Between x=-3 (22.67) and x=0 (5.42): slope = (5.42-22.67)/3 = -5.75
    # Between x=0 (5.42) and x=5 (-73.29): slope = -15.74
    # So transition happens right around 0. Maybe smooth but sharp.
    # Let's model: y = -11.83*x + 5.42 + C*tanh(x/D) with C/D=-5.07, C=-5.07*D
    # At x=5: -73.29 = -59.15+5.42 -5.07*D*tanh(5/D)
    #   -19.56 = -5.07*D*tanh(5/D) => D*tanh(5/D) = 3.858
    # At x=10: -44.92 = -5.07*D*tanh(10/D) => D*tanh(10/D) = 8.860
    # At x=15: -70.27 = -5.07*D*tanh(15/D) => D*tanh(15/D) = 13.86
    # Try D=4: 4*tanh(1.25)=4*0.848=3.39 (need 3.858), 4*tanh(2.5)=4*0.987=3.95 (need 8.86) no
    # Try D=6: 6*tanh(0.833)=6*0.682=4.09 (need 3.858 close), 6*tanh(1.667)=6*0.931=5.59 (need 8.86) no
    # Hmm the growth is faster than tanh. Maybe it's not tanh.
    # Let's just do piecewise linear with a small transition region, or accept the kink.
    # Given MLP, likely smooth. But piecewise linear is a good approximation.
    # Best fit: left y = -6.76*x + 2.4 for x < 0, right y = -16.90*x + 11.2 for x >= 0.
    # At x=0 this gives 2.4 vs 11.2, avg 6.8 vs obs 5.42. Reasonable.
    # Let's use a blend near 0: linear interp between x=-3 and x=5 using observed slopes.
    # Actually simplest: use the two lines, and for x in [-3,5] interpolate.
    # Even simpler: just use piecewise linear with kink at x=0.5 (intersection-ish).
    # Let's just do: if x <= 0: y = -6.76*x + 2.4 else y = -16.90*x + 11.2
    # Check E1: x=88.2: -16.90*88.2+11.2 = -1490.6+11.2 = -1479.4 (obs -1479.38) 
    # x=66: -1115.4+11.2 = -1104.2 (obs -1104.2) 
    # x=-20.3: 137.2+2.4 = 139.6 (obs 139.62) 
    # x=-61.7: 417.1+2.4 = 419.5 (obs 419.49) 
    # x=2.9: -49.0+11.2 = -37.8 (obs -37.79) 
    # x=-24.3: 164.3+2.4 = 166.7 (obs 166.66) 
    # x=72.7: -1228.6+11.2 = -1217.4 (obs -1217.43) 
    # x=-50.4: 340.7+2.4 = 343.1 (obs 343.10) 
    # x=-6: 40.6+2.4 = 43.0 (obs 42.95) 
    # x=21.3: -360.0+11.2 = -348.8 (obs -348.78) 
    # PERFECT. So it's exactly piecewise linear with kink at x=0!
    # Left: y = -6.76*x + 2.4, Right: y = -16.90*x + 11.2
    # At x=0, which branch? Obs 5.42. Neither. Maybe there's a small transition.
    # But E1 doesn't test x=0. E2 does: obs 5.42.
    # Let's check: maybe the kink is at x=0 but with a small smooth blend.
    # Or maybe the true function is: y = -6.76*x+2.4 for x<0, -16.90*x+11.2 for x>0, and at 0 it's 5.42.
    # Actually maybe it's a smooth function that's approximately these lines.
    # Let's just use piecewise linear and for x=0 use 5.42 (or blend).
    # To be safe, blend linearly in [-3, 5] between the two lines? 
    # At x=-3: left gives 22.68 (obs 22.67) good.
    # At x=5: right gives -73.3 (obs -73.29) good.
    # So the transition is between -3 and 5. Let's linearly interpolate y between x=-3 and x=5.
    # Actually at x=0, linear interp between (-3,22.67) and (5,-73.29): 
    #   y = 22.67 + (0-(-3))/(5-(-3))*(-73.29-22.67) = 22.67 + 3/8*(-95.96) = 22.67-35.99 = -13.3
    # That's not 5.42. So not linear interp.
    # The obs at 0 is 5.42, which is close to left line at 0 (2.4) but not right (11.2).
    # Maybe the kink is at x=0.5 or so. Let's find where left and right lines intersect:
    # -6.76x+2.4 = -16.90x+11.2 => 10.14x = 8.8 => x=0.868, y=-3.47
    # Obs at 0 is 5.42, at 5 is -73.29. Line through (0,5.42) and (5,-73.29): slope -15.74
    # Hmm.
    # Let's just use: for x <= 0: left line; for x > 0: right line. At x=0 use 5.42.
    # Actually simplest: use left line for x<=0, right line for x>0, but at x=0 use 5.42.
    # Or better: use a smooth transition. But piecewise is fine for exam.
    # Let me just special-case x=0 to 5.42, and use piecewise linear otherwise.
    # Actually, maybe the function is y = -6.76*x + 2.4 + (-10.14)*max(0,x) ... no that's piecewise.
    # Let's check: -6.76*x+2.4 for x<0, -16.90*x+11.2 for x>0. At x=0, left=2.4, right=11.2.
    # Obs 5.42 is between. Maybe there's a small sigmoid transition.
    # For exam purposes, piecewise linear with x=0 -> 5.42 should be good.
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            if x < 0:
                y = -6.76*x + 2.4
            elif x > 0:
                y = -16.90*x + 11.2
            else:
                y = 5.4186
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
