import math

def predict(probe):
    # Observations from E1:
    # For x >= 0 (except x=0): y ≈ 2.4 * x + small offset? Let's check:
    #   x=0.5 -> 3.0, x=1 -> 4.2, x=2 -> 6.6, x=4 -> 11.4, x=8 -> 21.0,
    #   x=16 -> 40.2, x=32 -> 78.6, x=64 -> 155.4, x=128 -> 309.0
    #   These fit y ≈ 2.4*x + 1.8 roughly. Check: 2.4*0.5+1.8=3.0 ✓, 2.4*1+1.8=4.2 ✓,
    #   2.4*2+1.8=6.6 ✓, 2.4*4+1.8=11.4 ✓, 2.4*8+1.8=21.0 ✓, 2.4*16+1.8=40.2 ✓,
    #   2.4*32+1.8=78.6 ✓, 2.4*64+1.8=155.4 ✓, 2.4*128+1.8=309.0 ✓
    # So for x > 0: y = 2.4*x + 1.8
    #
    # For x < 0: values are 2.4*x + 1.8 as well?
    #   x=-0.5: 2.4*(-0.5)+1.8 = 0.6, but observed 10.5. No.
    #   x=-1: 2.4*(-1)+1.8 = -0.6, observed 9.3. No.
    #   x=-2: -3.0, observed 6.9. No.
    #   x=-4: -7.8, observed 2.1. No.
    #   x=-8: -17.4, observed -7.5. No.
    #   x=-16: -36.6, observed -26.7. No.
    #   x=-32: -75.0, observed -65.1. No.
    #   x=-64: -151.8, observed -141.9. No.
    #   x=-100: -238.2, observed -228.3. No.
    #   x=-128: -305.4, observed -295.5. No.
    # For x<0, observed = 2.4*x + 1.8 + 10.2? Check:
    #   -0.5: 0.6+10.2=10.8 vs 10.5 (close)
    #   -1: -0.6+10.2=9.6 vs 9.3
    #   -2: -3.0+10.2=7.2 vs 6.9
    #   -4: -7.8+10.2=2.4 vs 2.1
    #   -8: -17.4+10.2=-7.2 vs -7.5
    #   -16: -36.6+10.2=-26.4 vs -26.7
    #   -32: -75.0+10.2=-64.8 vs -65.1
    #   -64: -151.8+10.2=-141.6 vs -141.9
    #   -100: -238.2+10.2=-228.0 vs -228.3
    #   -128: -305.4+10.2=-295.2 vs -295.5
    # Off by -0.3 consistently. So for x<0: y = 2.4*x + 1.8 + 9.9 = 2.4*x + 11.7
    # Check: -0.5: -1.2+11.7=10.5 ✓, -1: -2.4+11.7=9.3 ✓, -2: -4.8+11.7=6.9 ✓,
    #   -4: -9.6+11.7=2.1 ✓, -8: -19.2+11.7=-7.5 ✓, -16: -38.4+11.7=-26.7 ✓,
    #   -32: -76.8+11.7=-65.1 ✓, -64: -153.6+11.7=-141.9 ✓, -100: -240+11.7=-228.3 ✓,
    #   -128: -307.2+11.7=-295.5 ✓
    # So for x<0: y = 2.4*x + 11.7
    #
    # At x=0: observed -228.87. That's a special value, not on either line (1.8 or 11.7).
    # This suggests a special interval or point at x=0. Possibly a discontinuity / special value.
    # The problem statement mentions "an interval inside the domain where the function behaves differently".
    # x=0 gives -228.87 which is far off. Maybe there's a special interval around 0.
    # We only have x=0 as evidence. Could be a single point, could be an interval.
    # Best guess: special value at x=0 only (or small interval). Mark with "?".
    #
    # Model:
    #   x > 0: y = 2.4*x + 1.8
    #   x < 0: y = 2.4*x + 11.7
    #   x == 0: y = -228.87 (special, "?" interval unknown)
    
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x > 0:
                ys.append(2.4*x + 1.8)
            elif x < 0:
                ys.append(2.4*x + 11.7)
            else:
                ys.append(-228.87)
        except Exception:
            ys.append(None)
    return {"y": ys}
