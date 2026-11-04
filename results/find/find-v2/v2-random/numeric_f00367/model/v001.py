def predict(probe):
    # f(x) = 2.42 * x for all tested x [E1]
    # Check: 88.2*2.42=213.444≈213.48; 66*2.42=159.72≈160.2; -20.3*2.42=-49.126? no...
    # Recompute ratios from E1:
    # 213.48/88.2 = 2.4204
    # 160.2/66.0  = 2.4273
    # -37.02/-20.3 = 1.8236  <- not constant!
    # -136.38/-61.7 = 2.2104
    # 8.76/2.9 = 3.0207
    # -46.62/-24.3 = 1.9185
    # 176.28/72.7 = 2.4248
    # -109.26/-50.4 = 2.1679
    # -2.7/-6.0 = 0.45
    # 52.92/21.3 = 2.4845
    # Ratios are not constant, so not pure linear. Try y = a*x + b?
    # Differences suggest something else. Let's look for a pattern.
    # Try y = x * something(x). Or maybe y = 2.42*x rounded? 
    # 88.2*2.42=213.444 vs 213.48 (diff .036)
    # 66*2.42=159.72 vs 160.2 (diff .48)
    # Hmm. Try y = 2.4*x + small? 
    # Actually check: maybe y = x + something. 
    # 88.2 -> 213.48, diff 125.28
    # 66 -> 160.2, diff 94.2
    # -20.3 -> -37.02, diff -16.72
    # -61.7 -> -136.38, diff -74.68
    # 2.9 -> 8.76, diff 5.86
    # -24.3 -> -46.62, diff -22.32
    # 72.7 -> 176.28, diff 103.58
    # -50.4 -> -109.26, diff -58.86
    # -6.0 -> -2.7, diff 3.3
    # 21.3 -> 52.92, diff 31.62
    # Try y = 2.42*x? residuals: 
    # 213.48-213.444=0.036
    # 160.2-159.72=0.48
    # -37.02-(-49.126)=12.106  <- big
    # Hmm -20.3 is special?
    # Let's try y = 2.4*x + 0.02*x^2? no.
    # Try y = x*2.4 + 0.02*x? = 2.42x same.
    # Look at -6.0 -> -2.7. 2.42*-6=-14.52, not -2.7. Very different.
    # 2.9 -> 8.76. 2.42*2.9=7.018, not 8.76.
    # Maybe piecewise: for |x| small, different?
    # |x|<10: 2.9->8.76 (ratio 3.02), -6->-2.7 (ratio 0.45). Not consistent.
    # Hmm -6 gives -2.7 = 0.45*-6. 2.9 gives 8.76 = 3.02*2.9.
    # Try y = x + x*|x|/something? 
    # 2.9: 2.9+2.9*2.9/k = 8.76 => 8.41/k=5.86 => k=1.435
    # -6: -6+36/k=-2.7 => 36/k=3.3 => k=10.9. no.
    # Try y = 2.42*x for large |x|, something else for small.
    # Actually maybe y = round to 2 decimals of some function.
    # Let's try y = 2.42*x exactly and see which match:
    # 88.2*2.42=213.444 -> 213.48? off by .036
    # Hmm maybe coefficient is 2.4204? 88.2*2.4204=213.479. 66*2.4204=159.746 vs 160.2 no.
    # Try y = 2.4*x + 0.02*x^2? 88.2: 211.68+155.6=367 no.
    # Try y = x*sign(x)*... 
    # Let me try y = 2.42*x but with x rounded? 
    # Actually maybe y = 2.42*x - something*sin? 
    # Let's try y = a*x + b*sin(x)? Too many unknowns.
    # Try y = 2.42*x + c*sin(x):
    # 88.2: 213.444 + c*sin(88.2). sin(88.2 rad)=? 88.2 mod 2pi: 88.2-14*6.283=88.2-87.96=0.238, sin=0.236. 213.48-213.444=0.036 => c=0.153
    # 66: 159.72 + c*sin(66). 66-10*6.283=66-62.83=3.17, sin=-0.028. 160.2-159.72=0.48 => c=-17. no.
    # Try y = 2.42*x + c*cos(x)? 
    # Hmm. Let's try y = x*2.4 + 0.02*x^2*sign? no.
    # Look at -6->-2.7 and 2.9->8.76. Maybe y = x^2/... no sign.
    # -6 -> -2.7: ratio 0.45. 2.9->8.76: ratio 3.02. 
    # Maybe y = x + x^2/10? -6: -6+3.6=-2.4 close to -2.7. 2.9: 2.9+0.841=3.74 no.
    # Try y = x + x^2/8? -6: -6+4.5=-1.5 no.
    # Try y = x*|x|/something + ... 
    # Let's try y = 2.42*x + k*x^2? 
    # -6: -14.52+36k=-2.7 => 36k=11.82 => k=0.328
    # 2.9: 7.018+8.41k=8.76 => 8.41k=1.742 => k=0.207. no.
    # Try y = 2.42*x + k*x^3?
    # -6: -14.52-216k=-2.7 => -216k=11.82 => k=-0.0547
    # 2.9: 7.018+24.389k=8.76 => 24.389k=1.742 => k=0.0714. no.
    # Hmm. Maybe the function is 2.42*x but with rounding to nearest 0.06? 
    # 213.48/0.06=3558, 160.2/0.06=2670, -37.02/0.06=-617, -136.38/0.06=-2273, 8.76/0.06=146, -46.62/0.06=-777, 176.28/0.06=2938, -109.26/0.06=-1821, -2.7/0.06=-45, 52.92/0.06=882. All integers! So y is multiple of 0.06.
    # 213.48 = 3558*0.06. 88.2/0.06=1470. 3558/1470=2.4204...
    # 160.2=2670*0.06, 66/0.06=1100, 2670/1100=2.4273
    # -37.02=-617*0.06, -20.3/0.06=-338.33 not integer. Hmm.
    # Maybe y = round(2.42*x, 2)? 2.42*88.2=213.444 -> 213.44 not 213.48.
    # Maybe y = round(2.42*x*... 
    # Let's just try y = 2.42*x and check all:
    # 88.2: 213.444 (obs 213.48, diff .036)
    # 66: 159.72 (obs 160.2, diff .48)
    # -20.3: -49.126 (obs -37.02, diff 12.1) BIG
    # -61.7: -149.314 (obs -136.38, diff 12.9) BIG
    # 2.9: 7.018 (obs 8.76, diff 1.74)
    # -24.3: -58.806 (obs -46.62, diff 12.2) BIG
    # 72.7: 175.934 (obs 176.28, diff .35)
    # -50.4: -121.968 (obs -109.26, diff 12.7) BIG
    # -6.0: -14.52 (obs -2.7, diff 11.8) BIG
    # 21.3: 51.546 (obs 52.92, diff 1.37)
    # Pattern: negative x with |x|>~5 have diff ~+12. Positive x have small diff.
    # Wait -6 diff 11.8, -20.3 diff 12.1, -24.3 diff 12.2, -50.4 diff 12.7, -61.7 diff 12.9.
    # Diff increases with |x|. Maybe y = 2.42*x + 12.5 for x<0? But -6 diff 11.8.
    # Actually diff = obs - 2.42*x. For negatives: 11.8,12.1,12.2,12.7,12.9.
    # Hmm maybe y = 2.42*x + 12.5*something.
    # Or maybe y = 2.42*x for x>=0, and y = 2.42*x + 12.5 for x<0? But -6 gives -14.52+12.5=-2.02 vs -2.7. Close-ish.
    # Try y = 2.42*x + 12.5 for x<0: -20.3 -> -49.126+12.5=-36.626 vs -37.02. close.
    # -61.7 -> -149.314+12.5=-136.814 vs -136.38. close.
    # -24.3 -> -58.806+12.5=-46.306 vs -46.62. close.
    # -50.4 -> -121.968+12.5=-109.468 vs -109.26. close.
    # -6 -> -14.52+12.5=-2.02 vs -2.7. off by .68.
    # Hmm. Maybe y = 2.42*x + 12.5 for x<0 but -6 is off. Or maybe offset is 12.5+something.
    # Actually maybe y = 2.42*x + 12.5 for x < -5? and different for -5<x<0?
    # We only have -6 as the small negative. -6: obs -2.7. 2.42*-6=-14.52. diff 11.82.
    # Try y = 2.42*x + 12.5 for x<0. -6 -> -2.02 vs -2.7. 
    # Maybe coefficient slightly different. Let's fit negatives: y = a*x + b.
    # Points: (-20.3,-37.02),(-61.7,-136.38),(-24.3,-46.62),(-50.4,-109.26),(-6,-2.7)
    # Slope between -20.3 and -61.7: (-136.38+37.02)/(-61.7+20.3)=(-99.36)/(-41.4)=2.4
    # Between -24.3 and -50.4: (-109.26+46.62)/(-50.4+24.3)=(-62.64)/(-26.1)=2.4
    # Between -6 and -20.3: (-37.02+2.7)/(-20.3+6)=(-34.32)/(-14.3)=2.4
    # Slope 2.4! Intercept: -2.7-2.4*(-6)=-2.7+14.4=11.7. Check -20.3: 2.4*-20.3+11.7=-48.72+11.7=-37.02 ✓
    # -61.7: 2.4*-61.7+11.7=-148.08+11.7=-136.38 ✓
    # So for x<0: y = 2.4*x + 11.7
    # Now positives: (88.2,213.48),(66,160.2),(2.9,8.76),(72.7,176.28),(21.3,52.92)
    # Slope 88.2,66: (213.48-160.2)/(88.2-66)=53.28/22.2=2.4
    # 66,21.3: (160.2-52.92)/(66-21.3)=107.28/44.7=2.4
    # 21.3,2.9: (52.92-8.76)/(21.3-2.9)=44.16/18.4=2.4
    # Slope 2.4! Intercept: 8.76-2.4*2.9=8.76-6.96=1.8. Check 88.2: 2.4*88.2+1.8=211.68+1.8=213.48 ✓
    # 66: 158.4+1.8=160.2 ✓
    # So for x>=0: y = 2.4*x + 1.8
    # For x<0: y = 2.4*x + 11.7
    # Check x=0? Unknown. Boundary at 0.
    # So f(x) = 2.4*x + 1.8 if x>=0 else 2.4*x + 11.7
    def predict(probe):
        out = []
        for x in probe["x"]:
            if x >= 0:
                out.append(2.4*x + 1.8)
            else:
                out.append(2.4*x + 11.7)
        return {"y": out}
    return predict(probe)
