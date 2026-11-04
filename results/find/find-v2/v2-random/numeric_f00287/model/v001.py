import math

def predict(probe):
    # Observations from E1:
    # x=88.2 -> -1478.4 ; x=66.0 -> -1108.8 ; x=72.7 -> -1209.6
    #   These look like -x^2 * something? 88.2^2=7779.24, ratio -0.19; 66^2=4356, ratio -0.2546; 72.7^2=5285.29, ratio -0.2289
    #   Try -x^2/4? 88.2^2/4=1944.8 no. Try -x*|x|/... hmm
    #   Actually -1478.4/88.2 = -16.76; -1108.8/66 = -16.8; -1209.6/72.7 = -16.64. So y ≈ -16.8*x for large positive x.
    #   Check: 88.2*-16.8=-1481.76 (obs -1478.4); 66*-16.8=-1108.8 exact; 72.7*-16.8=-1221.36 (obs -1209.6). Close-ish.
    # x=-20.3 -> 14.7 ; x=-24.3 -> 17.5 ; x=-61.7 -> 43.4 ; x=-50.4 -> 35.7 ; x=-6.0 -> 4.2
    #   These look like -0.7*x? -20.3*-0.7=14.21 (obs 14.7); -24.3*-0.7=17.01 (obs 17.5); -61.7*-0.7=43.19 (obs 43.4); -50.4*-0.7=35.28 (obs 35.7); -6*-0.7=4.2 exact.
    #   So for negative x, y ≈ -0.7*x = 0.7*|x|. Ratio: 14.7/-20.3=-0.724; 17.5/-24.3=-0.720; 43.4/-61.7=-0.703; 35.7/-50.4=-0.708; 4.2/-6=-0.7
    #   Hmm ~ -0.71*x. Could be -x/sqrt(2)? 1/sqrt2=0.7071. -20.3*-0.7071=14.35 (obs 14.7). Close.
    # x=2.9 -> -402.4726 ; x=21.3 -> -352.8
    #   2.9: -402.4726. 2.9^2=8.41. -402.47/8.41=-47.86. Hmm. 2.9^3=24.389, -402.47/24.389=-16.5.
    #   21.3: -352.8. 21.3^2=453.69, ratio -0.7776. 21.3^3=9663.6, ratio -0.0365.
    #   Try -x^2 * something? 2.9: -8.41*k=-402.47 -> k=47.86. 21.3: -453.69*k=-352.8 -> k=0.7776. Not constant.
    #   Try -x^3/... 2.9^3=24.389, -402.47/24.389=-16.5. 21.3^3=9663.6, -352.8/9663.6=-0.0365. No.
    #   Hmm 2.9 gives huge negative. Maybe there's a special region near 0? Or a term like -c/x?
    #   -402.4726... note 402.4726. 2.9^2=8.41. 402.4726/8.41=47.857. Hmm 47.857... 
    #   Actually 2.9^4 = 70.7281. 402.4726/70.7281=5.69. 
    #   Let's try: maybe f(x) = -x^2 * something + ... Let me reconsider.
    #   -402.4726 = ? 2.9^2 * 47.857. 47.857 ≈ ? Hmm.
    #   Try -x^3 * 16.5? 2.9^3*16.5=402.4! Yes! 24.389*16.5=402.42. So -x^3*16.5 ≈ -402.47. Close.
    #   Check 21.3: 21.3^3*16.5=9663.6*16.5=159449. No, obs -352.8. Not matching.
    #   So different behavior for 2.9 vs 21.3. Maybe there's a region.
    #   Hmm, 2.9 is small. Maybe near 0 there's a different term.
    #   Let me reconsider: maybe f(x) = -x^2 * 16.5 for small? 2.9^2*16.5=8.41*16.5=138.8. No.
    #   -x^3*16.5 for 2.9 = -402.4. matches! For 21.3: -9663.6*16.5 huge. No.
    #   So maybe for small |x| it's -16.5 x^3? But 21.3 not small.
    #   What about 21.3 -> -352.8. 21.3^2=453.69. -352.8/453.69=-0.7776. Hmm -0.7776 ≈ -0.78.
    #   Let me look at positive large: 88.2->-1478.4, 66->-1108.8, 72.7->-1209.6. These are ~ -16.8x.
    #   But 21.3 -> -352.8, which is -16.56x. Oh! -352.8/21.3 = -16.56. Close to -16.8!
    #   So 21.3 also fits -16.8x roughly (-357.8 vs -352.8). OK so positive x: y ≈ -16.8x? But then 2.9 should be -48.7, not -402.
    #   So 2.9 is the outlier. Maybe near 0 there's a different regime.
    #   Let me reconsider 2.9: -402.4726. Hmm what if it's -x^3 * 16.5? = -402.4. 
    #   Or maybe there's a term -c/x^2 or something. 2.9: 1/2.9^2=0.1189. -402.47/0.1189=-3385. no.
    #   Maybe -16.8x plus a spike near 0? Like -16.8*2.9=-48.7, plus -353.8 extra. Hmm.
    #   Let me reconsider negative x: y ≈ -0.71x (i.e., positive). And positive x: y ≈ -16.8x (negative).
    #   So maybe f(x) = -16.8x for x>0, and -0.71x for x<0? That's a piecewise linear with a kink at 0.
    #   But 2.9 gives -402, not -48.7. So there's a special region near 0.
    #   -402.4726... let me see: 2.9^2 = 8.41. 402.4726/8.41 = 47.857. 47.857... hmm 47.857 = ?
    #   Actually maybe f(x) = -16.8x - something/x? At 2.9: -48.72 - 353.75. 353.75*2.9=1025.9. Hmm.
    #   Or maybe -16.8x - c/x^2: c/8.41=353.75 -> c=2975. At 21.3: 2975/453.69=6.56, so -357.8-6.56=-364. obs -352.8. Not great.
    #   Let me try: maybe f(x) = -16.8x for x>0 except near 0 where it's steeper.
    #   Actually 2.9^3*16.5 = 402.42, very close to 402.4726. Let me check more precisely: 2.9^3=24.389, *16.5=402.4185. obs 402.4726. diff 0.054. Hmm.
    #   2.9^3 * 16.502 = 402.467. Close. So maybe -16.5 x^3 near 0? But that's weird.
    #   Alternatively maybe there's a term like -x^2 * 47.86 near 0.
    #   Honestly with one experiment I'm guessing. Let me pick a reasonable piecewise model.
    #   Given uncertainty, I'll model: for x>0, y=-16.8x; for x<0, y=-0.71x; and near 0 (|x|<some) something steeper.
    #   But 2.9 is the only small positive. I don't know the boundary.
    #   Let me just fit: maybe f(x) = -16.8x for x>=threshold, and -16.5x^3 for 0<x<threshold? At 2.9: -402.4. At threshold where they meet: -16.8t = -16.5t^3 -> t^2=16.8/16.5=1.018 -> t=1.009. So threshold ~1. Then for x>1, -16.8x. Check 21.3: -357.8 vs obs -352.8. ok-ish.
    #   For x<0: -0.71x. At x=-6: 4.26 vs 4.2. good.
    #   Hmm but is there a cubic region for negative too? -6 gives 4.2 which is linear. So negative is linear.
    #   Actually maybe the whole thing: f(x) = -16.8x for x>1, -16.5x^3 for 0<x<1, -0.71x for x<0. That's a guess.
    #   Wait, but -16.8x for x>1 and -16.5x^3 for 0<x<1: at x=1 both give -16.8 and -16.5, close.
    #   But actually maybe simpler: the cubic region is |x|<1 and it's -16.5x^3? For negative small x that'd be positive small. But -6 is linear. So maybe cubic only for 0<x<1.
    #   This is too speculative. Let me just do piecewise linear with a special near-zero positive region.
    #   Actually, let me reconsider: maybe f(x) = -16.8x for all x>0, but there's an added term that's large near 0. Like -c/x? At 2.9: -48.7 - c/2.9 = -402.47 -> c/2.9=353.77 -> c=1025.9. At 21.3: -357.8 - 1025.9/21.3 = -357.8-48.2=-406. obs -352.8. Not matching.
    #   I'll go with piecewise: x>0: -16.8x (but 2.9 exception suggests near-zero different). 
    #   Given only one data point near zero, I'll model x>0 as -16.8x for x>=3, and for 0<x<3 use -16.5x^3. At x=3: -16.5*27=-445.5 vs -16.8*3=-50.4. Discontinuous. Bad.
    #   Hmm. Let me just try: maybe f(x) = -16.8x + g(x) where g is a spike near 0. 
    #   Actually you know what, let me reconsider the whole thing. Maybe it's -x * (16.8 + something*exp(-x^2))? 
    #   At 2.9: -2.9*(16.8 + A*exp(-8.41)) = -402.47 -> 16.8+A*0.000222=138.78 -> A*0.000222=121.98 -> A=549,000. At 21.3: exp(-453)~0, so -16.8*21.3=-357.8 vs -352.8. ok.
    #   That's a huge spike. Unlikely.
    #   I'll just go with a simple piecewise and note uncertainty. Given exam scoring, best guess:
    #   x>0: -16.8x ; x<0: -0.71x ; but 2.9 needs special. 
    #   Let me just include: if 0<x<3: -16.5*x**3 else if x>0: -16.8x else -0.71x.
    #   At x=3: -16.5*27=-445.5, at x=3+ -50.4. Discontinuous but I have no data between 2.9 and 21.3.
    #   Actually maybe the boundary is where -16.5x^3 = -16.8x -> x^2=1.018, x=1.009. So for x>1.009 linear, for 0<x<1.009 cubic. At 2.9 that's linear -> -48.7, not -402. Contradiction.
    #   So 2.9 must be in cubic region, meaning boundary >2.9. Then at boundary cubic meets linear: x^2=16.8/16.5 -> x=1.009. Contradiction.
    #   So it's not a clean cubic-to-linear. 
    #   Maybe it's -16.5x^3 for 0<x<3 and -16.8x for x>3, discontinuous. I'll go with that as best guess.
    #   Actually, let me reconsider: maybe the function is -16.8x for x>0 but with a different formula entirely near 0. 
    #   I'll just commit to: x>0: -16.8x, except 0<x<3: -16.5x^3. x<0: -0.71x.
    out = []
    for x in probe.get("x", []):
        try:
            if x > 0:
                if x < 3:
                    y = -16.5 * x**3
                else:
                    y = -16.8 * x
            else:
                y = -0.71 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
