def predict(probe):
    # Observations suggest f is roughly piecewise-linear with a negative slope
    # in the positive region and positive slope in the negative region,
    # i.e. approximately f(x) ≈ -a*x + b with a sign flip around 0.
    # E1: x=88.2 -> -63.96, x=66 -> -59.96, x=72.7 -> -61.16
    #     x=-61.7 -> 40.81, x=-50.4 -> 34.80, x=-24.3 -> 20.88
    #     x=-20.3 -> 18.75, x=-6 -> 6.64, x=2.9 -> -18.58, x=21.3 -> -45.81
    # Fit: roughly y ≈ -0.9*x + c with a kink near 0 (small x gives
    # larger magnitude than linear extrapolation, suggesting a steeper
    # slope near 0). Best guess: y ≈ -x for |x| small, saturating slope.
    # Model as y = -x * s(x) where s decreases with |x|? Check:
    #   x=2.9 -> -18.58 => ratio 6.4 (steep)
    #   x=21.3 -> -45.81 => ratio 2.15
    #   x=66 -> -59.96 => ratio 0.91
    #   x=88.2 -> -63.96 => ratio 0.73
    #   x=-6 -> 6.64 => ratio 1.11
    #   x=-20.3 -> 18.75 => ratio 0.92
    #   x=-24.3 -> 20.88 => ratio 0.86
    #   x=-50.4 -> 34.80 => ratio 0.69
    #   x=-61.7 -> 40.81 => ratio 0.66
    # Looks like y ≈ -sign(x) * g(|x|) with g saturating ~65-70.
    # Try g(t) = A * tanh(t / B) with A≈70, B≈? 
    #   t=88.2: 70*tanh(88.2/B)=63.96 => tanh=0.914 => 88.2/B≈1.55 => B≈57
    #   t=66: 70*tanh(66/57)=70*tanh(1.158)=70*0.820=57.4 (obs 59.96) close
    #   t=21.3: 70*tanh(0.374)=70*0.357=25.0 (obs 45.81) too low
    # Not tanh. Maybe g(t) = A*t/(B+t)? 
    #   t=88.2: A*88.2/(B+88.2)=63.96
    #   t=66: A*66/(B+66)=59.96
    #   ratio: (88.2/(B+88.2))/(66/(B+66)) = 63.96/59.96=1.0667
    #   88.2*(B+66) = 1.0667*66*(B+88.2)
    #   88.2B+5821.2 = 70.4B+6209.3 => 17.8B=388 => B≈21.8
    #   A = 63.96*(21.8+88.2)/88.2 = 63.96*110/88.2 = 79.8
    # Check t=21.3: 79.8*21.3/(21.8+21.3)=79.8*21.3/43.1=39.4 (obs 45.81) meh
    # Check t=50.4: 79.8*50.4/72.2=55.7 (obs 34.80) way off
    # Hmm, negative side differs from positive side.
    # Positive side: x=2.9->-18.58 (ratio 6.4), x=21.3->-45.81 (2.15),
    #   x=66->-59.96 (0.91), x=72.7->-61.16 (0.84), x=88.2->-63.96 (0.73)
    # Negative side: x=-6->6.64 (1.11), x=-20.3->18.75 (0.92),
    #   x=-24.3->20.88 (0.86), x=-50.4->34.80 (0.69), x=-61.7->40.81 (0.66)
    # Positive side has a steep region near 0; negative side is gentler.
    # Asymmetric. Best guess: piecewise linear fit.
    # Positive: points (2.9,-18.58),(21.3,-45.81),(66,-59.96),(72.7,-61.16),(88.2,-63.96)
    #   slope between 2.9 and 21.3: (-45.81+18.58)/18.4 = -1.48
    #   between 21.3 and 66: (-59.96+45.81)/44.7 = -0.317
    #   between 66 and 88.2: (-63.96+59.96)/22.2 = -0.180
    # Negative: (-6,6.64),(-20.3,18.75),(-24.3,20.88),(-50.4,34.80),(-61.7,40.81)
    #   slope -6 to -20.3: (18.75-6.64)/(-14.3) = -0.847
    #   -20.3 to -50.4: (34.80-18.75)/(-30.1) = -0.533
    #   -50.4 to -61.7: (40.81-34.80)/(-11.3) = -0.532
    # Roughly linear on negative side with slope ~-0.55, intercept ~3.4
    #   check -6: 3.4+3.3=6.7 ok; -20.3: 3.4+11.2=14.6 (obs 18.75) meh
    # Try slope -0.62, intercept 2.9: -6->6.6, -20.3->15.5 (obs 18.75)
    # Not great. Let's just do piecewise linear interpolation through
    # observed points, extrapolating with end slopes. This is a hypothesis.
    xs = [-61.7, -50.4, -24.3, -20.3, -6.0, 2.9, 21.3, 66.0, 72.7, 88.2]
    ys = [40.8138, 34.7953, 20.881, 18.7483, 6.6373, -18.576, -45.8131,
          -59.9589, -61.1649, -63.955]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x <= xs[0]:
            # extrapolate with first segment slope
            m = (ys[1]-ys[0])/(xs[1]-xs[0])
            y = ys[0] + m*(x-xs[0])
        elif x >= xs[-1]:
            m = (ys[-1]-ys[-2])/(xs[-1]-xs[-2])
            y = ys[-1] + m*(x-xs[-1])
        else:
            y = None
            for i in range(len(xs)-1):
                if xs[i] <= x <= xs[i+1]:
                    t = (x-xs[i])/(xs[i+1]-xs[i])
                    y = ys[i] + t*(ys[i+1]-ys[i])
                    break
        out.append(y)
    return {"y": out}
