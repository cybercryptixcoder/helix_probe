def predict(probe):
    # f(x) appears to be a polynomial-like function with very large magnitude outputs.
    # E1 data: try to fit a polynomial. Let's examine ratios.
    # x=88.2 -> 6.07e11; x=66 -> 1.42e11; x=72.7 -> 2.31e11
    # x=-61.7 -> -3.08e10; x=-50.4 -> -1.12e10; x=-24.3 -> -2.96e8
    # x=21.3 -> 4.99e8; x=2.9 -> 24006; x=-6 -> -292916; x=-20.3 -> -1.21e8
    # Looks like odd-ish power. Try x^5: 88.2^5 ~ 5.3e9, too small. x^6: 88.2^6 ~ 4.7e11 close!
    # 66^6 = 8.3e10, observed 1.42e11 ratio ~1.7
    # Try x^6 * something. 88.2^6=4.7e11 vs 6.07e11 -> 1.29
    # 66^6=8.27e10 vs 1.42e11 -> 1.72
    # Hmm not constant. Try x^7: 88.2^7=4.1e13 too big.
    # Maybe combination. Let's check sign: negative x gives negative y for large |x|, positive for positive x -> odd function dominant.
    # x=88.2 -> 6.07e11; x=72.7 -> 2.31e11; ratio (88.2/72.7)^n = 2.63 -> n = ln2.63/ln1.213 = 0.967/0.193=5.0
    # So ~x^5? 88.2^5 = 5.33e9, observed 6.07e11 -> factor 114
    # 72.7^5=2.03e9, observed 2.31e11 -> factor 114. Consistent!
    # 66^5=1.25e9, observed 1.42e11 -> factor 114. 
    # -61.7^5 = -8.94e8, observed -3.08e10 -> factor 34.5. Not consistent.
    # Hmm. -50.4^5=-3.25e8, obs -1.12e10 -> 34.5. Consistent for negatives!
    # -24.3^5=-8.47e6, obs -2.96e8 -> 34.9. Consistent.
    # -20.3^5=-3.45e6, obs -1.21e8 -> 35.0. Consistent.
    # -6^5=-7776, obs -292916 -> 37.7. Close-ish.
    # 2.9^5=205, obs 24006 -> 117. Hmm.
    # 21.3^5=4.38e6, obs 4.99e8 -> 114. 
    # So positive x: factor ~114, negative x: factor ~35. But 2.9 gives 117.
    # Wait maybe it's x^5 * 114 for x>0 and x^5*35 for x<0? But 2.9 -> 205*114=23370 vs 24006 close.
    # -6 -> -7776*35=-272160 vs -292916. ratio 37.7. Hmm.
    # Maybe there's an added term. Let's try y = a*x^5 + b*x^3 + c*x.
    # Actually let's reconsider: maybe it's x^5 * 114 for x>=0 and x^5*35 for x<0? Check -6: -7776*35=-272160, obs -292916, diff -20756.
    # Maybe piecewise: for x<0, y = 35*x^5 - something? 
    # Let's try y = 114*x^5 for x>=0. Check 2.9: 114*205=23370 vs 24006. diff 636.
    # 21.3: 114*4.38e6=4.99e8. matches!
    # 66: 114*1.25e9=1.425e11 matches!
    # 72.7: 114*2.03e9=2.31e11 matches!
    # 88.2: 114*5.33e9=6.08e11 matches!
    # So for x>=0: y = 114*x^5 (approx). 2.9 slight off maybe rounding.
    # For x<0: 35*x^5? -61.7: 35*-8.94e8=-3.13e10 vs -3.08e10. close.
    # -50.4: 35*-3.25e8=-1.14e10 vs -1.12e10 close.
    # -24.3: 35*-8.47e6=-2.96e8 matches!
    # -20.3: 35*-3.45e6=-1.21e8 matches!
    # -6: 35*-7776=-272160 vs -292916. off by 7%.
    # Hmm -6 is close to zero, maybe there's a lower-order term.
    # Let's fit: for x<0, y = 35*x^5 + c*x? -6: -272160 + c*(-6) = -292916 -> -6c=-20756 -> c=3459.
    # Check -20.3: 35*-3.45e6 + 3459*-20.3 = -1.207e8 - 70218 = -1.208e8 vs -1.21e8. ok.
    # Check -24.3: 35*-8.47e6 + 3459*-24.3 = -2.965e8 - 84053 = -2.966e8 vs -2.959e8. close.
    # Check -50.4: 35*-3.25e8 + 3459*-50.4 = -1.138e10 - 174334 = -1.138e10 vs -1.1226e10. off.
    # Hmm. Maybe c*x^3? -6: 35*-7776 + c*-216 = -292916 -> -216c = -20756 -> c=96.
    # -20.3: 35*-3.45e6 + 96*-8365 = -1.207e8 - 803040 = -1.215e8 vs -1.21e8. ok.
    # -24.3: 35*-8.47e6 + 96*-14349 = -2.965e8 - 1.38e6 = -2.979e8 vs -2.959e8. off.
    # Hmm.
    # Let's just try y = 114*x^5 for x>=0, y=35*x^5 for x<0 as first approximation.
    # Actually maybe it's simpler: y = 114*x^5 when x>=0, and for x<0 something else.
    # Let's check if 35 = 114 * something. 35/114 = 0.307.
    # Maybe the function is x^5 * (114 if x>=0 else 35)? That's odd.
    # Or maybe y = 114*x^5 for x>=0 and y = 114*x^5 * 0.307 for x<0? Same thing.
    # Let me reconsider. Maybe it's not x^5. Let me check x^5 vs x^6 more carefully.
    # Actually could be x^5 * 114 for x>=0. For x<0, maybe y = -114*|x|^5 * something.
    # Let's just go with piecewise power law.
    # Actually, let me reconsider: maybe it's a*x^5 + b*x for all x, with different behavior.
    # For x>=0: 114*x^5. For x<0: 35*x^5 + 3459*x? Let's check -6: 35*-7776+3459*-6=-272160-20754=-292914 vs -292916. 
    # Check -20.3: 35*-3.45e6 + 3459*-20.3 = -120750000 - 70218 = -120820218 vs -120955210. off by 0.1%.
    # Check -24.3: 35*-8.47e6 + 3459*-24.3 = -296450000 - 84054 = -296534054 vs -295937989. off 0.2%.
    # Check -50.4: 35*-3.25e8 + 3459*-50.4 = -1.1375e10 - 174334 = -1.1375e10 vs -1.1226e10. off 1.3%.
    # Check -61.7: 35*-8.94e8 + 3459*-61.7 = -3.129e10 - 213420 = -3.129e10 vs -3.0807e10. off 1.6%.
    # Hmm not great at large |x|.
    # Maybe for x<0 it's 35*x^5 + c*x^3? -6: 35*-7776 + c*-216 = -292916 -> c=96.3
    # -20.3: 35*-3.45e6 + 96.3*-8365 = -1.2075e8 - 805549 = -1.2156e8 vs -1.2096e8. off 0.5%
    # -61.7: 35*-8.94e8 + 96.3*-234800 = -3.129e10 - 2.26e7 = -3.131e10 vs -3.0807e10. off 1.6%
    # Not better.
    # Let me try assuming it's x^5 * 114 for x>=0, and for x<0 maybe x^5 * 114 * (something).
    # -61.7: obs/114 = -2.70e8. x^5=-8.94e8. ratio 0.302.
    # -50.4: obs/114 = -9.85e7. x^5=-3.25e8. ratio 0.303.
    # -24.3: obs/114 = -2.596e6. x^5=-8.47e6. ratio 0.307.
    # -20.3: obs/114 = -1.061e6. x^5=-3.45e6. ratio 0.307.
    # -6: obs/114 = -2570. x^5=-7776. ratio 0.330.
    # So ratio ~0.303 for large |x|, drifting to 0.33 near 0. Hmm.
    # Maybe y = 114*x^5 for x>=0, y = 114*x^5*0.303 for x<0? But then -6 would be -7776*114*0.303=-268600 vs -292916.
    # The drift near 0 suggests a lower-order term.
    # Let's fit y = a*x^5 + b*x^3 + c*x for x<0 using 3 points.
    # -61.7: a*(-8.94e8) + b*(-234800) + c*(-61.7) = -3.0807e10
    # -24.3: a*(-8.47e6) + b*(-14349) + c*(-24.3) = -2.9594e8
    # -6: a*(-7776) + b*(-216) + c*(-6) = -292916
    # This is getting complex. Let me just use a simpler model: piecewise x^5 with different coefficients, and accept some error.
    # Actually, wait. Let me reconsider the whole thing. Maybe it's not x^5.
    # Let me check x=2.9: obs 24006. 2.9^5=205. 24006/205=117.1. 
    # x=21.3: 21.3^5=4.38e6. 4.99e8/4.38e6=114.0.
    # x=66: 66^5=1.25e9. 1.42e11/1.25e9=113.6.
    # x=88.2: 88.2^5=5.33e9. 6.07e11/5.33e9=113.9.
    # So for x>=0, coefficient ~114, but 2.9 gives 117. Slight drift near 0.
    # Maybe y = 114*x^5 + 114*x? 2.9: 114*205 + 114*2.9 = 23370+330=23700 vs 24006. closer.
    # Or y = 114*x^5 + c*x. 2.9: 23370 + 2.9c = 24006 -> c=219. 
    # Check 21.3: 114*4.38e6 + 219*21.3 = 4.99e8 + 4665 = 4.99e8. ok.
    # So maybe y = 114*x^5 + 219*x for x>=0? But 219 seems arbitrary.
    # Hmm, maybe it's 114*(x^5 + x)? 2.9: 114*(205+2.9)=114*207.9=23700. still off.
    # Let me just go with y = 114*x^5 for x>=0 and y = 35*x^5 for x<0, with a note.
    # Actually, let me reconsider: could it be x^5 * 114 for x>=0 and x^5 * 35 for x<0, but 35 = 114 * 0.307?
    # Or maybe the function is x^5 * 114 for x>=0, and for x<0 it's x^5 * 114 * (1/3.25)? 
    # Let me just implement piecewise and note uncertainty.
    import math
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x >= 0:
                y = 114.0 * (x ** 5)
            else:
                y = 35.0 * (x ** 5)
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
