import math

def predict(probe):
    # Model: piecewise function with breakpoint at x=0.
    # For x < 0: f(x) = a*x^3 + b*x + c  (cubic, no x^2 term) [E1,E3,E6,E11]
    # For x >= 0: f(x) = A*(x+B)*exp(C*x) + D  [E4,E5,E10]
    # Fit coefficients from clean evidence:
    #   Negative side: use large |x| points where cubic dominates.
    #     f(-20) = -112324723.7, f(-10) = -3613822.11, f(-5) = -120306.515
    #   Solve a,b,c.
    #   Positive side: use points to fit A,B,C,D.
    #
    # Negative cubic: a*x^3 + b*x + c
    # Using x=-20: -8000a -20b + c = -112324723.7
    #       x=-10: -1000a -10b + c = -3613822.11
    #       x=-5:   -125a  -5b + c = -120306.515
    # Differences:
    #  (-8000+1000)a + (-20+10)b = -112324723.7 + 3613822.11 = -108710901.59
    #   -7000a -10b = -108710901.59  => 700a + b = 10871090.159
    #  (-1000+125)a + (-10+5)b = -3613822.11 + 120306.515 = -3493515.595
    #   -875a -5b = -3493515.595 => 175a + b = 698703.119
    # Subtract: 525a = 10172387.04 => a = 19375.9753...
    # b = 698703.119 - 175*a
    a = (10871090.159 - 698703.119) / 525.0
    b = 698703.119 - 175.0 * a
    c = -3613822.11 + 1000.0 * a + 10.0 * b

    # Positive side: A*(x+B)*exp(C*x) + D
    # Use points: x=1 -> 70.35, x=2 -> 3782.82, x=3 -> 28401.19, x=4 -> 118359.4
    # Try to fit. Let's estimate C from ratios.
    # f(2)-D ~ A(2+B)e^{2C}, f(1)-D ~ A(1+B)e^{C}
    # Assume D small-ish. Try C ~ 1.0? e^C ~ 2.718
    # f(4)/f(3) = 118359.4/28401.19 = 4.167
    # (4+B)/(3+B) * e^C = 4.167
    # f(3)/f(2) = 28401.19/3782.82 = 7.508
    # (3+B)/(2+B) * e^C = 7.508
    # Ratio: [(4+B)(2+B)]/[(3+B)^2] = 4.167/7.508 = 0.555
    # (8+6B+B^2)/(9+6B+B^2) = 0.555
    # 8+6B+B^2 = 0.555*(9+6B+B^2) = 4.995+3.33B+0.555B^2
    # 0.445B^2 + 2.67B + 3.005 = 0
    # B^2 + 6.0B + 6.753 = 0 => B = (-6 ± sqrt(36-27.01))/2 = (-6 ± 3.0)/2
    # B = -1.5 or B = -4.5
    # Try B = -1.5: (3-1.5)/(2-1.5)*e^C = 1.5/0.5*e^C = 3*e^C = 7.508 => e^C = 2.503 => C = 0.917
    # Check f(4)/f(3): (4-1.5)/(3-1.5)*e^C = 2.5/1.5*2.503 = 4.172 ✓ close
    # So B = -1.5, C = ln(2.503) ~ 0.9175
    # Now A: f(2) = A*(2-1.5)*e^{2C} + D = A*0.5*e^{2C}+D
    # e^{2C} = 2.503^2 = 6.265
    # f(2)=3782.82 = A*0.5*6.265 + D = 3.1325A + D
    # f(1)=70.35 = A*0.5*e^C + D = A*0.5*2.503 + D = 1.2515A + D
    # Subtract: 3712.47 = 1.881A => A = 1973.7
    # D = 70.35 - 1.2515*1973.7 = 70.35 - 2470.1 = -2399.7
    # Hmm D negative. Check f(3): A*1.5*e^{3C}+D = 1973.7*1.5*15.68 - 2399.7 = 46422 - 2399 = 44022, but actual 28401. Off.
    # Let me redo more carefully with least squares-ish. Actually let me just fit numerically.
    # Use exact points and solve. Let me use f(1),f(2),f(3),f(4).
    # Actually, let me reconsider. Maybe D is small and there's noise.
    # Let me try fitting with the cleaner large points and small points.
    # Let me just do a numeric fit here.
    # Points: (0.5,-22.9553),(1,70.35),(1.5,867.6703),(2,3782.82),(3,28401.19),(4,118359.4)
    # Try C from consecutive ratios:
    # r1 = f(1.5)/f(1) = 867.67/70.35 = 12.334 = (1.5+B)/(1+B)*e^{0.5C}
    # r2 = f(2)/f(1.5) = 3782.82/867.67 = 4.360 = (2+B)/(1.5+B)*e^{0.5C}
    # r3 = f(3)/f(2) = 28401.19/3782.82 = 7.508 = (3+B)/(2+B)*e^{C}
    # r4 = f(4)/f(3) = 118359.4/28401.19 = 4.167 = (4+B)/(3+B)*e^{C}
    # r3/r4 = (3+B)(3+B)/((2+B)(4+B)) = 7.508/4.167 = 1.802
    # (3+B)^2 = 1.802*(2+B)(4+B) = 1.802*(8+6B+B^2)
    # 9+6B+B^2 = 14.416+10.812B+1.802B^2
    # 0 = 5.416+4.812B+0.802B^2
    # B^2 + 6.0B + 6.753 = 0 => same as before, B=-1.5 or -4.5
    # B=-1.5: r3 = (1.5)/(0.5)*e^C = 3e^C = 7.508 => e^C=2.503, C=0.9175
    # Check r2: (0.5)/(0.5)*e^{0.5C} = e^{0.4587}=1.582, but actual 4.360. Off!
    # So B=-1.5 fails on r2. Try B=-4.5:
    # r3 = (3-4.5)/(2-4.5)*e^C = (-1.5)/(-2.5)*e^C = 0.6*e^C = 7.508 => e^C = 12.51, C=2.526
    # r2 = (2-4.5)/(1.5-4.5)*e^{0.5C} = (-2.5)/(-3)*e^{1.263} = 0.833*3.54 = 2.95, actual 4.36. Off.
    # Hmm neither fits well. Maybe D matters or noise. Let me include D.
    # Let me just do a proper numeric fit using scipy-free approach.
    # Actually, let me reconsider: maybe the formula is A*(x+B)*exp(C*x)+D with specific nice values.
    # Let me try to fit using the large-x points where D is negligible.
    # f(3)=28401.19, f(4)=118359.4, f(5)=358939.83
    # f(5)/f(4) = 3.032 = (5+B)/(4+B)*e^C
    # f(4)/f(3) = 4.167 = (4+B)/(3+B)*e^C
    # ratio: (5+B)(3+B)/((4+B)^2) = 3.032/4.167 = 0.7276
    # (15+8B+B^2) = 0.7276*(16+8B+B^2) = 11.64+5.82B+0.7276B^2
    # 0.2724B^2 + 2.18B + 3.36 = 0
    # B^2 + 8.0B + 12.33 = 0 => B = (-8±sqrt(64-49.3))/2 = (-8±3.83)/2 => B=-2.08 or -5.92
    # B=-2.08: (4-2.08)/(3-2.08)*e^C = 1.92/0.92*e^C = 2.087*e^C = 4.167 => e^C=1.996, C=0.691
    # Check f(5)/f(4): (5-2.08)/(4-2.08)*e^C = 2.92/1.92*1.996 = 3.036 ✓
    # Good. So B~-2.08, C~0.691. Hmm not clean.
    # Let me try B=-2, C=ln(2)=0.6931:
    # (4-2)/(3-2)*2 = 2*2=4, actual 4.167. Close-ish.
    # Let me try to nail it. Maybe A, B, C, D are specific.
    # Let me use f(0.5)=-22.9553, f(1)=70.35, f(2)=3782.82, f(3)=28401.19
    # With B=-2, C=ln2: f(x)=A(x-2)2^x + D
    # f(1)=A(-1)*2+D = -2A+D = 70.35
    # f(2)=A(0)*4+D = D = 3782.82?? That gives D=3782.82, then -2A = 70.35-3782.82=-3712.47, A=1856.2
    # Check f(3)=A(1)*8+D = 1856.2*8+3782.82=18632.4, actual 28401. Off.
    # Hmm. Let me try B=-1, C=ln2: f(x)=A(x-1)2^x+D
    # f(1)=0+D=D=70.35
    # f(2)=A(1)*4+70.35=3782.82 => 4A=3712.47, A=928.1
    # f(3)=A(2)*8+70.35=928.1*16+70.35=14920, actual 28401. Off.
    # Let me try a different approach: fit log of f for large x.
    # ln f(3)=10.254, ln f(4)=11.681, ln f(5)=12.791
    # diffs: 1.427, 1.110. Not constant, so not pure exp.
    # For A(x+B)e^{Cx}, ln f ~ ln A + ln(x+B) + Cx
    # ln f(4)-ln f(3) = ln((4+B)/(3+B)) + C = 1.427
    # ln f(5)-ln f(4) = ln((5+B)/(4+B)) + C = 1.110
    # Subtract: ln((4+B)(4+B)/((3+B)(5+B))) = 0.317
    # (4+B)^2/((3+B)(5+B)) = e^0.317 = 1.373
    # (16+8B+B^2) = 1.373*(15+8B+B^2) = 20.6+10.98B+1.373B^2
    # 0 = 4.6+2.98B+0.373B^2 => B^2+7.99B+12.33=0 => same, B=-2.08 or -5.92
    # B=-2.08: C = 1.427 - ln((4-2.08)/(3-2.08)) = 1.427 - ln(2.087) = 1.427-0.736=0.691
    # So B≈-2.08, C≈0.691. Hmm. Maybe exact values are B=-2, C=ln(2)? Let me check with D.
    # Let me just fit numerically in code. I'll do a grid/iterative fit.
    # Actually let me reconsider the whole thing. Let me look at f(0)=21.28.
    # f(0)=A*B*1+D = AB+D = 21.28
    # f(1)=A(1+B)e^C+D=70.35
    # f(2)=A(2+B)e^{2C}+D=3782.82
    # f(3)=A(3+B)e^{3C}+D=28401.19
    # f(4)=A(4+B)e^{4C}+D=118359.4
    # 4 equations, 4 unknowns. Let me solve numerically.
    # From f(0): D = 21.28 - AB
    # f(1)-f(0) = A[(1+B)e^C - B] = 70.35-21.28 = 49.07
    # f(2)-f(0) = A[(2+B)e^{2C} - B] = 3761.54
    # f(3)-f(0) = A[(3+B)e^{3C} - B] = 28379.91
    # f(4)-f(0) = A[(4+B)e^{4C} - B] = 118338.12
    # Ratios: (f(2)-f(0))/(f(1)-f(0)) = 76.66 = [(2+B)e^{2C}-B]/[(1+B)e^C-B]
    # (f(3)-f(0))/(f(2)-f(0)) = 7.545 = [(3+B)e^{3C}-B]/[(2+B)e^{2C}-B]
    # (f(4)-f(0))/(f(3)-f(0)) = 4.170 = [(4+B)e^{4C}-B]/[(3+B)e^{3C}-B]
    # This is getting complex. Let me just do a numeric solve in the code.
    # I'll implement a simple fit: guess B, C, solve A,D from two points, check residuals.
    # Let me do a coarse grid search over B in [-6,0], C in [0.3,1.2].
    # Actually, let me just hardcode a reasonable fit and refine.
    # Let me try B=-2, C=0.6931 (ln2):
    # f(0)=A(-2)+D=21.28
    # f(1)=A(-1)(2)+D=-2A+D=70.35 => subtract: (from f0) -2A+D - (-2A+D)... wait f0: -2A+D=21.28, f1: -2A+D=70.35. Contradiction! So B≠-2 exactly.
    # Let me try B=-1.5, C=0.6931:
    # f(0)=A(-1.5)+D=21.28
    # f(1)=A(-0.5)(2)+D=-A+D=70.35 => subtract: 0.5A = 49.07 => A=98.14, D=21.28+1.5*98.14=168.5
    # f(2)=A(0.5)(4)+D=98.14*2+168.5=364.8, actual 3782.82. Way off.
    # Hmm. Let me try C larger. B=-1.5, C=1.0:
    # f(0)=-1.5A+D=21.28
    # f(1)=A(-0.5)e+D=-0.5*2.718A+D=-1.359A+D=70.35 => 0.141A=49.07 => A=348, D=21.28+522=543
    # f(2)=A(0.5)e^2+D=348*0.5*7.389+543=1286+543=1829, actual 3782. Off.
    # B=-1.5, C=1.2:
    # f(1)=-0.5*3.32A+D=-1.66A+D=70.35, f0: -1.5A+D=21.28 => 0.16A=49.07 => A=306.7, D=21.28+460=481
    # f(2)=0.5*e^2.4*A+D=0.5*11.02*306.7+481=1690+481=2171, actual 3782. Off.
    # B=-1.5, C=1.5:
    # f(1)=-0.5*4.48A+D=-2.24A+D=70.35, f0:-1.5A+D=21.28 => 0.74A=49.07 => A=66.3, D=21.28+99.5=120.8
    # f(2)=0.5*e^3*A+D=0.5*20.09*66.3+120.8=666+121=787, actual 3782. Off.
    # Hmm, need larger A. Let me try B more negative.
    # B=-3, C=1.0:
    # f(0)=-3A+D=21.28
    # f(1)=-2*2.718A+D=-5.436A+D=70.35 => 2.436A=49.07 => A=20.14, D=21.28+60.4=81.7
    # f(2)=-1*7.389*A+D=-7.389*20.14+81.7=-148.8+81.7=-67, actual 3782. Off.
    # Hmm. Let me try B=-1, C=1.0:
    # f(0)=-A+D=21.28
    # f(1)=0*e+D=D=70.35 => D=70.35, A=49.07
    # f(2)=1*7.389*49.07+70.35=362.6+70.35=433, actual 3782. Off.
    # Let me try B=0, C=1.0:
    # f(0)=D=21.28
    # f(1)=A*1*2.718+21.28=70.35 => 2.718A=49.07 => A=18.05
    # f(2)=A*2*7.389+21.28=18.05*14.78+21.28=266.8+21.28=288, actual 3782. Off.
    # The growth is much faster. Let me estimate C from f(3)/f(2) and f(4)/f(3) more carefully with D.
    # Actually let me just do a numeric fit in code. I'll write a simple solver.
    # Let me use the points f(1),f(2),f(3),f(4) and solve.
    # I'll do a 2D grid search over B and C, solving A,D linearly.
    # For given B,C: 
    #   f(x) = A*(x+B)*e^{Cx} + D
    #   Let u_i = (x_i+B)*e^{C x_i}
    #   Then f_i = A*u_i + D. Linear least squares for A,D.
    # Then minimize residual over B,C.
    # I'll implement this in code with a coarse grid then refine.
    
    # Let me just write the fit in code.
    pos_data = [(0.5,-22.9553),(1.0,70.35),(1.5,867.6703),(2.0,3782.82),
                (3.0,28401.19),(4.0,118359.4),(5.0,358939.83),(6.0,889935.3)]
    
    best = None
    # coarse grid
    Bv = -6.0
    while Bv <= 0.5:
        Cv = 0.3
        while Cv <= 1.5:
            # linear fit A,D
            us = []
            fs = []
            for (x,y) in pos_data:
                u = (x+Bv)*math.exp(Cv*x)
                us.append(u)
                fs.append(y)
            n = len(us)
            su = sum(us); sf = sum(fs)
            suu = sum(u*u for u in us)
            suf = sum(u*f for u,f in zip(us,fs))
            den = n*suu - su*su
            if abs(den) < 1e-12:
                Cv += 0.02
                continue
            A = (n*suf - su*sf)/den
            D = (sf - A*su)/n
            # residual
            res = 0.0
            for (x,y) in pos_data:
                pred = A*(x+Bv)*math.exp(Cv*x)+D
                res += (pred-y)**2
            if best is None or res < best[0]:
                best = (res, A, Bv, Cv, D)
            Cv += 0.02
        Bv += 0.1
    
    # refine around best
    if best is not None:
        _, A0, B0, C0, D0 = best
        Bv = B0 - 0.15
        while Bv <= B0 + 0.15:
            Cv = C0 - 0.15
            while Cv <= C0 + 0.15:
                us = []; fs = []
                for (x,y) in pos_data:
                    u = (x+Bv)*math.exp(Cv*x)
                    us.append(u); fs.append(y)
                n = len(us)
                su = sum(us); sf = sum(fs)
                suu = sum(u*u for u in us)
                suf = sum(u*f for u,f in zip(us,fs))
                den = n*suu - su*su
                if abs(den) > 1e-12:
                    A = (n*suf - su*sf)/den
                    D = (sf - A*su)/n
                    res = sum((A*(x+Bv)*math.exp(Cv*x)+D-y)**2 for (x,y) in pos_data)
                    if res < best[0]:
                        best = (res, A, Bv, Cv, D)
                Cv += 0.005
            Bv += 0.005
    
    if best is not None:
        _, A, B, C, D = best
    else:
        A, B, C, D = 1.0, -1.0, 1.0, 0.0

    def f(x):
        if x < 0:
            return a*x*x*x + b*x + c
        else:
            return A*(x+B)*math.exp(C*x) + D

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(f(x))
        except Exception:
            ys.append(None)
    return {"y": ys}
