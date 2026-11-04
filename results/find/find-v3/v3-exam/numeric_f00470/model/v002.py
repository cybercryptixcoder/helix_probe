import math

def predict(probe):
    # Model: f(x) = sign(x) * (|x|^p) * (a + b*|x| + c*|x|^2 ...) — but let's test structure.
    #
    # Evidence:
    # E2: x=1 -> 70.35, x=10 -> 11386930.38. Ratio 161860 over 10x.
    #     log10(161860) = 5.209, so effective exponent ~5.2 at large x.
    #     But x=1->70.35, x=2->3783.82: ratio 53.78 over 2x -> exp 5.75.
    #     x=2->3: 28401/3783=7.5 over 1.5x -> exp 4.97
    #     x=9->10: 11386930/6727933=1.692 over 1.111x -> exp 5.09
    #     So exponent ~5 at large, higher at small. Not pure power.
    #
    # Negative: x=-1 -> -36.091, x=-10 -> -3613824.11. Ratio 100140 over 10x -> exp 5.0006.
    #     x=-1->-2: 1500/36.09=41.56 over 2x -> exp 5.377
    #     x=-9->-10: 3613824/2148293=1.682 over 1.111x -> exp 5.05
    #     So negative is cleaner ~ x^5 at large, with extra at small.
    #
    # E3 check: x=104.5 -> 1.418e12. 104.5^5 = 1.246e10. ratio = 113.8.
    #     x=123.6 -> 3.283e12. 123.6^5 = 2.885e10. ratio = 113.8.
    #     x=79.4 -> 3.591e11. 79.4^5 = 3.157e9. ratio = 113.7.
    #     Consistent! So for large positive x, y ≈ 113.8 * x^5.
    #     Check x=10: 113.8*1e5 = 1.138e7. Observed 1.1386930e7. YES!
    #     Check x=1: 113.8. Observed 70.35. NO — small x differs.
    #
    # So positive: y = 113.8 * x^5 for large x, but small x has less.
    #     x=1: 70.35 vs 113.8 -> deficit 43.45
    #     x=2: 3783.82 vs 113.8*32=3641.6 -> excess 142.2
    #     x=3: 28401 vs 113.8*243=27653 -> excess 748
    #     Hmm so it's not just 113.8*x^5. Let's fit y = a*x^5 + b*x^3 + c*x.
    #
    # Negative large: x=-10 -> -3613824. 10^5=1e5, ratio 36.14.
    #     x=-104.5? not in E3. x=-55.8 -> -1.865e10. 55.8^5=5.404e8. ratio=34.5.
    #     x=-63.9 -> -3.669e10. 63.9^5=1.065e9. ratio=34.45.
    #     x=-20.3 (E1) -> -1.2096e8. 20.3^5=3.446e6. ratio=35.1.
    #     x=-24.3 (E1) -> -2.959e8. 24.3^5=8.47e6. ratio=34.9.
    #     x=-50.4 (E1) -> -1.1226e10. 50.4^5=3.256e8. ratio=34.5.
    #     x=-61.7 (E1) -> -3.0807e10. 61.7^5=8.94e8. ratio=34.5.
    #     So negative large: y ≈ -34.5 * |x|^5.
    #     Check x=-10: 34.5*1e5=3.45e6 vs 3.614e6. ratio 36.14 — slightly higher.
    #     x=-1: 34.5 vs 36.09. Close-ish but small x differs.
    #
    # So both sides ~ coefficient * x^5 at large, but positive coeff ~113.8, negative ~34.5.
    # Ratio 113.8/34.5 = 3.30. Hmm.
    #
    # Let's fit positive: y = a*x^5 + b*x^3 + c*x using E2 data.
    # Actually let's just do least squares in code.
    #
    # Also E1: x=2.9 -> 24006.3893. 2.9^5=205.1. 113.8*205.1=23340. Close but not exact.
    #     x=21.3 -> 4.9857e8. 21.3^5=4.383e6. 113.8*4.383e6=4.988e8. YES matches!
    #     x=66.0 -> 1.4249e11. 66^5=1.252e9. 113.8*1.252e9=1.4248e11. YES!
    #     x=72.7 -> 2.3107e11. 72.7^5=2.031e9. 113.8*2.031e9=2.311e11. YES!
    #     x=88.2 -> 6.0738e11. 88.2^5=5.337e9. 113.8*5.337e9=6.073e11. YES!
    # So positive large is exactly 113.8*x^5. Small x deviates.
    #
    # x=2.9: 113.8*205.1=23340 vs 24006. excess 666.
    # x=1.2 (E3) -> 249.2048. 113.8*1.2^5=113.8*2.488=283.1. deficit 34.
    # x=1 -> 70.35 vs 113.8. deficit 43.45.
    # x=2 -> 3783.82 vs 3641.6. excess 142.2.
    # Hmm, so it's not a simple polynomial in x^5. Let's fit a*x^5+b*x^3+c*x+d*x^2... 
    # Actually let's just fit polynomial in x with odd powers up to 5, plus maybe even.
    #
    # Let me reconsider: maybe f(x) = x^5 * (something) + lower terms.
    # Let's just do a proper fit in code with basis x, x^2, x^3, x^4, x^5.
    #
    # For negative: check E1 x=-6.0 -> -292915.946. 6^5=7776. 34.5*7776=268272. 
    #     Hmm observed 292916. ratio 37.67. Higher.
    #     x=-20.3: 34.5*3.446e6=1.189e8 vs 1.2096e8. ratio 35.1.
    #     So negative also has lower-order corrections.
    #
    # Let me just fit both sides with polynomial basis {x, x^3, x^5} and see residuals.
    # Actually the E3 match was 0.60 with v1's fit. Let's improve.

    # Fit positive: y = a*x^5 + b*x^3 + c*x (odd only, since f(0) likely 0)
    # Use E2 positive + E1 positive + E3 positive points.
    pos = [(1,70.35),(2,3783.82),(3,28401.19),(4,118360.4),(5,358940.83),
           (6,889937.3),(7,1919315.07),(8,3736882.84),(9,6727933.75),(10,11386930.38),
           (2.9,24006.3893),(21.3,498566508.849),(66.0,142487853201.7),
           (72.7,231073987061.1789),(88.2,607379528140.0764),
           (1.2,249.2048),(104.5,1418170236771.25),(65.5,137171213311.5103),
           (30.3,2904585078.6999),(104.9,1445522923769.7898),
           (123.6,3282957176456.9175),(79.4,359086872056.3639),(103.0,1319260760409.1902)]
    neg = [(-1,-36.091),(-2,-1500.006),(-3,-10244.411),(-4,-40769.54),(-5,-120305.515),
           (-6,-292916.946),(-7,-623586.531),(-8,-1202334.656),(-9,-2148292.995),(-10,-3613824.11),
           (-20.3,-120955209.4828),(-61.7,-30806744759.1345),(-24.3,-295937989.9227),
           (-50.4,-11226066722.555),(-6.0,-292915.946),
           (-55.8,-18654932509.0998),(-63.9,-36693855455.0953)]

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

    # Try basis x, x^3, x^5 for both sides
    cp = fit(pos, [1,3,5])
    cn = fit(neg, [1,3,5])

    def predict_one(x):
        c = cp if x >= 0 else cn
        return c[0]*x + c[1]*x**3 + c[2]*x**5

    return {"y": [predict_one(x) for x in probe["x"]]}
