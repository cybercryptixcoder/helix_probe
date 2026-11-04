def predict(probe):
    # f(x) = x^6 + x^5 + x^4 + x^3 + x^2 + x for x >= 1  [E2,E3,E4,E5,E7]
    #   check x=2: 64+32+16+8+4+2=126? observed 36. NO.
    # Actually let me re-derive. Observed integers:
    #   f(1)=-0.2, f(2)=36, f(3)=913.2, f(4)=6364, f(5)=26805, f(10)=1992220
    #   f(-1)=-12, f(-2)=83.2, f(-3)=1569, f(-4)=9472.8, f(-5)=36730
    #   f(0)=0, f(0.5)=2.9625
    # Try f(x)=x^6+x^5+x^4+x^3+x^2+x: x=2 ->126 (obs 36). No.
    # Try f(x)=x^6 - x^5 + x^4 - x^3 + x^2 - x: x=2 -> 64-32+16-8+4-2=42 (obs 36). Close-ish.
    # Try f(x)=x^6 - x^5 + x^4 - x^3 + x^2 - x + something.
    # x=3: 729-243+81-27+9-3=546 (obs 913.2). No.
    # Let's fit degree 6 to integer points and check half-integers.
    # E4 half-integers: 1.5->-2.0, 2.5->289.3125, 3.5->3002.7, 4.5->15181.5625
    # E4 integers: 6->84676.8, 7->221368, 8->505723.2, 9->1044135
    # E4 negatives: -1.5->-5.4875, -2.5->373.5, -6->109932, -7->276658.2
    # E4 large: -20->145577380, 15->23573820, -15->26137995, 50->33819064500, -50->34880914000
    # Note f(50) vs f(-50): 33819064500 vs 34880914000. Nearly equal! ~x^6.
    # 50^6 = 15625000000. Ratio ~2.16. Hmm.
    # 15^6=11390625, obs 23573820, ratio 2.07. -15^6 same, obs 26137995 ratio 2.29.
    # 20^6=64000000, obs 145577380 ratio 2.27.
    # So leading term ~2.2*x^6? Let's check 10: 2.2*1e6=2.2e6, obs 1992220. ratio 1.99.
    # 5: 2.2*15625=34375, obs 26805. ratio 1.72.
    # Not constant. So not pure x^6.
    # Let me try: f(x) = x^6 + x^5 + x^4 + x^3 + x^2 + x + x^6? = 2x^6+...: x=10: 2000000+111110=2111110 (obs 1992220). Close.
    # x=5: 2*15625+3905=35155 (obs 26805). No.
    # Try f(x) = x^6 + x^5 + x^4 + x^3 + x^2 + x + x^5? = x^6+2x^5+...: x=10: 1e6+2e5+11110=1211110 no.
    # Hmm. Let me just fit degree 6 to integer points via code and check.
    # Actually the KEY new info from E8:
    #   f(x)=0 for -1 < x <= 0  (all of -0.05..-0.95 give -0.0, and 0.0 gives 0.0)
    #   f(-1)=-12, f(-1.1)=-12.1679, f(-0.99)=-0.0
    #   f(0.05)=4.791, f(0.95)=0.1497, f(0.99)=-0.1308
    #   f(1.1)=-1.7077
    # So for x<=0 with |x|<1: f=0. For x=0: f=0.
    # For 0<x<1: some curve. f(0.05)=4.791, f(0.1)=4.5919, ..., f(0.9)=0.5037, f(0.95)=0.1497, f(0.99)=-0.1308
    # So small positive x has a bump starting near 4.79 at 0.05, decreasing to ~0 at 0.95, negative at 0.99.
    # f(1.1)=-1.7077, f(1.5)=-2.0. So it continues down then back up?
    # f(1)=? E2 says -0.2. Wait E2 f(1)=-0.2. But E8 f(0.99)=-0.1308, f(1.1)=-1.7077. So f(1)=-0.2 fits between.
    # Hmm so f is NOT the poly at x=1 either? E2 says f(1)=-0.2.
    # Let's reconsider. Maybe f(x) = x^6 + x^5 + x^4 + x^3 + x^2 + x for |x|>=1 but that gives f(1)=6 not -0.2.
    # So the poly is wrong. Let me actually fit.
    # Let me use E4 integer points 6,7,8,9 and E2 integers to fit degree 6.
    # Points: (0,0),(1,-0.2),(2,36),(3,913.2),(4,6364),(5,26805),(6,84676.8),(7,221368),(8,505723.2),(9,1044135),(10,1992220)
    # That's 11 points, degree 6 overdetermined. Let's see if degree 6 fits.
    # Differences: 36-(-0.2)=36.2; 913.2-36=877.2; 6364-913.2=5450.8; 26805-6364=20441; 84676.8-26805=57871.8; 221368-84676.8=136691.2; 505723.2-221368=284355.2; 1044135-505723.2=538411.8; 1992220-1044135=948085
    # 6th differences should be constant if degree 6. Let me not do by hand.
    # I'll fit in code. But the small-x regime is clearly separate.
    # Let me hypothesize: f(x) = P(x) for |x|>=1 (some poly), and for -1<x<=0 f=0, for 0<x<1 some other curve.
    # E8: f(1.1)=-1.7077, f(1.5)=-2.0, f(2)=36. So there's a dip near 1.5 then rises.
    # Actually f(1)=-0.2, f(1.1)=-1.7077, f(1.5)=-2.0, f(2)=36. So minimum around 1.5.
    # This suggests the poly P has a local min near 1.5. Let's check: if P(x)=x^6+x^5+... no.
    # Let me just fit degree 6 to the integer points and see.
    # I'll do least squares on integers 0..10 plus negatives.
    # Negatives: (-1,-12),(-2,83.2),(-3,1569),(-4,9472.8),(-5,36730),(-6,109932),(-7,276658.2)
    # Let me fit degree 6 to all these integer points (both signs) and check half-integers.
    # Actually maybe the function is: f(x) = x^6 + x^5 + x^4 + x^3 + x^2 + x for x>=1, but that's contradicted.
    # Let me try a different base: maybe f(x) = (x^2+x+1)^3 - something? 
    # (x^2+x+1)^3 at x=2: 7^3=343. obs 36. No.
    # Let me try f(x) = x^6 + x^5 + x^4 + x^3 + x^2 + x + x^4*... 
    # I'll just fit numerically in code. Given the constraints, let me:
    # 1. Fit degree 6 poly to integer points (0,±1..±7, 10, 15, -15, 20, -20, 50, -50) - use all integer data.
    # 2. For -1<x<=0: f=0.
    # 3. For 0<x<1: fit from E6+E4+E8 small positive points.
    # 4. For |x|>=1: use poly.
    # But E8 shows f(1.1)=-1.7077, f(0.99)=-0.1308. If poly at 1.1 gives -1.7077, good.
    # Let me check: is f continuous at x=1? f(0.99)=-0.1308, f(1)=-0.2, f(1.1)=-1.7077. Roughly continuous.
    # So maybe the poly IS valid for x>=1 and the small-x regime is only 0<x<1.
    # And for x<=0, f=0 for -1<x<=0, and poly for x<=-1.
    # Check continuity at x=-1: f(-0.99)=-0.0, f(-1)=-12. Discontinuous! Jump from 0 to -12.
    # Hmm. So at x=-1 there's a jump. And f(-1.1)=-12.1679 (close to -12).
    # So for x<=-1, f is the poly (which gives -12 at -1). For -1<x<=0, f=0.
    # Let me verify poly at -1 = -12. If poly is degree 6 through integers, f(-1)=-12 by construction.
    # OK so plan:
    # - x <= -1: poly
    # - -1 < x <= 0: 0
    # - 0 < x < 1: small curve
    # - x >= 1: poly
    # But wait, is poly valid at x=1? f(1)=-0.2. And at x=1.1 f=-1.7077. Let's see if a single poly fits both.
    # Let me fit degree 6 to integers and check 1.1, 1.5.
    # I'll just do it in code and trust.
    # Actually, let me reconsider the small positive curve. E8: 0.05->4.791, 0.95->0.1497, 0.99->-0.1308.
    # E6: 0.1->4.5919 ... 0.9->0.5037.
    # This looks like it could be a poly. Let me fit degree 5 to all small positive points.
    # Points: (0.05,4.791),(0.1,4.5919),(0.2,4.21),(0.25,4.0205),(0.3,3.8276),(0.4,3.419),(0.45,3.1979),(0.5,2.9625),(0.55,2.7112),(0.6,2.4428),(0.7,1.8536),(0.75,1.5342),(0.8,1.2006),(0.9,0.5037),(0.95,0.1497),(0.99,-0.1308)
    # Fit degree 5 least squares.
    # Also need f(0)=0? But f(0.05)=4.791, so f(0) would be ~4.9 if continuous. But E8 says f(0)=0.0!
    # So there's a jump at x=0: f(0)=0, f(0.05)=4.791. Discontinuous at 0.
    # OK so: x=0 -> 0, 0<x<1 -> small curve, x<=-1 -> poly, -1<x<0 -> 0, x>=1 -> poly.
    # Wait but is f continuous at x=1? f(0.99)=-0.1308, f(1)=-0.2. Close. And poly at 1 = -0.2. So maybe small curve connects to poly at x=1.
    # Let me just fit and check.

    import math

    def solve_linear(A, b):
        n = len(A)
        M = [A[i][:] + [b[i]] for i in range(n)]
        for i in range(n):
            piv = i
            for r in range(i+1, n):
                if abs(M[r][i]) > abs(M[piv][i]):
                    piv = r
            M[i], M[piv] = M[piv], M[i]
            pv = M[i][i]
            if abs(pv) < 1e-14:
                continue
            for j in range(i, n+1):
                M[i][j] /= pv
            for r in range(n):
                if r != i and abs(M[r][i]) > 1e-15:
                    f = M[r][i]
                    for j in range(i, n+1):
                        M[r][j] -= f * M[i][j]
        return [M[i][n] for i in range(n)]

    # Main poly: fit degree 6 to integer points
    # Use points: (0,0),(1,-0.2),(2,36),(3,913.2),(4,6364),(5,26805),(6,84676.8),(7,221368),(8,505723.2),(9,1044135),(10,1992220)
    # negatives: (-1,-12),(-2,83.2),(-3,1569),(-4,9472.8),(-5,36730),(-6,109932),(-7,276658.2)
    # large: (15,23573820),(-15,26137995),(20,145577380),(-20,145577380),(-20,145577380)
    # Wait E4: -20->145577380, 15->23573820, -15->26137995, 50->33819064500, -50->34880914000
    # Let me use degree 6 least squares on all integer points.
    int_pts = [
        (0,0),(1,-0.2),(2,36),(3,913.2),(4,6364),(5,26805),(6,84676.8),(7,221368),
        (8,505723.2),(9,1044135),(10,1992220),
        (-1,-12),(-2,83.2),(-3,1569),(-4,9472.8),(-5,36730),(-6,109932),(-7,276658.2),
        (15,23573820),(-15,26137995),(20,145577380),(-20,145577380),
        (50,33819064500),(-50,34880914000)
    ]
    # degree 6 least squares
    deg = 6
    m = deg + 1
    N = [[0.0]*m for _ in range(m)]
    rhs = [0.0]*m
    for x, y in int_pts:
        pw = [x**k for k in range(m)]
        for i in range(m):
            rhs[i] += pw[i]*y
            for j in range(m):
                N[i][j] += pw[i]*pw[j]
    coef = solve_linear(N, rhs)

    def poly(x):
        return sum(coef[k]*(x**k) for k in range(m))

    # Small positive curve: 0<x<1
    small_pts = [
        (0.05,4.791),(0.1,4.5919),(0.2,4.21),(0.25,4.0205),(0.3,3.8276),(0.4,3.419),
        (0.45,3.1979),(0.5,2.9625),(0.55,2.7112),(0.6,2.4428),(0.7,1.8536),
        (0.75,1.5342),(0.8,1.2006),(0.9,0.5037),(0.95,0.1497),(0.99,-0.1308)
    ]
    sdeg = 5
    sm = sdeg + 1
    SN = [[0.0]*sm for _ in range(sm)]
    srhs = [0.0]*sm
    for x, y in small_pts:
        pw = [x**k for k in range(sm)]
        for i in range(sm):
            srhs[i] += pw[i]*y
            for j in range(sm):
                SN[i][j] += pw[i]*pw[j]
    scoef = solve_linear(SN, srhs)

    def smallpoly(x):
        return sum(scoef[k]*(x**k) for k in range(sm))

    out = []
    for x in probe.get("x", []):
        try:
            if x <= -1:
                y = poly(x)
            elif x <= 0:
                y = 0.0
            elif x < 1:
                y = smallpoly(x)
            else:
                y = poly(x)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
