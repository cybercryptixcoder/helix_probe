def predict(probe):
    # Linear: y = 2.42 * x [E1: 88.2->213.48, 66->160.2, -20.3->-37.02, etc.]
    # Check ratio: 213.48/88.2=2.4204, 160.2/66=2.427, -37.02/-20.3=1.823? no
    # Recompute: -37.02/-20.3 = 1.823... inconsistent. Let's check others.
    # 8.76/2.9=3.02, -46.62/-24.3=1.918, 176.28/72.7=2.424, -109.26/-50.4=2.168
    # -2.7/-6.0=0.45, 52.92/21.3=2.484
    # Not linear. Try y = 2.42*x rounded? 88.2*2.42=213.44 ~213.48 ok
    # 66*2.42=159.72 vs 160.2 no
    # Try y = x*2.42 + something? 
    # Look: 2.9->8.76, 8.76/2.9=3.02. -6->-2.7, ratio 0.45.
    # Maybe y = 2.42*x but with rounding to 2 decimals? 66*2.42=159.72 not 160.2
    # Try 2.4*x: 88.2*2.4=211.68 no
    # Try x*2.42: 21.3*2.42=51.546 vs 52.92 no
    # Hmm. 52.92/21.3=2.4845. 213.48/88.2=2.4204.
    # Maybe y = 2.42*x + 0.06*? 
    # Try y = 2.42*x + 0.02*x*something
    # Actually maybe y = 2.42*x rounded to nearest 0.06? 
    # Let's look for pattern: values 213.48,160.2,-37.02,-136.38,8.76,-46.62,176.28,-109.26,-2.7,52.92
    # All divisible by 0.06? 213.48/0.06=3558, 160.2/0.06=2670, -37.02/0.06=-617, yes all multiples of 0.06
    # x values: 88.2,66,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6,21.3
    # 88.2/0.06=1470, 66/0.06=1100, -20.3/0.06 not integer
    # y/0.06: 3558,2670,-617,-2273,146,-777,2938,-1821,-45,882
    # x*? : 3558/1470=2.42, 2670/1100=2.427
    # Hmm 2670/1100 = 2.4272. 3558/1470=2.4204.
    # Maybe y = round(2.42*x, 2)? 66*2.42=159.72 no.
    # Try y = 2.42*x but x rounded? 
    # 160.2/2.42 = 66.198. 213.48/2.42=88.215.
    # Maybe y = 2.42*x + 0.06*round(something)
    # 213.48 - 2.42*88.2 = 213.48-213.444=0.036
    # 160.2 - 2.42*66 = 160.2-159.72=0.48
    # -37.02 - 2.42*(-20.3)= -37.02+49.126=12.106 no
    # Let me reconsider. Maybe y = 2.42*x is wrong.
    # Try y = 2.4*x: 88.2*2.4=211.68 vs 213.48 diff 1.8
    # Try y = 2.42*x: mostly close but off.
    # Look at -6 -> -2.7. ratio 0.45. That's very different!
    # 2.9 -> 8.76 ratio 3.02. -20.3 -> -37.02 ratio 1.823.
    # Maybe y = x * (2.42) but with x transformed? 
    # Or maybe y = 2.42*x for x>0, different for x<0?
    # x>0: 88.2->213.48 (2.42), 66->160.2 (2.427), 2.9->8.76 (3.02), 72.7->176.28 (2.424), 21.3->52.92 (2.484)
    # x<0: -20.3->-37.02 (1.823), -61.7->-136.38 (2.21), -24.3->-46.62 (1.918), -50.4->-109.26 (2.168), -6->-2.7 (0.45)
    # Hmm inconsistent within signs too.
    # Wait: maybe y = 2.42*x rounded to 2 decimals, but x itself... 
    # 2.9*2.42=7.018 vs 8.76. no.
    # Let me check: 8.76 = 2.9*3.02. -2.7 = -6*0.45.
    # Maybe y = 2.42*x + 0.06*k where k depends on x?
    # Actually maybe y = 2.42 * round(x)? 2.9 rounds to 3, 3*2.42=7.26 no.
    # Try y = 2.42*x with x rounded to integer: 88.2->88, 88*2.42=212.96 no.
    # Hmm. Let me try y = 2.42*x + 0.06*floor(x)? 
    # 88.2: 213.444 + 0.06*88=213.444+5.28 no.
    # Let me try a different slope. Maybe y = 2.42*x is close but actual is different.
    # Solve from two points: (88.2,213.48) and (66,160.2): slope=(213.48-160.2)/(88.2-66)=53.28/22.2=2.4
    # intercept: 160.2-2.4*66=160.2-158.4=1.8
    # Check: 2.4*88.2+1.8=211.68+1.8=213.48 ✓
    # 2.4*66+1.8=158.4+1.8=160.2 ✓
    # 2.4*(-20.3)+1.8=-48.72+1.8=-46.92 vs -37.02 ✗
    # Hmm close-ish but no.
    # Try (66,160.2) and (72.7,176.28): slope=(176.28-160.2)/(72.7-66)=16.08/6.7=2.4
    # intercept: 160.2-2.4*66=1.8. Same! So y=2.4x+1.8 for positives.
    # Check 2.9: 2.4*2.9+1.8=6.96+1.8=8.76 ✓
    # Check 21.3: 2.4*21.3+1.8=51.12+1.8=52.92 ✓
    # Check -20.3: 2.4*(-20.3)+1.8=-48.72+1.8=-46.92 vs -37.02 ✗
    # So for x>0: y=2.4x+1.8. For x<0 different.
    # x<0: (-20.3,-37.02),(-61.7,-136.38),(-24.3,-46.62),(-50.4,-109.26),(-6,-2.7)
    # slope from (-20.3,-37.02),(-61.7,-136.38): (-136.38+37.02)/(-61.7+20.3)=(-99.36)/(-41.4)=2.4
    # intercept: -37.02-2.4*(-20.3)=-37.02+48.72=11.7
    # Check -24.3: 2.4*(-24.3)+11.7=-58.32+11.7=-46.62 ✓
    # Check -50.4: 2.4*(-50.4)+11.7=-120.96+11.7=-109.26 ✓
    # Check -6: 2.4*(-6)+11.7=-14.4+11.7=-2.7 ✓
    # So for x<0: y=2.4x+11.7
    # For x>0: y=2.4x+1.8
    # At x=0? unknown. Maybe there's a jump.
    # Difference in intercept: 11.7-1.8=9.9. Hmm.
    # Maybe it's y=2.4x+1.8 for x>=0, and y=2.4x+11.7 for x<0.
    # Or maybe there's a region. Let's just implement piecewise.
    # Actually maybe: y = 2.4*x + 1.8 + 9.9*(x<0)? 
    # Or maybe y = 2.4*x + 1.8 + 9.9 if x<0.
    # Could be y = 2.4*x + 1.8 + 9.9*[x<0]. 
    # Or maybe the function is y = 2.4*x + 1.8 for x>=0 and y=2.4*x+11.7 for x<0.
    # Let's go with piecewise. But what about x=0? Unknown. Guess 1.8 (positive branch).
    # Actually maybe there's a threshold region. But only one experiment. Keep simple.
    out=[]
    for x in probe["x"]:
        if x>=0:
            out.append(2.4*x+1.8)
        else:
            out.append(2.4*x+11.7)
    return {"y":out}
