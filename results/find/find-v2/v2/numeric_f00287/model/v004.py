import math

def predict(probe):
    # Observations:
    # - For x <= -5.1: y = -0.7*x  [E1 x=-6 -> 4.2; E2 x=-40..-10; E8 x=-6.0..-5.1 -> 4.2]
    # - For -5.0 <= x <= 18.5: y ≈ -402.3 (constant, noisy)  [E2, E4 x=10..18, E6 x=-5..18.5, E8 x=-5.0..-2.5, E12 x=-5..18]
    # - For x >= 19: y = -16.8*x  [E4 x=19 -> -319.2; E2 x=20..100; E3; E5; E7; E10]
    # Left break: sharp between -5.1 (4.2) and -5.0 (-402.3) [E8]
    # Right break: sharp between 18.5 (-402.5) and 19 (-319.2) [E6]
    # E12: x=18.9 -> -302.4, which is -16.8*18.9 = -317.52? No: -302.4 = -16*18.9.
    #   Actually -302.4/18.9 = -16.0. Hmm. But x=19 -> -319.2 = -16.8*19.
    #   So between 18.5 and 19 there's a transition. -302.4 at 18.9.
    #   Check: maybe right region is y = -16.8*x but with a breakpoint at 18.9? -16.8*18.9=-317.52 ≠ -302.4.
    #   -302.4 = -16.8*18 exactly. So maybe y = -16.8*(x-0.9)? At x=19: -16.8*18.1=-304.08 no.
    #   Let's reconsider: -302.4 = -16.8 * 18.0. So at x=18.9 output equals -16.8*18.
    #   Perhaps the linear region uses floor? Or maybe transition is gradual.
    #   E4: x=19 -> -319.2 = -16.8*19. x=20 -> -336 = -16.8*20. So at 19 it's exact.
    #   At 18.9 -> -302.4. -302.4/-16.8 = 18.0. So y = -16.8*floor(x)? At 19 floor=19 -> -319.2 ✓. At 18.9 floor=18 -> -302.4 ✓.
    #   But E10: x=20..128 all exact -16.8*x, integers, floor same. E11: x=77.6 -> -1293.6 = -16.8*77.0? -16.8*77=-1293.6 ✓. floor(77.6)=77 ✓.
    #   x=110.8 -> -1848.0 = -16.8*110 ✓ (floor 110). x=52.9 -> -873.6 = -16.8*52 ✓ (floor 52).
    #   x=94.1 -> -1579.2 = -16.8*94 ✓. x=94.8 -> -1579.2 = -16.8*94 ✓ (floor 94).
    #   x=119.7 -> -1999.2 = -16.8*119 ✓ (floor 119).
    #   So right region: y = -16.8 * floor(x) for x >= 19? But at 18.9 floor=18 gives -302.4 ✓.
    #   Wait but 18.9 < 19 and it's in linear region. So breakpoint is lower than 19.
    #   E6: x=18.5 -> -402.5 (constant), x=19 -> -319.2. So break between 18.5 and 18.9.
    #   E12: x=18.0 -> -402.37 (constant), x=18.9 -> -302.4 (linear). So break between 18.0 and 18.9.
    #   E4: x=18 -> ? not shown but E6 shows 18.0 constant. So break in (18.0, 18.9].
    #   Hmm, but floor hypothesis: at x=18.9 floor=18. If breakpoint is 18.5, then 18.5..18.9 would be linear with floor 18 -> -302.4.
    #   But E6 x=18.5 -> -402.5 constant. So breakpoint > 18.5.
    #   So breakpoint in (18.5, 18.9]. Let's guess 18.6? Or maybe it's where floor changes... no.
    #   Actually maybe the rule is: for x >= 18.6 (or some threshold), y = -16.8*floor(x). At 18.9 floor=18 -> -302.4 ✓.
    #   But then at x=19 floor=19 -> -319.2 ✓.
    #   Left region: E8 x=-5.1 -> 4.2 = -0.7*(-6)? -0.7*-5.1=3.57. But observed 4.2 = -0.7*(-6). So floor too!
    #   -0.7*floor(-5.1) = -0.7*(-6) = 4.2 ✓. x=-5.0: floor(-5.0)=-5 -> 3.5, but observed -402.27 (constant). So breakpoint at -5.0.
    #   E10: x=-120 -> 84 = -0.7*(-120) ✓ floor. x=-100 -> 70 = -0.7*(-100) ✓.
    #   E1: x=-20.3 -> ? E1 not fully shown but -0.7*floor(-20.3)=-0.7*(-21)=14.7. 
    #   E9: x=-65.6 -> 46.2 = -0.7*(-66) = 46.2 ✓ floor. x=-44.7 -> 31.5 = -0.7*(-45)=31.5 ✓. x=-79.1 -> 56.0 = -0.7*(-80)=56 ✓. x=-66.9 -> 46.9 = -0.7*(-67)=46.9 ✓.
    #   E11: x=-13.3 -> 9.8 = -0.7*(-14)=9.8 ✓. x=-107.4 -> 75.6 = -0.7*(-108)=75.6 ✓. x=-46.1 -> 32.9 = -0.7*(-47)=32.9 ✓. x=-100.1 -> 70.7 = -0.7*(-101)=70.7 ✓.
    #   So left region: y = -0.7*floor(x) for x <= -5.1 (or x < -5.0).
    #   Check x=-5.1: floor=-6 -> 4.2 ✓. x=-5.0: constant. So condition x < -5.0 or x <= -5.1.
    #   Middle: -5.0 <= x < breakpoint_right, y ≈ -402.3.
    #   Right breakpoint: between 18.5 and 18.9. Let's say 18.6? Uncertain.
    #   Actually maybe the breakpoint is at 18.5+? Let's just pick 18.6 as guess.
    #   Hmm, but maybe the constant region is -5.0 <= x < 18.6, and right is x >= 18.6 with floor.
    #   At x=18.6 floor=18 -> -302.4. At 18.5 floor=18 -> -302.4 but observed constant. So breakpoint > 18.5.
    #   Let's guess 18.6.
    out = []
    for x in probe.get("x", []):
        try:
            if x < -5.0:
                out.append(-0.7 * math.floor(x))
            elif x < 18.6:
                out.append(-402.3)
            else:
                out.append(-16.8 * math.floor(x))
        except Exception:
            out.append(None)
    return {"y": out}
