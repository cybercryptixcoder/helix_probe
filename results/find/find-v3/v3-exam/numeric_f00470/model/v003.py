import math

def predict(probe):
    # Beliefs:
    # B1. For |x| large (say |x| > ~3), f(x) ≈ sign(x) * C * |x|^5, but with
    #     different coefficients on each side: positive ~113.8, negative ~34.5 [E1,E2,E3].
    # B2. Near x=0 the function is NOT small: f(0)=21.28, and |f| stays O(10-30)
    #     for |x| <= ~1 [E4]. So there is a "small-x region" with a different rule.
    # B3. In the small-x region the values look like a smooth curve with a
    #     constant-ish offset ~21 plus wiggles; positive and negative sides differ.
    #     Positive side: 0.05->15.4, 0.1->10.4, 0.2->2.54, 0.3->-5.9, 0.4->-16.1,
    #     0.5->-22.96, 0.6->-22.65, 0.7->-17.83, 0.8->-5.33, 0.9->23.99, 1.0->71.35.
    #     Negative side: -0.05->22.61, -0.1->22.85, -0.2->24.95, -0.3->27.38,
    #     -0.5->25.69, -0.7->16.83, -0.9->-11.13, -1.0->-34.09.
    # B4. The transition between small-x region and power-law region is somewhere
    #     around |x| ~ 1-3. At x=1.2 (E3) y=249.2, at x=2 (E2) y=3783.8, at x=2.9
    #     y=24006. So the power-law takes over quickly above x~1.
    # B5. Hypothesis: f(x) = P(x) + S(x) where P is the odd power-law part and S is
    #     a small-x "bump" that decays. But E4 shows f(0)=21.28 nonzero, so there
    #     is a genuine additive constant/offset near 0. Perhaps f(x) = g(x) + h(x)
    #     where h is a localized bump around 0.
    #
    # Let's model: f(x) = sign(x)*C_side*|x|^5 + bump(x), where bump is a smooth
    # function localized to |x| < ~1.5, fit from E4 plus the small-x points in E2/E3.
    #
    # Actually simpler: fit a piecewise polynomial. For |x| >= x0 use the power law
    # (with small correction). For |x| < x0 use a polynomial fit to E4 + nearby.
    #
    # Let's look at E4 more carefully. The values are NOT symmetric. Let's try
    # fitting each side separately with a low-degree polynomial in x over |x|<=1.
    #
    # Positive small-x points (x, y):
    #   (0.05,15.3992),(0.1,10.4473),(0.2,2.5408),(0.3,-5.9163),(0.4,-16.1413),
    #   (0.5,-22.9553),(0.6,-22.6466),(0.7,-17.834),(0.8,-5.3302),(0.9,23.9947),
    #   (1.0,71.35)
    # Negative small-x points:
    #   (-0.05,22.6125),(-0.1,22.8483),(-0.2,24.9533),(-0.3,27.3822),
    #   (-0.5,25.692),(-0.7,16.8289),(-0.9,-11.1291),(-1.0,-34.091)
    # f(0)=21.28.
    #
    # These look like they could be a Gaussian bump plus a linear/quadratic trend.
    # Positive side: rises to ~ -23 at x=0.5, then shoots up to 71 at x=1.
    # Negative side: ~22-27 for small |x|, drops to -34 at x=-1.
    #
    # Hmm, the positive side at x=1 is 71.35, and the power law 113.8*x^5 = 113.8.
    # So there's a deficit. At x=1.2, power law gives 283, observed 249. Deficit 34.
    # At x=2, power law 3641, observed 3783 — excess 142. So the bump changes sign.
    #
    # Let's try: f(x) = C_pos * x^5 + B(x) where B is a bump. Then
    # B(x) = f(x) - 113.8*x^5 for positive x.
    #   x=0.05: 15.3992 - 113.8*3.125e-7 ≈ 15.3992
    #   x=0.1: 10.4473 - 113.8*1e-5 ≈ 10.4462
    #   x=0.2: 2.5408 - 113.8*3.2e-4 ≈ 2.5044
    #   x=0.3: -5.9163 - 113.8*0.00243 ≈ -6.1928
    #   x=0.4: -16.1413 - 113.8*0.01024 ≈ -17.3063
    #   x=0.5: -22.9553 - 113.8*0.03125 ≈ -26.5116
    #   x=0.6: -22.6466 - 113.8*0.07776 ≈ -31.4939
    #   x=0.7: -17.834 - 113.8*0.16807 ≈ -36.9604
    #   x=0.8: -5.3302 - 113.8*0.32768 ≈ -42.6204
    #   x=0.9: 23.9947 - 113.8*0.59049 ≈ -43.1931
    #   x=1.0: 71.35 - 113.8 = -42.45
    #   x=1.2: 249.2048 - 113.8*2.48832 ≈ 249.2048 - 283.17 ≈ -33.97
    #   x=2: 3783.82 - 113.8*32 = 3783.82 - 3641.6 = 142.22
    #   x=2.9: 24006.39 - 113.8*205.11 ≈ 24006.39 - 23341.5 ≈ 664.9
    #   x=3: 28401.19 - 113.8*243 = 28401.19 - 27653.4 = 747.8
    # So B(x) is negative around x=0.5-1.2, positive at x=2-3. Not a simple bump.
    #
    # Maybe the coefficient isn't exactly 113.8. Let's reconsider.
    # Actually maybe the positive side is C*x^5 + D*x^3 + E*x + bump.
    # At large x, x^5 dominates so C≈113.8. The lower terms matter at small x.
    #
    # Let's fit positive side with C=113.8 fixed and see residuals vs x^3, x, const.
    # Actually, let's just fit a polynomial in x (up to x^5) to ALL positive data
    # including E4, and see if it works. But E4 has a sharp structure near 0 that
    # a degree-5 poly won't capture well.
    #
    # Alternative: maybe the function is f(x) = x^5 * something + a Gaussian.
    # Let's look at the shape of E4 positive: starts at 15, dips to -23 at x=0.5,
    # rises to 71 at x=1. That's like a cubic-ish wiggle. 
    #
    # Let's try fitting positive small-x with a degree-4 or 5 polynomial in x
    # (including constant term) over the E4 points, and blend with power law.
    #
    # Actually, let's step back. The simplest hypothesis that fits everything:
    # f(x) = A_side * x^5 + Q_side(x) where Q is a low-degree polynomial
    # (degree <= 3) that captures the small-x behavior. Fit Q from residuals.
    #
    # For positive: residuals r = y - 113.8*x^5 at E4 points are roughly
    #   15.4, 10.4, 2.5, -6.2, -17.3, -26.5, -31.5, -37.0, -42.6, -43.2, -42.5
    # This looks like it could be a cubic: starting positive, going negative,
    # flattening around -42. Let's fit r = a + b*x + c*x^2 + d*x^3.
    # At x=0: a ≈ 21.28 (from f(0)=21.28, and 113.8*0=0). Wait f(0)=21.28,
    # so Q(0)=21.28. Good, a=21.28.
    # Then r - 21.28 at x=0.05: -5.88; x=0.1: -10.83; x=0.2: -18.74;
    # x=0.3: -27.47; x=0.4: -38.59; x=0.5: -47.79; x=0.6: -52.77;
    # x=0.7: -58.24; x=0.8: -63.90; x=0.9: -64.47; x=1.0: -63.73.
    # Hmm, roughly linear-ish then flattening. Let's fit b*x + c*x^2 + d*x^3.
    # Actually let's just do least squares in code.
    #
    # For negative: residuals r = y - (-34.5*|x|^5) = y + 34.5*|x|^5.
    # Wait, for negative x, x^5 is negative, so -34.5*|x|^5 = 34.5*x^5? No.
    # Let's define for negative side: f(x) ≈ -34.5*|x|^5 = 34.5*x^5 (since x^5<0).
    # Hmm, -34.5*|x|^5 with x<0: |x|=-x, so -34.5*(-x)^5 = -34.5*(-x^5)=34.5*x^5.
    # So f(x) ≈ 34.5*x^5 for x<0? But x^5<0 so f<0. Yes.
    # Residual r = y - 34.5*x^5 (x<0, so 34.5*x^5 <0, r = y - negative = y + |...|).
    #   x=-0.05: 22.6125 - 34.5*(-3.125e-7) ≈ 22.6125
    #   x=-0.1: 22.8483 - 34.5*(-1e-5) ≈ 22.8486
    #   x=-0.2: 24.9533 - 34.5*(-3.2e-4) ≈ 24.9643
    #   x=-0.3: 27.3822 - 34.5*(-0.00243) ≈ 27.4660
    #   x=-0.5: 25.692 - 34.5*(-0.03125) ≈ 26.7701
    #   x=-0.7: 16.8289 - 34.5*(-0.16807) ≈ 22.6273
    #   x=-0.9: -11.1291 - 34.5*(-0.59049) ≈ 9.2428
    #   x=-1.0: -34.091 - 34.5*(-1) = 0.409
    #   x=-1.2? not in E4. 
    #   x=-2: -1500.006 - 34.5*(-32) = -1500.006 + 1104 = -396.0
    #   x=-3: -10244.411 - 34.5*(-243) = -10244.411 + 8383.5 = -1860.9
    #   x=-6: -292915.946 - 34.5*(-7776) = -292915.946 + 268272 = -24644
    # Hmm, residuals grow negative at larger |x|, suggesting coefficient 34.5 is
    # slightly too small. Let's refit.
    #
    # OK, enough hand analysis. Let me just do a proper fit in code:
    # - Positive: fit y = c5*x^5 + c3*x^3 + c1*x + c0 over all positive data,
    #   but weight small-x points more? Or use a piecewise approach.
    # - Actually, let's try: fit positive with basis {1, x, x^2, x^3, x^5} over
    #   ALL positive data (E1,E2,E3,E4). If residuals are small, great.
    # - Same for negative with basis {1, x, x^2, x^3, x^5}.
    #
    # Let me just code it up and see.

    pos = [
        (0.05,15.3992),(0.1,10.4473),(0.2,2.5408),(0.3,-5.9163),(0.4,-16.1413),
        (0.5,-22.9553),(0.6,-22.6466),(0.7,-17.834),(0.8,-5.3302),(0.9,23.9947),
        (1.0,71.35),(1.2,249.2048),
        (1,70.35),(2,3783.82),(3,28401.19),(4,118360.4),(5,358940.83),
        (6,889937.3),(7,1919315.07),(8,3736882.84),(9,6727933.75),(10,11386930.38),
        (2.9,24006.3893),(21.3,498566508.849),(66.0,142487853201.7),
        (72.7,231073987061.1789),(88.2,607379528140.0764),
        (104.5,1418170236771.25),(65.5,137171213311.5103),
        (30.3,2904585078.6999),(104.9,1445522923769.7898),
        (123.6,3282957176456.9175),(79.4,359086872056.3639),(103.0,1319260760409.1902),
    ]
    neg = [
        (-0.05,22.6125),(-0.1,22.8483),(-0.2,24.9533),(-0.3,27.3822),
        (-0.5,25.692),(-0.7,16.8289),(-0.9,-11.1291),(-1.0,-34.091),
        (-1,-36.091),(-2,-1500.006),(-3,-10244.411),(-4,-40769.54),(-5,-120305.515),
        (-6,-292916.946),(-7,-623586.531),(-8,-1202334.656),(-9,-2148292.995),(-10,-3613824.11),
        (-20.3,-120955209.4828),(-61.7,-30806744759.1345),(-24.3,-295937989.9227),
        (-50.4,-11226066722.555),(-55.8,-18654932509.0998),(-63.9,-36693855455.0953),
    ]
    # f(0) = 21.28

    def fit(data, powers):
        n = len(powers)
        A = [[0.0]*n for _ in range(n)]
        b = [0.0]*n
        for x,y in data:
            phi = [x**p for p in powers]
            for i in range(n):
                b[i] += phi[i]*y
                for j in range(n):
                    A[i][j] += phi[i]*phi[j]
        for i in range(n):
            p = max(range(i,n), key=lambda r: abs(A[r][i]))
            A[i],A[p]=A[p],A[i]
            b[i],b[p]=b[p],b[i]
            if abs(A[i][i])<1e-12: continue
            for r in range(i+1,n):
                f=A[r][i]/A[i][i]
                for c in range(i,n): A[r][c]-=f*A[i][c]
                b[r]-=f*b[i]
        coef=[0.0]*n
        for i in range(n-1,-1,-1):
            if abs(A[i][i])<1e-12: continue
            s=b[i]-sum(A[i][j]*coef[j] for j in range(i+1,n))
            coef[i]=s/A[i][i]
        return coef

    # Try basis {1, x, x^2, x^3, x^5} for both sides
    powers = [0,1,2,3,5]
    cp = fit(pos, powers)
    cn = fit(neg, powers)

    def predict_one(x):
        if x == 0:
            return 21.28
        c = cp if x > 0 else cn
        return sum(c[i]*(x**powers[i]) for i in range(len(powers)))

    return {"y": [predict_one(x) for x in probe["x"]]}
