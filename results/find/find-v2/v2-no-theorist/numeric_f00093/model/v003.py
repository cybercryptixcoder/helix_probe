def predict(probe):
    # f is monotone decreasing over the whole domain [E1, E2, E3]
    # f(0) ≈ -8.83, negative offset; odd-ish: f(-x) ≈ -f(x) - 17.7 [E2]
    # Slope near 0 steep: f(1)-f(-1) ≈ -6.87, f(2)-f(-2) ≈ -13.0 [E2]
    # Slope flattens at large |x|: f(100)-f(80) ≈ 10.65, f(120)-f(100) ≈ 3.6 [E2]
    # At x=120, f≈-69.68; at x=-100, f≈61.21 -> saturation ~±70 [E2]
    # E3 shows near-saturation already at x≈104 (f≈-66.9) and x≈-64 (f≈42)
    # Model: f(x) = c - A * tanh(x / s), c≈-4.2, A≈65.4, s≈? 
    # Mid-range: f(20)=-44.75, f(-20)=18.59 -> center -13.08, half-span 31.67
    #   tanh(20/s) = 31.67/65.4 = 0.484 -> 20/s = 0.527 -> s ≈ 38
    # f(40)=-53.52: (53.52-4.2)/65.4=0.754 -> 40/s=0.98 -> s≈41
    # f(10)=-36.40: (36.40-4.2)/65.4=0.492 -> 10/s=0.539 -> s≈18.6 (inconsistent)
    # Better: use a two-parameter fit. Try c=-4.2, A=65.4, s=30
    # Check f(10): -4.2-65.4*tanh(0.333)=-4.2-65.4*0.321=-25.2 (obs -36.4, too shallow)
    # The shape is steeper near 0 than tanh with s=30. Try s=22:
    # f(10)=-4.2-65.4*tanh(0.455)=-4.2-65.4*0.426=-32.1 (obs -36.4)
    # f(20)=-4.2-65.4*tanh(0.909)=-4.2-65.4*0.720=-51.3 (obs -44.75, too steep)
    # So tanh doesn't fit well; use a piecewise-linear-ish / arctan shape
    # Try f(x) = c - A * (2/pi) * atan(x/s):
    # f(20)=-44.75: (44.75-4.2)/65.4=0.620 -> atan(20/s)=0.974 -> 20/s=1.44 -> s≈13.9
    # f(10)=-36.4: (36.4-4.2)/65.4=0.492 -> atan(10/s)=0.773 -> 10/s=0.973 -> s≈10.3
    # f(40)=-53.5: (53.5-4.2)/65.4=0.754 -> atan(40/s)=1.184 -> 40/s=2.43 -> s≈16.5
    # arctan also inconsistent. The real curve is roughly linear in mid-range.
    # E2 differences: f(0)-f(-20)=26.4 over 20 -> slope 1.32
    #   f(-20)-f(-40)=10.67 over 20 -> slope 0.53
    #   f(20)-f(40)=8.77 over 20 -> slope 0.44
    #   f(40)-f(60)=5.36 -> 0.27; f(60)-f(80)=3.6 -> 0.18; f(80)-f(100)=3.6 -> 0.18
    #   f(-40)-f(-60)=10.65 -> 0.53; f(-60)-f(-80)=10.65 -> 0.53; f(-80)-f(-100)=10.65 -> 0.53
    # Interesting: on negative side slope is constant 0.53 from -40 to -100!
    # On positive side slope decays: 0.44, 0.27, 0.18, 0.18
    # This suggests asymmetry / different saturation on each side.
    # Negative side: f(-100)=61.21, f(-40)=29.26 -> slope 0.53 constant
    #   extrapolate: f(-128)=61.21+0.53*28=76.05
    # Positive side: f(100)=-66.08, f(120)=-69.68 -> slope 0.18
    #   f(128)=-69.68-0.18*8=-71.1
    # Center: f(0)=-8.83, slope near 0 ~3.4 (from f(1)-f(-1)=-6.87)
    # Build piecewise: 
    #   |x|<=2: steep, slope ~3.4
    #   2<|x|<=20: transition
    #   negative side beyond -40: linear slope 0.53
    #   positive side beyond 40: decaying to slope 0.18
    # Use a smooth blend: f(x) = c - A*tanh(x/s) with different s for sign? 
    # Simpler: f(x) = c - A * tanh(x/s_pos) for x>0, c - A*tanh(x/s_neg) for x<0
    # But f(0)=-8.83 means c=-8.83. Then A from saturation: 
    #   pos: -8.83 - A*tanh(120/s_pos) = -69.68 -> A*tanh(...) = 60.85
    #   neg: -8.83 - A*tanh(-100/s_neg) = 61.21 -> A*tanh(100/s_neg)=70.04
    # Asymmetric A too. Let's use separate A_pos, A_neg.
    # pos: A_pos*tanh(120/s_pos)=60.85; at x=100: A_pos*tanh(100/s_pos)=57.25
    #   ratio tanh(120/s)/tanh(100/s)=1.063 -> s_pos large, ~? 
    #   if s_pos=80: tanh(1.5)=0.905, tanh(1.25)=0.848, ratio 1.067 ✓
    #   A_pos=60.85/0.905=67.2. Check x=40: 67.2*tanh(0.5)=67.2*0.462=31.05 -> f=-39.9 (obs -53.5) ✗
    # tanh too shallow mid-range. Need steeper center.
    # Try f(x) = c - A * erf(x/s) style, or use a logistic with sharp center.
    # Given difficulty, use interpolation-style: piecewise linear through E2 knots,
    # extrapolate linearly beyond. This is a mechanism model (the curve shape).
    # Knots from E2 (x, y):
    knots = [(-128, 76.05),(-100,61.2126),(-80,50.5605),(-60,39.9084),(-40,29.2562),
             (-20,18.5887),(-10,13.1151),(-5,4.5567),(-2,-2.5588),(-1,-5.3751),
             (0,-8.8302),(1,-12.242),(2,-15.5757),(5,-25.4152),(10,-36.3993),
             (20,-44.7483),(40,-53.5169),(60,-58.8789),(80,-62.479),(100,-66.079),
             (120,-69.6791),(128,-71.12)]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x <= knots[0][0]:
                out.append(knots[0][1])
            elif x >= knots[-1][0]:
                out.append(knots[-1][1])
            else:
                for i in range(len(knots)-1):
                    x0,y0 = knots[i]; x1,y1 = knots[i+1]
                    if x0 <= x <= x1:
                        t = (x-x0)/(x1-x0)
                        out.append(y0 + t*(y1-y0))
                        break
        except Exception:
            out.append(None)
    return {"y": out}
