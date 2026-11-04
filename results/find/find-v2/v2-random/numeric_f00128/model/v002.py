import math

def predict(probe):
    # Observations:
    # E1: (88.2,-1479),(66,-1104),(-20.3,139.6),(-61.7,419.5),(2.9,-37.8),
    #     (-24.3,166.7),(72.7,-1217),(-50.4,343.1),(-6,43),(21.3,-348.8)
    # E2: (104.5,-1754.8),(1.2,-8.57),(-55.8,379.6),(65.5,-1095.7),(30.3,-500.9),
    #     (-63.9,434.4),(104.9,-1761.6),(123.6,-2077.6),(79.4,-1330.7),(103,-1729.5)
    # Sign: positive x -> negative y; negative x -> positive y. Odd-ish, monotone decreasing.
    # Magnitude grows faster than linear at large |x| (e.g. 123.6 -> -2077, ratio -16.8;
    #   104.5 -> -1755 ratio -16.8; 30.3 -> -501 ratio -16.5; 1.2 -> -8.6 ratio -7.1).
    # Small |x| has smaller ratio (~7), large |x| ratio ~16.8. Looks like a smooth
    #   saturating / sigmoid-ish odd function: y = -A * tanh(x/s) * something, or
    #   y ≈ -k*x with k growing with |x|. Let's fit y = -a*x - b*x^3? Check:
    #   x=1.2: -a*1.2 - b*1.7 = -8.57 -> a*1.2 ≈ 8.57 (b negligible) -> a≈7.1
    #   x=30.3: -7.1*30.3 - b*27800 = -501 -> -215 - 27800b = -501 -> b=0.0103
    #   x=123.6: -7.1*123.6 - 0.0103*1.888e6 = -877 - 19447 = -20324. Too big.
    # So not cubic. Try y = -a*x - b*x*|x| (quadratic-ish):
    #   x=30.3: -7.1*30.3 - b*918 = -501 -> -215 -918b=-501 -> b=0.311
    #   x=123.6: -7.1*123.6 - 0.311*15277 = -877 - 4751 = -5628. Too big.
    # Try saturating: y = -A*tanh(x/s). At large x, y->-A. But 123.6->-2077 and
    #   104.5->-1755, still growing, so not saturated yet. 
    # Try y = -a*x - b*x^3 with small b won't fit. Let's try power law y=-c*x*|x|^p.
    #   ratio |y/x|: at x=1.2: 7.1; x=30.3: 16.5; x=104.5: 16.8; x=123.6: 16.8.
    #   Ratio saturates ~16.8 for |x|>30. So slope ~16.8 at large, ~7 at small.
    # This looks like y = -16.8*x + correction that vanishes for large |x|, OR
    #   a smooth transition. Actually: at small x slope 7, at large x slope 16.8.
    # Try y = -a*x - b*tanh(x/s)*x? Hmm.
    # Better: fit y = -a*x - b*sinh(x/s)? Let's just do a smooth odd fit.
    # Try y = -p*x - q*x^3 but with saturation: y = -p*x - q*x^3/(1+(x/r)^2).
    # Simpler: use two-regime. Small |x|: slope ~7. Large |x|: slope ~16.8.
    # Transition around |x|~20-30. 
    # Let's fit y = -a*x - b*x*(1-exp(-(x/s)^2)) ... 
    # Actually simplest: y = -a*x - b*x^3 works for small, but overshoots large.
    # Let's fit piecewise linear-ish: slope 7 for |x|<15, slope 16.8 for |x|>40,
    #   smooth between. Check E1: x=2.9 -> -37.8, ratio -13.0. Hmm that's between.
    #   x=-6 -> 43, ratio -7.2. x=21.3 -> -348.8 ratio -16.4. x=-20.3->139.6 ratio -6.9.
    # Wait: x=2.9 ratio 13, x=-6 ratio 7.2, x=21.3 ratio 16.4, x=-20.3 ratio 6.9.
    # Asymmetric! Positive small x has higher ratio than negative small x?
    #   x=2.9: 13.0; x=-6: 7.2; x=-20.3: 6.9; x=21.3: 16.4; x=-24.3: 6.9; x=30.3: 16.5
    #   x=-50.4: 6.8; x=-55.8: 6.8; x=-61.7: 6.8; x=-63.9: 6.8
    #   x=65.5: 16.7; x=66: 16.7; x=72.7: 16.7; x=79.4: 16.8; x=88.2: 16.8
    #   x=103: 16.8; x=104.5: 16.8; x=104.9: 16.8; x=123.6: 16.8
    # CLEAR: positive x -> slope ~16.8 (for |x|>~20), negative x -> slope ~6.8!
    #   And small positive x (2.9) slope 13, small negative (-6) slope 7.2.
    # So it's NOT odd. Positive side: steeper. Negative side: shallower.
    # Let's fit separately.
    # Positive x: slope ~16.8 for x>20. At x=2.9 slope 13. At x=1.2 slope 7.1.
    #   So positive side: y = -16.8*x + something? x=1.2: -16.8*1.2=-20 vs -8.57.
    #   Looks like positive side saturates slope: y = -16.8*x + 9.7*tanh(x/s)?
    #   Actually maybe y = -16.8*x + c*(1-exp(-x/s)). At x=1.2: -20.2 + c*(1-e^-..)
    # Negative x: slope ~6.8 for x<-20. At x=-6 slope 7.2, x=-20.3 slope 6.9.
    #   So negative side is nearly linear slope 6.8-7.2 throughout!
    #   Check: -6.8*-6=40.8 vs 43 ok. -6.8*-20.3=138 vs 139.6 ok.
    #   -6.8*-61.7=419.6 vs 419.5 PERFECT. -6.8*-50.4=342.7 vs 343.1 ok.
    #   -6.8*-55.8=379.4 vs 379.6 ok. -6.8*-63.9=434.5 vs 434.4 ok.
    #   -6.8*-24.3=165.2 vs 166.7 ok. So negative side: y = -6.8*x (approx).
    # Positive side: x=21.3:-348.8 (ratio16.4), x=30.3:-500.9(16.5), x=65.5:-1095.7(16.7),
    #   x=66:-1104.2(16.7), x=72.7:-1217.4(16.7), x=79.4:-1330.7(16.8),
    #   x=88.2:-1479.4(16.8), x=103:-1729.5(16.8), x=104.5:-1754.8(16.8),
    #   x=104.9:-1761.6(16.8), x=123.6:-2077.6(16.8).
    #   Slope approaches 16.8. At x=21.3 ratio 16.4, x=30.3 ratio 16.5.
    #   Small: x=1.2 ratio 7.1, x=2.9 ratio 13.0.
    #   So positive side: slope transitions from ~7 (at x=0) to 16.8 (at large x).
    #   Model: y = -16.8*x + 9.8*x*exp(-x/s)? At x=0 slope = -16.8+9.8=-7. 
    #   At large x slope -16.8. Transition scale s.
    #   x=1.2: -16.8*1.2 + 9.8*1.2*exp(-1.2/s) = -8.57
    #     -20.16 + 11.76*exp(-1.2/s) = -8.57 -> 11.76*exp(-1.2/s)=11.59 -> exp=0.985 -> s~80
    #   x=2.9: -16.8*2.9 + 9.8*2.9*exp(-2.9/80) = -48.72 + 28.42*0.964 = -48.72+27.4=-21.3
    #     vs -37.8. Not great.
    #   Try s=10: x=1.2: -20.16+11.76*0.887=-20.16+10.43=-9.73 vs -8.57 close.
    #     x=2.9: -48.72+28.42*0.748=-48.72+21.26=-27.5 vs -37.8. off.
    #   Hmm. Maybe transition is sharper. Let's try y = -a*x - b*x^2 for positive?
    #   x=1.2: -a*1.2-b*1.44=-8.57; x=2.9:-a*2.9-b*8.41=-37.8
    #   From eq1: a+1.2b=7.14. eq2: a+2.9b=13.03. Subtract: 1.7b=5.89->b=3.46,a=3.0
    #   Check x=21.3: -3*21.3-3.46*453.7=-63.9-1570=-1634 vs -348.8. WAY off.
    #   So not quadratic. 
    # Let me reconsider: maybe positive side is y=-16.8*x for x>~15, and there's a
    #   separate small-x behavior. x=2.9->-37.8: -16.8*2.9=-48.7, actual -37.8, diff +10.9
    #   x=1.2->-8.57: -16.8*1.2=-20.2, diff +11.6
    #   So y = -16.8*x + 11.5*(something that's ~1 for small x, 0 for large).
    #   At x=21.3: -16.8*21.3=-357.8, actual -348.8, diff +9.0. Still ~9!
    #   At x=30.3: -16.8*30.3=-509, actual -500.9, diff +8.1.
    #   At x=65.5: -16.8*65.5=-1100.4, actual -1095.7, diff +4.7.
    #   At x=88.2: -16.8*88.2=-1481.8, actual -1479.4, diff +2.4.
    #   At x=123.6: -16.8*123.6=-2076.5, actual -2077.6, diff -1.1.
    #   So diff decreases from ~11.5 to 0. Maybe y = -16.8*x + 12*exp(-x/50)?
    #   x=1.2: -20.2+12*0.976=-20.2+11.7=-8.5 ✓
    #   x=2.9: -48.7+12*0.944=-48.7+11.3=-37.4 ✓ (vs -37.8)
    #   x=21.3: -357.8+12*0.653=-357.8+7.8=-350 ✓ (vs -348.8)
    #   x=30.3: -509+12*0.545=-509+6.5=-502.5 ✓ (vs -500.9)
    #   x=65.5: -1100.4+12*0.270=-1100.4+3.2=-1097.2 ✓ (vs -1095.7)
    #   x=88.2: -1481.8+12*0.171=-1481.8+2.05=-1479.7 ✓ (vs -1479.4)
    #   x=123.6: -2076.5+12*0.084=-2076.5+1.0=-2075.5 (vs -2077.6) ok
    #   EXCELLENT fit! Positive side: y = -16.8*x + 12*exp(-x/50)
    # Negative side: y = -6.8*x. Check small: x=-6: 40.8 vs 43. x=-20.3: 138 vs 139.6.
    #   Slight offset? diff ~2. Maybe y=-6.8*x+2? x=-6:40.8+2=42.8✓; x=-20.3:138+2=140✓
    #   x=-61.7:419.6+2=421.6 vs 419.5. Hmm over. Maybe no offset, just -6.8*x.
    #   Let's refine slope: -61.7->419.5 gives 6.80; -50.4->343.1 gives 6.81; -55.8->379.6 gives 6.80.
    #   -63.9->434.4 gives 6.80. -24.3->166.7 gives 6.86. -20.3->139.6 gives 6.88.
    #   -6->43 gives 7.17. So slope slightly higher at small |x|. 
    #   Model negative: y = -6.8*x + small correction. Use y=-6.8*x + 2*exp(x/30)? 
    #   x=-6: 40.8+2*0.819=42.4 vs 43 ok. x=-20.3:138+2*0.508=139 vs 139.6 ok.
    #   x=-61.7:419.6+2*0.128=419.9 vs 419.5 ok. Good enough.
    # Final model:
    #   if x>=0: y = -16.8*x + 12*exp(-x/50)
    #   if x<0:  y = -6.8*x + 2*exp(x/30)
    out=[]
    for x in probe.get("x",[]):
        try:
            x=float(x)
            if x>=0:
                y=-16.8*x+12.0*math.exp(-x/50.0)
            else:
                y=-6.8*x+2.0*math.exp(x/30.0)
            out.append(y)
        except Exception:
            out.append(None)
    return {"y":out}
