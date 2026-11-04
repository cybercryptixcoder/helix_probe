def predict(probe):
    # f is smooth, monotone decreasing, S-shaped (sigmoid-like) [E1, E2]
    # f(0) ≈ -8.8 (between -7.09 at -0.5 and -10.57 at 0.5) [E2]
    # Slope near 0 is steep: ~ -3.3/unit [E2]
    # Saturates toward ~ -65 at large +x, ~ +42 at large -x [E1]
    # Symmetric-ish sigmoid: f(x) ≈ c - A*tanh(x/s) with c≈-11, A≈53, s≈?
    # Fit tanh: at x=0, f=-8.8 => c=-8.8. At x=14, f=-39.78 => A*tanh(14/s)=30.98
    #   At x=-12, f=14.33 => A*tanh(12/s)=23.13
    #   At x=88.2, f=-63.96 => A*tanh(88.2/s)=55.16
    #   At x=-61.7, f=40.81 => A*tanh(61.7/s)=49.61
    # Try A=60: tanh(88.2/s)=0.919=>88.2/s=1.59=>s=55.5
    #   tanh(61.7/55.5)=tanh(1.11)=0.805=>48.3 (obs 49.6) ok
    #   tanh(14/55.5)=tanh(0.252)=0.247=>14.8 (obs 31.0) too low
    # Not pure tanh. Steeper near 0 than tanh with that scale.
    # Try logistic-like: f(x) = c - A*(2/(1+exp(-x/s))-1) same as tanh.
    # Maybe two scales: steep near 0, gentle tail. Use sum of two tanh?
    # f(x) = c - A1*tanh(x/s1) - A2*tanh(x/s2)
    # Near 0 slope: -(A1/s1 + A2/s2) ≈ -3.3
    # At x=14: A1*tanh(14/s1)+A2*tanh(14/s2) = 30.98
    # At x=88.2: A1+A2 ≈ 55.16 (both saturated)
    # At x=-12: A1*tanh(12/s1)+A2*tanh(12/s2) = 23.13
    # At x=-61.7: A1+A2 ≈ 49.61 (slightly less, so not fully saturated)
    # Try s1=4, s2=40, A1+A2=56:
    #   slope: A1/4 + A2/40 = 3.3 => 10*A1+A2=132 => 9*A1=76 => A1=8.4, A2=47.6
    #   x=14: 8.4*tanh(3.5)+47.6*tanh(0.35)=8.4*0.998+47.6*0.336=8.38+16.0=24.4 (obs 31) low
    # Try s1=6, s2=30, A1+A2=56:
    #   A1/6+A2/30=3.3 => 5A1+A2=99 => 4A1=43 => A1=10.75, A2=45.25
    #   x=14: 10.75*tanh(2.33)+45.25*tanh(0.467)=10.75*0.981+45.25*0.436=10.55+19.7=30.3 (obs 31.0) good!
    #   x=-12: 10.75*tanh(2)+45.25*tanh(0.4)=10.75*0.964+45.25*0.380=10.36+17.2=27.6 (obs 23.1) high
    #   x=88.2: 10.75+45.25*tanh(2.94)=10.75+45.25*0.994=55.7 (obs 55.2) good
    #   x=-61.7: 10.75+45.25*tanh(2.06)=10.75+45.25*0.968=54.5 (obs 49.6) high
    # Asymmetric: negative side saturates lower. Add offset c and asymmetry.
    # Let's fit c, A1, A2, s1, s2, and asym via different A for pos/neg.
    # Simpler: f(x) = c - A*tanh(x/s) with c, A, s fit to data.
    # Data: (0,-8.8),(0.5,-10.57),(1,-12.24),(2,-15.58),(4,-22.24),(7,-31.51),
    #   (10,-36.40),(14,-39.78),(21.3,-45.81),(66,-59.96),(88.2,-63.96)
    #   (-0.5,-7.09),(-1.5,-3.85),(-3,-0.07),(-4.5,3.44),(-6.5,7.66),(-9,12.08),
    #   (-12,14.33),(-20.3,18.75),(-24.3,20.88),(-50.4,34.80),(-61.7,40.81)
    # Positive side reaches -63.96 at 88.2; negative reaches 40.81 at -61.7.
    # Asymmetric: positive saturates ~ -66, negative ~ +42.
    # Model: f(x) = c - A*tanh(x/s) for x>=0, c - B*tanh(x/s') for x<0
    # with c≈-8.8. Positive: A*tanh(x/s) = f-c... at x=0.5: A*tanh(0.5/s)=1.77
    #   at x=14: A*tanh(14/s)=30.98; at x=88.2: A*tanh(88.2/s)=55.16
    #   ratio 55.16/30.98=1.78. Try s=20: tanh(4.41)=0.9997, tanh(0.7)=0.604 => ratio 1.65
    #   Try s=25: tanh(3.53)=0.998, tanh(0.56)=0.508 => ratio 1.96
    #   Try s=22: tanh(4.01)=0.9993, tanh(0.636)=0.562 => ratio 1.78 good!
    #   A = 55.16/0.9993 = 55.2. Check x=0.5: 55.2*tanh(0.0227)=55.2*0.0227=1.25 (obs 1.77) low
    #   Check x=2: 55.2*tanh(0.0909)=55.2*0.0907=5.0 (obs 6.78) low
    #   Check x=4: 55.2*tanh(0.182)=55.2*0.180=9.9 (obs 13.44) low
    #   Check x=7: 55.2*tanh(0.318)=55.2*0.308=17.0 (obs 22.71) low
    #   Check x=10: 55.2*tanh(0.455)=55.2*0.426=23.5 (obs 27.6) low
    #   Check x=21.3: 55.2*tanh(0.968)=55.2*0.748=41.3 (obs 37.0) high
    # Not great. Try sum of two tanh on positive side.
    # f(x)-c = A1*tanh(x/s1)+A2*tanh(x/s2), A1+A2=55.2
    # x=0.5: A1*0.5/s1+A2*0.5/s2=1.77 => A1/s1+A2/s2=3.54
    # x=14: A1*tanh(14/s1)+A2*tanh(14/s2)=30.98
    # x=88.2: A1+A2=55.16
    # Try s1=3, s2=30: A1/3+A2/30=3.54 => 10A1+A2=106.2 => 9A1=51 => A1=5.67,A2=49.5
    #   x=14: 5.67*tanh(4.67)+49.5*tanh(0.467)=5.67+49.5*0.436=5.67+21.6=27.3 (obs 31) low
    # Try s1=4, s2=25: A1/4+A2/25=3.54 => 25A1+4A2=354 => 25A1+4(55.2-A1)=354 => 21A1=133.2 => A1=6.34,A2=48.9
    #   x=14: 6.34*tanh(3.5)+48.9*tanh(0.56)=6.33+48.9*0.508=6.33+24.8=31.2 (obs 31.0) good!
    #   x=2: 6.34*tanh(0.5)+48.9*tanh(0.08)=6.34*0.462+48.9*0.0799=2.93+3.91=6.84 (obs 6.78) good!
    #   x=4: 6.34*tanh(1)+48.9*tanh(0.16)=6.34*0.762+48.9*0.159=4.83+7.78=12.6 (obs 13.44) close
    #   x=7: 6.34*tanh(1.75)+48.9*tanh(0.28)=6.34*0.941+48.9*0.273=5.97+13.35=19.3 (obs 22.71) low
    #   x=10: 6.34*tanh(2.5)+48.9*tanh(0.4)=6.34*0.987+48.9*0.380=6.26+18.6=24.8 (obs 27.6) low
    #   x=21.3: 6.34+48.9*tanh(0.852)=6.34+48.9*0.692=6.34+33.8=40.2 (obs 37.0) high
    # Meh. Try s1=5, s2=22: A1/5+A2/22=3.54 => 22A1+5A2=389.4 => 22A1+5(55.2-A1)=389.4 => 17A1=113.4 => A1=6.67,A2=48.5
    #   x=14: 6.67*tanh(2.8)+48.5*tanh(0.636)=6.67*0.993+48.5*0.562=6.62+27.3=33.9 (obs 31) high
    #   x=7: 6.67*tanh(1.4)+48.5*tanh(0.318)=6.67*0.885+48.5*0.308=5.90+14.9=20.8 (obs 22.7) close
    #   x=10: 6.67*tanh(2)+48.5*tanh(0.455)=6.67*0.964+48.5*0.426=6.43+20.7=27.1 (obs 27.6) good
    #   x=21.3: 6.67+48.5*tanh(0.968)=6.67+48.5*0.748=6.67+36.3=43.0 (obs 37.0) high
    #   x=4: 6.67*tanh(0.8)+48.5*tanh(0.182)=6.67*0.664+48.5*0.180=4.43+8.73=13.2 (obs 13.44) good
    #   x=2: 6.67*tanh(0.4)+48.5*tanh(0.0909)=6.67*0.380+48.5*0.0907=2.53+4.40=6.93 (obs 6.78) good
    #   x=0.5: 6.67*tanh(0.1)+48.5*tanh(0.0227)=6.67*0.0997+48.5*0.0227=0.665+1.10=1.77 (obs 1.77) 
    #   x=88.2: 6.67+48.5*tanh(4.01)=6.67+48.5*0.9993=55.1 (obs 55.16) good
    #   x=66: 6.67+48.5*tanh(3)=6.67+48.5*0.995=54.9 (obs 51.16) high by 3.7
    #   x=72.7: 6.67+48.5*tanh(3.30)=6.67+48.5*0.997=55.0 (obs 52.36) high
    # Hmm positive side at 66-72 obs is lower than model. Maybe A2 smaller.
    # Let's just fit numerically-ish. Actually let's use a cleaner approach:
    # f(x) = c - A*tanh(x/s) - B*tanh(x/t) with c=-8.8
    # Positive: A+B=55.16 (at 88.2), slope at 0: A/s+B/t=3.54
    # At x=14: A*tanh(14/s)+B*tanh(14/t)=30.98
    # At x=66: A*tanh(66/s)+B*tanh(66/t)=51.16
    # At x=21.3: A*tanh(21.3/s)+B*tanh(21.3/t)=37.0
    # Try s=5, t=22, A=6.67, B=48.5: x=66 gives 54.9 vs 51.16. 
    # Reduce B, increase A? A+B=55.16. If A=10, B=45.16:
    #   slope: 10/5+45.16/22=2+2.05=4.05 (need 3.54) too steep
    # Try s=6, t=25, A=10, B=45.16: slope 1.67+1.81=3.48 close
    #   x=14: 10*tanh(2.33)+45.16*tanh(0.56)=9.81+45.16*0.508=9.81+22.9=32.7 (obs 31) ok
    #   x=66: 10+45.16*tanh(2.64)=10+45.16*0.990=54.7 (obs 51.16) high
    #   x=21.3: 10*tanh(3.55)+45.16*tanh(0.852)=10+45.16*0.692=10+31.3=41.3 (obs 37) high
    # The tail is lower than tanh predicts. Maybe use a different saturating function.
    # Actually the data at 66,72.7,88.2: -59.96,-61.16,-63.96. Slope ~ -0.18.
    # At 21.3: -45.81. Between 21.3 and 66: slope -0.317.
    # At 14: -39.78. Between 14 and 21.3: slope -0.82.
    # At 10: -36.40. Between 10 and 14: slope -0.845.
    # At 7: -31.51. Between 7 and 10: slope -1.63.
    # At 4: -22.24. Between 4 and 7: slope -3.09.
    # At 2: -15.58. Between 2 and 4: slope -3.33.
    # At 1: -12.24. Between 1 and 2: slope -3.33.
    # At 0.5: -10.57. Between 0.5 and 1: slope -3.34.
    # So slope is ~-3.3 near 0, decreasing gradually. This is like a Gaussian-ish
    # or a smooth step. tanh with s~? slope at 0 = A/s. If A=55, s=16.7 for slope 3.3.
    #   x=14: 55*tanh(0.838)=55*0.685=37.7 (obs 30.98) high
    #   x=4: 55*tanh(0.24)=55*0.235=12.9 (obs 13.44) good
    #   x=7: 55*tanh(0.419)=55*0.396=21.8 (obs 22.71) good
    #   x=10: 55*tanh(0.599)=55*0.536=29.5 (obs 27.6) close
    #   x=21.3: 55*tanh(1.275)=55*0.855=47.0 (obs 37.0) high
    #   x=66: 55*tanh(3.95)=55*0.999=55.0 (obs 51.16) high
    # Tail too high. Need slower saturation. Maybe f = c - A*x/sqrt(1+(x/s)^2)?
    # That's like x/sqrt(1+x^2) which saturates. slope at 0 = A/s.
    # A=55, s=16.7: x=14: 55*14/sqrt(1+0.702)=55*14/1.305=55*10.73=590 no.
    # Actually A*x/sqrt(s^2+x^2): x=14: 55*14/sqrt(279+196)=55*14/21.8=35.3 (obs 31) high
    #   x=4: 55*4/sqrt(279+16)=55*4/17.2=12.8 (obs 13.44) good
    #   x=21.3: 55*21.3/sqrt(279+454)=55*21.3/27.1=43.2 (obs 37) high
    #   x=66: 55*66/sqrt(279+4356)=55*66/68.1=53.3 (obs 51.16) close
    #   x=88.2: 55*88.2/sqrt(279+7779)=55*88.2/89.8=54.0 (obs 55.16) close
    # Better on tail. Try s=20: slope 55/20=2.75 (need 3.3). A=66,s=20: slope 3.3
    #   x=14: 66*14/sqrt(400+196)=66*14/24.4=37.9 (obs 31) high
    # Hmm. Let's just use the two-tanh fit and accept some error, or use
    # a piecewise approach with the actual data points as anchors.
    # Given the exam is on sealed probes, a smooth interpolation through
    # observed points is safest. Use monotone cubic-ish via linear interp
    # with fine grid from the data. Actually linear interp through the
    # dense E2 points plus E1 points should be quite good.
    # Let me build a sorted anchor list from all data and linearly interpolate.
    # E2 gives dense coverage near 0; E1 gives far points.
    # Anchors (x, y):
    pts = [
        (-61.7, 40.8138), (-50.4, 34.7953), (-24.3, 20.881), (-20.3, 18.7483),
        (-12.0, 14.3263), (-9.0, 12.075), (-6.5, 7.6615), (-6.0, 6.6373),
        (-4.5, 3.4383), (-3.0, -0.0686), (-1.5, -3.8538), (-0.5, -7.0942),
        (0.5, -10.5679), (1.0, -12.242), (2.0, -15.5757), (2.9, -18.576),
        (4.0, -22.2431), (7.0, -31.5088), (10.0, -36.3993), (14.0, -39.7849),
        (21.3, -45.8131), (66.0, -59.9589), (72.7, -61.1649), (88.2, -63.955),
    ]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x <= xs[0]:
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
