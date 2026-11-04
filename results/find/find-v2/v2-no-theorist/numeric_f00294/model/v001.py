def predict(probe):
    # f(x) = x + 17.6 for all x in [-128, 128] [E1]
    # E1: 88.2->105.8 (+17.6), 66.0->82.8 (+16.8), -20.3->-28.4 (-8.1)...
    # Wait: check differences: 105.8-88.2=17.6, 82.8-66=16.8, -28.4-(-20.3)=-8.1
    # Not constant offset. Check ratio: 105.8/88.2=1.1995, 82.8/66=1.2545
    # Check y = x + 17.6? no. Try y = 1.2*x: 88.2*1.2=105.84 ✓, 66*1.2=79.2 ✗
    # Try y = x*1.2 for 88.2 ✓ but 66 gives 79.2 vs 82.8.
    # Recheck: 82.8/66 = 1.2545. Hmm.
    # Try y = x + 17.6: 66+17.6=83.6 close to 82.8. -20.3+17.6=-2.7 vs -28.4 no.
    # Try y = 1.2x: -20.3*1.2=-24.36 vs -28.4 no.
    # Look again: 88.2->105.8, 66->82.8, -20.3->-28.4, -61.7->-69.4, 2.9->19.8,
    # -24.3->-32.4, 72.7->89.8, -50.4->-58.4, -6->-14.4, 21.3->38.8
    # diffs: 17.6, 16.8, -8.1, -7.7, 16.9, -8.1, 17.1, -8.0, -8.4, 17.5
    # Positive x: diff ~ +17; negative x: diff ~ -8.
    # So y = x + 17.6 if x>0 else x - 8.1? Check 2.9+17.6=20.5 vs 19.8 close.
    # 21.3+17.6=38.9 vs 38.8 ✓. -6-8.1=-14.1 vs -14.4 ✓. -50.4-8=-58.4 ✓.
    # 72.7+17.6=90.3 vs 89.8. 66+17.6=83.6 vs 82.8. Hmm slightly off.
    # Maybe y = 1.2x for x>0? 88.2*1.2=105.84 ✓ 66*1.2=79.2 ✗
    # Try y = x*1.2 for x in some range... 72.7*1.2=87.24 vs 89.8 no.
    # Actually diffs positive: 17.6,16.8,16.9,17.1,17.5 ~ 17.2 avg
    # negative diffs: -8.1,-7.7,-8.1,-8.0,-8.4 ~ -8.06
    # So y = x + 17.2 if x>0, x - 8.06 if x<0. But 2.9+17.2=20.1 vs 19.8.
    # Maybe y = x + 17.6 for x>0 and x - 8 for x<0. Test: 66+17.6=83.6 vs 82.8 (off 0.8)
    # Hmm. Try y = 1.2x for x>0? no.
    # Try y = x*1.2 for x>0: 88.2 ok, 66->79.2 no.
    # Look: 66->82.8, 82.8/66=1.2545. 72.7->89.8, 89.8/72.7=1.235.
    # Try y = x + 17.6 for x>0... 66 gives 83.6 not 82.8.
    # Maybe there's a threshold. 88.2 and 72.7 and 66 and 21.3 and 2.9 all positive.
    # 2.9->19.8 diff 16.9; 21.3->38.8 diff 17.5; 66->82.8 diff 16.8; 72.7->89.8 diff 17.1; 88.2->105.8 diff 17.6
    # Diffs vary. Maybe y = 1.2x for x in [0,?]... no.
    # Try y = x + 17.6 - something. Or y = 1.2x for x>0 small? 2.9*1.2=3.48 no.
    # Perhaps y = x + 17.6 for x>0, but 66: 83.6 vs 82.8. Off by 0.8.
    # Alternatively y = 1.2x - 0.5? 66*1.2-0.5=78.7 no.
    # Let's fit: positive points (2.9,19.8),(21.3,38.8),(66,82.8),(72.7,89.8),(88.2,105.8)
    # slope between 2.9 and 88.2: (105.8-19.8)/(88.2-2.9)=86/85.3=1.008. intercept ~ 19.8-2.9*1.008=16.88
    # So y ≈ x + 17 for x>0. Check 66+17=83 vs 82.8 ✓. 72.7+17=89.7 vs 89.8 ✓. 88.2+17=105.2 vs 105.8.
    # 21.3+17=38.3 vs 38.8. 2.9+17=19.9 vs 19.8 ✓.
    # So y = x + 17 for x>0.
    # negative: (-20.3,-28.4),(-61.7,-69.4),(-24.3,-32.4),(-50.4,-58.4),(-6,-14.4)
    # slope: (-58.4-(-14.4))/(-50.4-(-6))=-44/-44.4=0.99. intercept: -14.4-(-6)*0.99=-8.46
    # So y ≈ x - 8 for x<0. Check -20.3-8=-28.3 vs -28.4 ✓. -61.7-8=-69.7 vs -69.4 ✓.
    # -24.3-8=-32.3 vs -32.4 ✓. -50.4-8=-58.4 ✓. -6-8=-14 vs -14.4 ✓.
    # So: y = x + 17 if x>0, x - 8 if x<0. What about x=0? unknown, guess 0.
    # Maybe it's y = x + 17 for x>=0 and x - 8 for x<0. Or maybe threshold elsewhere.
    # Could be y = x + 17 for x>0 and x - 8 for x<=0.
    # Or maybe it's a piecewise with threshold at 0.
    out = []
    for x in probe.get("x", []):
        try:
            if x > 0:
                out.append(x + 17)
            elif x < 0:
                out.append(x - 8)
            else:
                out.append(0)
        except Exception:
            out.append(None)
    return {"y": out}
