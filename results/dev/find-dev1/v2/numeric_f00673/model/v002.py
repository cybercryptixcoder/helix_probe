import math

def predict(probe):
    # f(x) = 16.8*|x| + noise for |x| >= ~0.6 [E1, E2]
    # Near zero (|x| < ~0.6) the |x| term is absent: f is small and noisy,
    #   roughly flat around 0 with no kink [E3, E4]
    # E3: |x|<=0.1 gives values ~ -1.3..1.6 (noise around 0), not 16.8|x|
    # E4: |x|<=0.6 gives values ~0..9 with no clean |x| trend; at 0.6 ~9
    # So there's a transition: below ~0.6 output is near 0 (noisy), above it
    #   follows 16.8*|x|. The |x| regime seems to kick in around 0.6-1.0.
    # E3 at 0.6: 9.99, 16.8*0.6=10.08 -> matches |x| regime at 0.6
    # E4 at 0.6: 9.17, 8.95 -> also ~|x| regime (10.08)
    # E3 at 0.4: 5.53, 16.8*0.4=6.72; at 0.3: 5.35 vs 5.04; at 0.2: 2.57 vs 3.36
    # E4 at 0.5: 7.92,7.21 vs 8.4; at 0.4: 6.60,5.05 vs 6.72; at 0.3: 5.33,5.80 vs 5.04
    # So around 0.3-0.6 it's roughly |x|-like but noisy/rounded.
    # Below ~0.2 it collapses toward 0 (E3: 0.1->0.57, 0.05->1.6, 0.02->-0.28..1.2)
    # Best model: f(x) = 16.8*|x| for |x| >= 0.6; for |x| < 0.6 use a
    #   rounded/attenuated version. Try f = 16.8*|x| * smoothstep, or just
    #   f = 16.8*|x|^2/0.6 for |x|<0.6 (quadratic bottom) [E4 hypothesis].
    # E4 check quadratic: at 0.5: 16.8*0.25/0.6=7.0 (obs 7.9,7.2) ok
    #   at 0.3: 16.8*0.09/0.6=2.52 (obs 5.3,5.8) too low
    # Hmm. Actually E4 values at 0.3 are ~5.5, close to 16.8*0.3=5.04.
    # So maybe |x| regime holds down to ~0.2, and only below 0.2 it rounds off.
    # E3: 0.2->2.57 (16.8*0.2=3.36), 0.1->0.57 (1.68), 0.05->1.6, 0.02->-0.28
    # So below ~0.2 output shrinks toward 0. Use quadratic below 0.2:
    #   f = 16.8*x^2/0.2 = 84*x^2 for |x|<0.2; f=16.8*|x| above.
    # Check 0.1: 84*0.01=0.84 (obs 0.57) ok; 0.05: 0.21 (obs 1.6) noisy;
    #   0.02: 0.034 (obs -0.28..1.2) noisy ok.
    # Check 0.2: 84*0.04=3.36 matches |x| at boundary.
    # This is a guess; noise is large near 0.
    out = []
    for x in probe["x"]:
        try:
            ax = abs(x)
            if ax >= 0.2:
                out.append(16.8 * ax)
            else:
                out.append(84.0 * x * x)
        except Exception:
            out.append(None)
    return {"y": out}
