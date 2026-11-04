def predict(probe):
    # Hypothesis: f(x) is roughly linear with negative slope.
    # From E1: as x increases, y decreases (e.g. x=88.2 -> y=-63.96, x=-61.7 -> y=40.81).
    # Fit slope/intercept from E1 points.
    # Points: (88.2,-63.955),(66.0,-59.9589),(-20.3,18.7483),(-61.7,40.8138),
    #         (2.9,-18.576),(-24.3,20.881),(72.7,-61.1649),(-50.4,34.7953),
    #         (-6.0,6.6373),(21.3,-45.8131)
    # Slope approx: use endpoints (88.2,-63.955) and (-61.7,40.8138):
    #   slope = (40.8138 - (-63.955)) / (-61.7 - 88.2) = 104.7688 / -149.9 ≈ -0.699
    # Intercept ~ -63.955 - (-0.699)*88.2 ≈ -63.955 + 61.65 ≈ -2.3
    # Check x=2.9: -0.699*2.9 - 2.3 ≈ -4.33, observed -18.576. Not great.
    # Try least squares quickly with a couple more points.
    # (66,-59.9589): -0.699*66-2.3 = -48.43, obs -59.96. Off.
    # Slope from (66,-59.9589) and (-61.7,40.8138): 100.77/-127.7 ≈ -0.789
    # Intercept: -59.9589 - (-0.789)*66 = -59.9589 + 52.07 = -7.89
    # Check x=2.9: -0.789*2.9 - 7.89 = -10.18, obs -18.576. Still off.
    # Check x=21.3: -0.789*21.3-7.89 = -24.7, obs -45.81. Off.
    # Maybe nonlinear. Let's look: x=2.9 -> -18.6, x=21.3 -> -45.8, x=66 -> -60, x=88.2 -> -64.
    # x=-6 -> 6.6, x=-20.3 -> 18.7, x=-24.3 -> 20.9, x=-50.4 -> 34.8, x=-61.7 -> 40.8.
    # Looks like y ≈ -0.7*x - 2 for large |x|, but steeper near 0? Actually near 0:
    # x=-6 -> 6.6 (slope ~ -1.1), x=2.9 -> -18.6 (slope ~ -6.4 from 0?). Hmm.
    # Maybe y = -x*something? Let's check y/x ratio: 2.9 -> -6.4; 21.3 -> -2.15; 66 -> -0.91; 88.2 -> -0.725.
    # -6 -> -1.1; -20.3 -> -0.92; -24.3 -> -0.86; -50.4 -> -0.69; -61.7 -> -0.66.
    # Ratio approaches ~ -0.7 for large |x|, steeper near 0.
    # Try y = -0.7*x - 2 + something? At x=2.9: -0.7*2.9-2 = -4.03, obs -18.58, diff -14.5.
    # At x=-6: 4.2-2=2.2, obs 6.64, diff 4.4. At x=21.3: -14.91-2=-16.9, obs -45.8, diff -28.9.
    # Hmm, maybe y = -0.7*x - 2 - 0.5*x*|x|/something? 
    # Let's try quadratic: y = a*x^2 + b*x + c.
    # Use three points: (2.9,-18.576), (-6,6.6373), (88.2,-63.955)
    # 8.41a + 2.9b + c = -18.576
    # 36a - 6b + c = 6.6373
    # 7779.24a + 88.2b + c = -63.955
    # Subtract eq1 from eq2: 27.59a - 8.9b = 25.2133
    # Subtract eq1 from eq3: 7770.83a + 85.3b = -45.379
    # From first: b = (27.59a - 25.2133)/8.9 = 3.1a - 2.833
    # Sub: 7770.83a + 85.3*(3.1a - 2.833) = -45.379
    # 7770.83a + 264.43a - 241.65 = -45.379
    # 8035.26a = 196.27 -> a = 0.02443
    # b = 3.1*0.02443 - 2.833 = 0.0757 - 2.833 = -2.757
    # c = -18.576 - 8.41*0.02443 - 2.9*(-2.757) = -18.576 - 0.2055 + 7.995 = -10.786
    # Check x=-20.3: 0.02443*412.09 + (-2.757)*(-20.3) - 10.786 = 10.07 + 55.97 - 10.79 = 55.25, obs 18.75. Way off.
    # So not quadratic. Maybe piecewise or different form.
    # Let's try y = -0.7*x - 2 for |x|>30, and something else near 0.
    # Actually check x=-20.3: -0.7*(-20.3)-2 = 14.21-2=12.21, obs 18.75. diff 6.5.
    # x=-24.3: 17.01-2=15.01, obs 20.88, diff 5.9.
    # x=-50.4: 35.28-2=33.28, obs 34.80, diff 1.5.
    # x=-61.7: 43.19-2=41.19, obs 40.81, diff -0.4.
    # x=66: -46.2-2=-48.2, obs -59.96, diff -11.8.
    # x=72.7: -50.89-2=-52.89, obs -61.16, diff -8.3.
    # x=88.2: -61.74-2=-63.74, obs -63.96, diff -0.2.
    # Hmm asymmetric. Maybe y = -0.7*x - 2 - 0.1*x*|x|/... no.
    # Try y = -0.7*x - 2 + 0.5*sin(x/10)? At x=2.9: sin(0.29)=0.286, +0.14 -> -3.9, no.
    # Let's just do a piecewise linear interpolation from the data points as a first model.
    # But that's memorization-ish. Better: fit a smooth function.
    # Look at differences: y vs x seems like y ≈ -0.7*x - 2 - 0.5*tanh(x/10)*something?
    # At x=2.9: tanh(0.29)=0.28, -0.5*0.28=-0.14, no.
    # Let's try y = -0.7*x - 2 - 0.3*x*exp(-x^2/200)? At x=2.9: -0.3*2.9*exp(-0.042)=-0.87*0.959=-0.83, total -4.86, obs -18.6. No.
    # Maybe the function is y = -0.7*x - 2 - 0.5*x*exp(-x^2/500)? 
    # At x=2.9: -0.5*2.9*exp(-0.0168)=-1.45*0.983=-1.43, total -5.46, no.
    # The deviation at small x is large negative. At x=2.9 diff is -14.5, at x=21.3 diff is -28.9, at x=66 diff -11.8.
    # Peak deviation around x~20-30? At x=21.3 diff -28.9. At x=66 diff -11.8. At x=88 diff -0.2.
    # At negative x: x=-6 diff +4.4, x=-20.3 diff +6.5, x=-24.3 diff +5.9, x=-50.4 diff +1.5, x=-61.7 diff -0.4.
    # So deviation is negative for positive x (peak ~ -29 near x=21), positive for negative x (peak ~ +6.5 near x=-20).
    # Asymmetric. Maybe y = -0.7*x - 2 - 0.5*x*exp(-((x-20)/30)^2)? 
    # At x=21.3: -0.5*21.3*exp(-(1.3/30)^2)=-10.65*0.998=-10.63, total -27.5, obs -45.8. No.
    # Let's try a different base: maybe y = -0.7*x - 2 - 0.5*x*exp(-x^2/1000) for x>0?
    # At x=21.3: -0.5*21.3*exp(-0.4537)=-10.65*0.635=-6.76, total -23.7, obs -45.8. No.
    # Hmm. Let's try y = -0.7*x - 2 - 0.5*x*exp(-x^2/2000)?
    # x=21.3: exp(-0.2268)=0.797, -10.65*0.797=-8.49, total -25.4, obs -45.8. No.
    # Maybe the slope is steeper near 0. Let's fit y = a*x + b for x in [-10,10]: 
    # points (2.9,-18.576), (-6,6.6373). slope = (6.6373-(-18.576))/(-6-2.9)=25.2133/-8.9=-2.833
    # intercept: -18.576 - (-2.833)*2.9 = -18.576+8.216=-10.36
    # So near 0: y ≈ -2.833*x - 10.36. Check x=-6: 16.998-10.36=6.64 ✓. x=2.9: -8.216-10.36=-18.58 ✓.
    # For large |x|: slope ~ -0.7, intercept ~ -2.
    # So maybe y = -0.7*x - 2 + (something that decays). At x=2.9, need extra -14.5. 
    # Extra = -2.133*x - 8.36? At x=2.9: -6.19-8.36=-14.55 ✓. At x=-6: 12.8-8.36=4.44 ✓.
    # So extra ≈ -2.133*x - 8.36 for small x. But that's linear, would grow. Need decay.
    # Maybe extra = -2.133*x*exp(-x^2/200) - 8.36*exp(-x^2/200)?
    # At x=21.3: exp(-0.4537)=0.635, -2.133*21.3*0.635=-28.85, -8.36*0.635=-5.31, total -34.16, obs extra -28.9. Close-ish.
    # At x=66: exp(-21.78)≈0, extra 0, obs extra -11.8. No.
    # Hmm at x=66 extra is -11.8, not 0. So decay is slower.
    # Let's try extra = -2.133*x*exp(-x^2/5000) - 8.36*exp(-x^2/5000)?
    # x=21.3: exp(-0.0907)=0.913, -2.133*21.3*0.913=-41.5, -8.36*0.913=-7.63, total -49.1, obs -28.9. Too much.
    # Maybe extra = -2.133*x*exp(-|x|/30) - 8.36*exp(-|x|/30)?
    # x=21.3: exp(-0.71)=0.492, -2.133*21.3*0.492=-22.35, -8.36*0.492=-4.11, total -26.46, obs -28.9. Close.
    # x=66: exp(-2.2)=0.111, -2.133*66*0.111=-15.63, -8.36*0.111=-0.93, total -16.56, obs -11.8. Close-ish.
    # x=88.2: exp(-2.94)=0.053, -2.133*88.2*0.053=-9.97, -8.36*0.053=-0.44, total -10.4, obs -0.2. Off.
    # Hmm. At x=88.2 extra is -0.2, so decay must be faster for large x.
    # Maybe extra = -2.133*x*exp(-x^2/3000) - 8.36*exp(-x^2/3000)?
    # x=21.3: exp(-0.151)=0.860, -2.133*21.3*0.860=-39.1, -8.36*0.860=-7.19, total -46.3, obs -28.9. Too much.
    # Let's try extra = -2.133*x*exp(-x^2/1000) - 8.36*exp(-x^2/1000)?
    # x=21.3: exp(-0.4537)=0.635, -2.133*21.3*0.635=-28.85, -8.36*0.635=-5.31, total -34.16, obs -28.9. 
    # x=66: exp(-4.356)=0.0129, -2.133*66*0.0129=-1.82, -8.36*0.0129=-0.11, total -1.93, obs -11.8. Off.
    # This is getting complicated. Let me just use a piecewise linear interpolation with a few knots, 
    # which is a legitimate model of a smooth-ish function.
    # Actually, maybe the function is y = -0.7*x - 2 - 0.5*x*exp(-((x-20)/40)^2) ... no.
    # Let me try a simple neural-net-like form: y = A*tanh(B*x + C) + D*x + E.
    # At large |x|, tanh saturates, so y ≈ D*x + E ± A. Slope D ≈ -0.7.
    # At x=88.2: -0.7*88.2 + E + A = -63.955 -> E + A = -2.215
    # At x=-61.7: -0.7*(-61.7) + E - A = 40.8138 -> 43.19 + E - A = 40.81 -> E - A = -2.38
    # So E ≈ -2.3, A ≈ 0.08. Tiny A, so tanh term negligible at large x. 
    # But at small x, tanh is linear: A*B*x. Need slope ~ -2.833 near 0, so A*B ≈ -2.833+0.7 = -2.133.
    # With A=0.08, B ≈ -26.7. Then tanh(-26.7*x + C). At x=2.9: tanh(-77.4+C). For this to be ~ -1, need C large.
    # Hmm, but then at x=21.3: tanh(-568+C) also -1, so y ≈ -0.7*21.3 - 2.3 - 0.08 = -17.3, obs -45.8. No.
    # So tanh with large B doesn't work.
    # Let's try y = -0.7*x - 2.3 + A*tanh(B*(x - x0)).
    # At x=21.3, need extra -28.9: A*tanh(B*(21.3-x0)) = -28.9. So |A| >= 28.9.
    # At x=88.2, extra -0.2: A*tanh(B*(88.2-x0)) = -0.2. So tanh saturates to ~0? No, tanh saturates to ±1.
    # If A=-30, then at x=88.2 need tanh(...) = 0.0067, so B*(88.2-x0) ≈ 0.0067. 
    # At x=21.3 need tanh(...) = 0.963, so B*(21.3-x0) ≈ 2.0.
    # From these: B*(88.2-x0)=0.0067, B*(21.3-x0)=2.0. Subtract: B*66.9 = -1.993 -> B=-0.0298.
    # Then 21.3-x0 = 2.0/-0.0298 = -67.1 -> x0 = 88.4.
    # Check x=66: B*(66-88.4)=-0.0298*(-22.4)=0.667, tanh=0.584, A*tanh=-30*0.584=-17.5, obs extra -11.8. Close-ish.
    # Check x=2.9: B*(2.9-88.4)=-0.0298*(-85.5)=2.55, tanh=0.988, -30*0.988=-29.6, obs extra -14.5. Off.
    # Check x=-6: B*(-6-88.4)=-0.0298*(-94.4)=2.81, tanh=0.993, -29.8, obs extra +4.4. Way off.
    # So not a single tanh.
    # Given time constraints, let me just use a piecewise linear model with knots at the data points,
    # which will at least fit the data and interpolate reasonably. It's a model of a smooth function.
    # Knots: (-61.7,40.8138),(-50.4,34.7953),(-24.3,20.881),(-20.3,18.7483),(-6,6.6373),
    #        (2.9,-18.576),(21.3,-45.8131),(66,-59.9589),(72.7,-61.1649),(88.2,-63.955)
    # For x outside, extrapolate with slope -0.7.
    knots = [(-61.7,40.8138),(-50.4,34.7953),(-24.3,20.881),(-20.3,18.7483),(-6.0,6.6373),
             (2.9,-18.576),(21.3,-45.8131),(66.0,-59.9589),(72.7,-61.1649),(88.2,-63.955)]
    xs = probe.get("x", [])
    out = []
    for x in xs:
        if x is None:
            out.append(None)
            continue
        if x <= knots[0][0]:
            y = knots[0][1] + (-0.7)*(x - knots[0][0])
        elif x >= knots[-1][0]:
            y = knots[-1][1] + (-0.7)*(x - knots[-1][0])
        else:
            for i in range(len(knots)-1):
                x0,y0 = knots[i]; x1,y1 = knots[i+1]
                if x0 <= x <= x1:
                    t = (x-x0)/(x1-x0)
                    y = y0 + t*(y1-y0)
                    break
        out.append(y)
    return {"y": out}
