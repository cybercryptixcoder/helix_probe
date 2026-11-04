import math

def predict(probe):
    # Model hypothesis: f(x) = sign(x) * |x|^k * c  ... let's test scaling.
    # Look at magnitudes: x=5.3 -> 479722 ; x=38.6 -> 9.7e9 ; x=92.5 -> 7.7e11
    # log-log: ln(479722)=13.08 at ln(5.3)=1.67; ln(9.7e9)=22.99 at ln(38.6)=3.65
    # slope ~ (22.99-13.08)/(3.65-1.67)=9.91/1.98=5.0
    # x=92.5: ln=4.53, ln(7.7e11)=27.37; slope (27.37-22.99)/(4.53-3.65)=4.38/0.88=4.98
    # So f(x) ~ sign(x)*|x|^5 * c. Check c: 5.3^5=4182 -> 479722/4182=114.7
    # 38.6^5=8.57e7 -> 9.7e9/8.57e7=113.2 ; 92.5^5=6.77e9 -> 7.7e11/6.77e9=113.7
    # c ~ 113.5. Check negative: x=-93.8: 93.8^5=7.26e9 *113.5=8.24e11, observed -2.49e11. Off!
    # Hmm negative side differs. x=-39.2: 39.2^5=9.26e7*113.5=1.05e10, obs -3.2e9. ratio 0.30
    # x=-123.2: 123.2^5=2.84e10*113.5=3.22e12, obs -9.7e11, ratio 0.30
    # x=-117.6: 117.6^5=2.25e10*113.5=2.55e12, obs -7.7e11, ratio 0.30
    # x=-56.7: 56.7^5=5.86e8*113.5=6.65e10, obs -2.02e10, ratio 0.30
    # So negative side: c ~ 34 (=113.5/3.33). Hmm 113.5/34 ~ 3.34.
    # Check small negatives: x=-14: 14^5=537824*34=1.83e7, obs -1.91e7. close!
    # x=-3.3: 3.3^5=391*34=13300, obs -16159. ratio 1.21... hmm
    # x=-1.4: 1.4^5=5.38*34=183, obs -269. ratio 1.47
    # x=-8.5: 8.5^5=44371*34=1.51e6, obs -1.62e6. ratio 1.07
    # x=-25.1: 25.1^5=9.96e6*34=3.39e8, obs -3.48e8. good
    # x=-47.1: 47.1^5=2.32e8*34=7.9e9, obs -8.0e9. good
    # x=-73.3: 73.3^5=2.12e9*34=7.2e10, obs -7.28e10. good
    # x=-127.4: 127.4^5=3.36e10*34=1.14e12, obs -1.15e12. good
    # x=-103: 103^5=1.16e10*34=3.94e11, obs -3.98e11. good
    # x=-97.6: 97.6^5=8.86e9*34=3.01e11, obs -3.04e11. good
    # So negative side c~34 works for |x|>~10. Small ones deviate.
    # Positive side: check more. x=74.8: 74.8^5=2.34e9*113.5=2.66e11, obs 2.66e11. 
    # x=95.2: 95.2^5=7.82e9*113.5=8.88e11, obs 8.90e11. 
    # x=5.3: 5.3^5=4182*113.5=474,700, obs 479722. good
    # x=15.7: 15.7^5=953,000*113.5=1.08e8, obs 1.08e8. good
    # x=7.1: 7.1^5=18042*113.5=2.05e6, obs 2.06e6. good
    # x=-3.3 obs -16159. 3.3^5=391. 16159/391=41.3. Hmm not 34.
    # x=-1.4: 1.4^5=5.378. 269/5.378=50.0. Hmm.
    # x=-7.3 (E17): 7.3^5=20730. obs -766341. 766341/20730=36.97
    # x=-23.1: 23.1^5=6.58e6. obs -2.30e8. ratio 34.96
    # x=-36.6: 36.6^5=6.57e7. obs -2.28e9. ratio 34.7
    # x=-48.3: 48.3^5=2.63e8. obs -9.08e9. ratio 34.5
    # x=-63.8: 63.8^5=1.06e9. obs -3.64e10. ratio 34.4
    # x=-124.8: 124.8^5=3.03e10. obs -1.04e12. ratio 34.3
    # So negative c ~ 34-35 for larger, drifting up for small.
    # Positive side small: x=0.9 (E15): 0.9^5=0.59049. obs 23.9947. ratio 40.6
    # x=2.2 (E17): 2.2^5=51.54. obs 6089.15. ratio 118.1
    # x=2.9 (E1): 2.9^5=205.1. Let's find E1 y... not given fully. 
    # x=5.3 ratio 114.7. x=7.1 ratio 114.2. x=15.7 ratio 113.8. x=38.6 ratio 113.2.
    # So positive c ~ 113.5 for |x|>~5, but deviates small.
    # x=0.9: 23.99. 0.9^5=0.59049. 23.99/0.59=40.6. Hmm.
    # Maybe it's not exactly x^5. Let's check x=2.2: 6089. 2.2^5=51.54. 
    # Maybe f = a*x^5 + b*x^3 + ... Let's fit positive small.
    # x=0.9 -> 23.99 ; x=2.2 -> 6089 ; x=5.3 -> 479722 ; x=7.1 -> 2.06e6
    # Try x^5*113.5: 0.9->67, 2.2->5850, 5.3->474700, 7.1->2.05e6
    # At 2.2 predicted 5850 vs 6089 close. At 0.9 predicted 67 vs 24. off.
    # Hmm maybe there's a small x term. Let's try f = 113.5*x^5 - something?
    # Actually 0.9: 113.5*0.59049=67.0. obs 23.99. diff -43.
    # 2.2: 113.5*51.54=5850. obs 6089. diff +239.
    # Not clean. Let's check x=1.2 (E2): need y. Not shown.
    # Let's check x=2.0 (E6): not shown.
    # Let's check x=2.9 (E1): not shown.
    # Hmm. Let's check x=-1.4: -269. -34*5.378=-183. obs -269. 
    # -1.4 with c=50: -269. 
    # x=-3.3: -16159. 3.3^5=391. c=41.3
    # x=-7.3: -766341. 7.3^5=20730. c=36.97
    # x=-8.5: -1.62e6. 8.5^5=44371. c=36.5
    # x=-14: -1.91e7. 14^5=537824. c=35.5
    # x=-23.1: c=34.96
    # x=-25.1: c=34.9
    # So negative c drifts from ~50 at x=-1.4 down to 34 at large.
    # Positive c drifts from ~40 at x=0.9 up to 113.5.
    # This suggests maybe f(x) = x^5 * something + lower order, OR there's a piecewise.
    # Actually maybe f(x) = x^5 * (a + b/x^2 + ...)? 
    # For positive: c(x) = 113.5 + b/x^2. At x=0.9: 40.6 = 113.5 + b/0.81 -> b=-59. At x=2.2: 118.1=113.5+b/4.84 -> b=22. inconsistent.
    # Let's reconsider. Maybe f(x) = x^5 * 113.5 for x>0 and x^5*34 for x<0, plus a correction near 0.
    # Actually let's check: is there an interval where it behaves differently? "There may be an interval inside the domain where the function behaves differently."
    # Small x region! Let's check x near 0.
    # x=0.9 -> 23.99 ; x=-1.4 -> -269 ; x=-3.3 -> -16159 ; x=2.2 -> 6089
    # Hmm. Let's check x=-1.4: -269. x=0.9: 24. 
    # What if small region is different function like x^3 or x^7?
    # x=0.9: 23.99. 0.9^3=0.729. 23.99/0.729=32.9. 0.9^7=0.478. 50.2
    # x=2.2: 6089. 2.2^3=10.65. 571. 2.2^7=249. 24.4
    # x=-1.4: -269. 1.4^3=2.744. 98. 1.4^7=10.54. 25.5
    # x=-3.3: -16159. 3.3^3=35.9. 450. 3.3^7=4261. 3.79
    # Hmm inconsistent.
    # Let's just go with x^5 piecewise: positive c=113.5, negative c=34, with small-x correction.
    # Actually let me reconsider the whole thing. Maybe it's sign(x)*|x|^5 * c where c depends on sign.
    # Positive: 113.5, negative: 34. Ratio 113.5/34 = 3.34.
    # But small x deviates. Let me check if maybe it's x^5 + x^3 or similar.
    # Positive: f = A*x^5 + B*x^3. 
    # x=5.3: 479722 = A*4182 + B*148.9
    # x=7.1: 2.06e6 = A*18042 + B*357.9
    # From these: solve. 479722/4182=114.7. Let's do: 
    # 4182A + 148.9B = 479722
    # 18042A + 357.9B = 2060040
    # Multiply first by 2.404: 10054A+358B=1.153e6. Subtract: (18042-10054)A = 2060040-1153000=907040. 7988A=907040. A=113.5. B=(479722-4182*113.5)/148.9=(479722-474657)/148.9=5065/148.9=34.0
    # Check x=2.2: 113.5*51.54+34*10.65=5850+362=6212. obs 6089. close-ish.
    # x=0.9: 113.5*0.59049+34*0.729=67.0+24.8=91.8. obs 23.99. off.
    # Hmm.
    # Let me try f = A*x^5 + B*x^3 + C*x for positive.
    # x=0.9: 23.99 = A*0.59049+B*0.729+C*0.9
    # x=2.2: 6089 = A*51.54+B*10.65+C*2.2
    # x=5.3: 479722 = A*4182+B*148.9+C*5.3
    # This is getting complex. Given time, let me just do piecewise x^5 with sign-dependent c, accept small-x error.
    # Actually wait, let me reconsider negative small.
    # x=-1.4: -269. x^5 term: -34*5.378=-183. Need -86 more.
    # x=-3.3: -16159. -34*391=-13294. Need -2865 more.
    # x=-7.3: -766341. -34*20730=-704820. Need -61521 more.
    # x=-8.5: -1.62e6. -34*44371=-1.509e6. Need -111000.
    # x=-14: -1.91e7. -34*537824=-1.829e7. Need -810000.
    # x=-23.1: -2.30e8. -34*6.58e6=-2.237e8. Need -6.3e6.
    # So there's an extra negative term. x^3? -1.4^3=-2.744. -86/-2.744=31.3
    # -3.3^3=-35.9. -2865/-35.9=79.8. inconsistent.
    # x^7? -1.4^7=-10.54. -86/-10.54=8.2. -3.3^7=-4261. -2865/-4261=0.67. no.
    # Hmm. Let me just go with x^5 piecewise and accept some error. Actually let me reconsider.
    # Maybe it's |x|^5 * sign(x) * c but c is a function... no.
    # Let me just check: is it maybe x^5 * 113.5 for x>0, and for x<0 it's -|x|^5*34? 
    # The small-x deviation might be noise or a different regime.
    # Actually, let me reconsider: maybe the whole thing is x^5 * (some smooth function).
    # Let me just go with the piecewise and add a small correction term.
    # Given the difficulty, I'll model: f(x) = sign(x)*|x|^5*c(sign) with c_pos=113.5, c_neg=34.
    # And for |x|<4 maybe different. Let me check |x|<4 data:
    # x=0.9: 23.99 ; x=-1.4: -269 ; x=2.2: 6089 ; x=-3.3: -16159 ; x=2.0(E6):? ; x=2.9(E1):?
    # x=1.2(E2):? 
    # Hmm. 0.9->24, 2.2->6089. That's a jump. 2.2^5*113.5=5850. So 2.2 fits x^5. 0.9 doesn't.
    # Maybe 0.9 is in a different regime. 0.9^5*113.5=67, obs 24. 
    # What if for |x|<1 it's x^3*33? 0.9^3*33=24.06. Yes! 
    # x=-1.4: |x|>1. -1.4^5*34=-183, obs -269. Hmm.
    # What if |x|<2 different? x=-1.4: -269. x^3*? 1.4^3=2.744. 269/2.744=98. 
    # x=0.9: 24/0.729=32.9. inconsistent.
    # I'll just go with x^5 piecewise, it's the dominant behavior. Small x I'll use x^5 too.
    # Let me refine c values. Positive: use 113.5. Negative: use 34.3.
    # Actually let me check positive more carefully with E22: x=79.1: 79.1^5=3.10e9*113.5=3.52e11, obs 3.52e11. 
    # x=96.0: 96^5=8.15e9*113.5=9.25e11, obs 9.28e11. 
    # x=80.0: 80^5=3.28e9*113.5=3.72e11, obs 3.73e11. 
    # x=127.9: 127.9^5=3.42e10*113.5=3.88e12, obs 3.90e12. 
    # x=124.6: 124.6^5=3.00e10*113.5=3.41e12, obs 3.42e12. 
    # Great, c_pos=113.5 solid.
    # Negative: E22 x=-79.9: 79.9^5=3.26e9*34.3=1.12e11, obs -1.12e11. 
    # x=-106.6: 106.6^5=1.38e10*34.3=4.73e11, obs -4.73e11. 
    # Great c_neg=34.3.
    # Small x: I'll just use same formula. Accept error.
    # Actually let me reconsider small x once more. x=0.9->24, x=2.2->6089, x=5.3->479722.
    # Ratios: 6089/24=254 for x ratio 2.44. 2.44^5=86. 2.44^6=210. 2.44^6.2~254. Hmm.
    # 479722/6089=78.8 for x ratio 2.41. 2.41^5=81. close to 78.8.
    # 6089/24=254 for 2.44. 2.44^5=86, not 254. So small x is steeper.
    # Maybe x^6? 2.44^6=210. Still not 254. x^6.3?
    # I'll just use x^5 and note uncertainty.
    # Actually, let me reconsider: maybe it's x^5 + x^7 or similar for small.
    # 0.9: 113.5*0.59049=67. obs 24. So less than x^5.
    # Maybe there's a subtraction. Or maybe small x uses different.
    # I'll go with x^5 piecewise. Good enough for most.
    out = []
    for x in probe.get("x", []):
        try:
            if x >= 0:
                y = 113.5 * (x ** 5)
            else:
                y = -34.3 * ((-x) ** 5)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
