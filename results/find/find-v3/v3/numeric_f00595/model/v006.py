def predict(probe):
    # Main idea:
    # The box is essentially a "round to nearest integer, but with a special
    # negative half-integer tie rule".  For x >= 0, y = round(x) with ties
    # going up (e.g. 0.5 -> 1, 1.5 -> 2, 2.5 -> 3).
    # For x < 0, y = round(x) with ties going down (e.g. -0.5 -> -2,
    # -1.5 -> -3, -2.5 -> -4).  Away from half-integers this is just
    # ordinary nearest-integer rounding.  The evidence (E2, E4, E8, E10)
    # pins down the tie behaviour on both sides of zero.
    #
    # More precisely, for x >= 0:  y = floor(x + 0.5)
    # for x < 0:                  y = ceil(x - 0.5)
    #
    # This matches all experiments, including the apparently "off by one"
    # cases like -0.1 -> -2 (because -0.1 - 0.5 = -0.6, ceil = 0? no...).
    # Let's re-derive carefully from the data.

    # Observations:
    # E2:  0.5->1, -0.5->-2, 0.1->1, -0.1->-2, 1.5->2, -1.5->-3,
    #      3.2->4, -3.2->-5, 100->101, -100->-101
    # E4:  -0.9->-2, -0.1->-2, 0.0->-1, 0.9->1, 1.1->2, -1.1->-3,
    #      2.0->3, -2.0->-3, 50.5->51, -50.5->-52
    # E8:  2.5->3, 2.01->3, 1.5->2, 1.49->2, 0.99->1, 0.01->1,
    #      -0.01->-2, -0.99->-2, -1.49->-3, -1.5->-3, -2.01->-4,
    #      -2.5->-4, 3.99->4, 4.01->5, -3.99->-5, -4.01->-6,
    #      10.5->11, -10.5->-12, 0.5->1, -0.5->-2
    # E10: -0.5->-2, -0.25->-2, -0.75->-2, -1.0->-2, -1.25->-3,
    #      -1.75->-3, -0.99->-2, -1.01->-3, 1.0->2, 0.999->1,
    #      -0.001->-2, 0.001->1
    #
    # Pattern: for x >= 0, y = floor(x + 0.5)  (ties up)
    #          for x < 0,  y = floor(x - 0.5)  (ties down, i.e. away from zero)
    #
    # Check: x=0.0 -> floor(0.5)=0, but E4 says 0.0 -> -1. Hmm.
    # Wait E4: x=0.0 -> y=-1.  That's odd.  Let's check floor(0.0-0.5)=floor(-0.5)=-1.
    # So 0.0 behaves like the negative branch!  But E10: -0.001->-2,
    # 0.001->1.  And E2: 0.1->1.  So 0.0 -> -1 (negative branch),
    # 0.001 -> 1 (positive branch).  So the boundary is x > 0 vs x <= 0.
    #
    # Check with x=0.0: x<=0 branch: floor(0.0 - 0.5) = floor(-0.5) = -1. ✓
    # x=0.001: x>0 branch: floor(0.001+0.5)=floor(0.501)=0? But E10 says 1.
    # Hmm, that fails.  Let's recheck E10: 0.001 -> 1.0.  floor(0.501)=0.
    # So floor(x+0.5) doesn't work for small positive x.
    #
    # Let's reconsider.  Maybe it's ceil for positive?  ceil(0.001)=1 ✓
    # ceil(0.5)=1 ✓, ceil(1.5)=2 ✓, ceil(2.5)=3 ✓, ceil(3.2)=4 ✓,
    # ceil(0.1)=1 ✓, ceil(0.9)=1 ✓, ceil(0.99)=1 ✓, ceil(1.49)=2 ✓,
    # ceil(2.01)=3 ✓, ceil(3.99)=4 ✓, ceil(4.01)=5 ✓, ceil(10.5)=11 ✓,
    # ceil(50.5)=51 ✓, ceil(100)=101 ✓, ceil(1.0)=1? But E10 says 1.0->2.
    # Hmm, ceil(1.0)=1, but E10 says 2.  And E4: 2.0->3, ceil(2.0)=2. Fail.
    #
    # So it's not ceil either.  Let's tabulate positive x:
    # 0.001->1, 0.01->1, 0.1->1, 0.5->1, 0.9->1, 0.99->1, 0.999->1,
    # 1.0->2, 1.01->2, 1.1->2, 1.2->2, 1.49->2, 1.5->2, 1.99->2,
    # 2.0->3, 2.01->3, 2.5->3, 2.9->3, 3.2->4, 3.99->4, 4.01->5,
    # 10.5->11, 50.5->51, 100->101
    #
    # This looks like: y = floor(x) + 1 for x >= 0?  Check:
    # floor(0.001)+1=1 ✓, floor(0.5)+1=1 ✓, floor(0.999)+1=1 ✓,
    # floor(1.0)+1=2 ✓, floor(1.5)+1=2 ✓, floor(1.99)+1=2 ✓,
    # floor(2.0)+1=3 ✓, floor(2.5)+1=3 ✓, floor(3.2)+1=4 ✓,
    # floor(3.99)+1=4 ✓, floor(4.01)+1=5 ✓, floor(10.5)+1=11 ✓,
    # floor(50.5)+1=51 ✓, floor(100)+1=101 ✓.
    # Yes!  For x >= 0: y = floor(x) + 1.
    #
    # Now negative x:
    # -0.001->-2, -0.01->-2, -0.1->-2, -0.25->-2, -0.5->-2, -0.75->-2,
    # -0.9->-2, -0.99->-2, -1.0->-2, -1.01->-3, -1.1->-3, -1.25->-3,
    # -1.49->-3, -1.5->-3, -1.75->-3, -2.0->-3, -2.01->-4, -2.5->-4,
    # -3.2->-5, -3.99->-5, -4.01->-6, -10.5->-12, -50.5->-52,
    # -100->-101, -127.7->-129
    #
    # This looks like: y = floor(x) - 1 for x < 0?  Check:
    # floor(-0.001)-1 = -1-1 = -2 ✓
    # floor(-0.5)-1 = -1-1 = -2 ✓
    # floor(-0.99)-1 = -1-1 = -2 ✓
    # floor(-1.0)-1 = -1-1 = -2 ✓
    # floor(-1.01)-1 = -2-1 = -3 ✓
    # floor(-1.5)-1 = -2-1 = -3 ✓
    # floor(-2.0)-1 = -2-1 = -3 ✓
    # floor(-2.01)-1 = -3-1 = -4 ✓
    # floor(-2.5)-1 = -3-1 = -4 ✓
    # floor(-3.2)-1 = -4-1 = -5 ✓
    # floor(-3.99)-1 = -4-1 = -5 ✓
    # floor(-4.01)-1 = -5-1 = -6 ✓
    # floor(-10.5)-1 = -11-1 = -12 ✓
    # floor(-50.5)-1 = -51-1 = -52 ✓
    # floor(-100)-1 = -100-1 = -101 ✓
    # floor(-127.7)-1 = -128-1 = -129 ✓
    # Yes!  For x < 0: y = floor(x) - 1.
    #
    # What about x = 0.0?  E4 says 0.0 -> -1.
    # x < 0 branch: floor(0.0)-1 = 0-1 = -1 ✓
    # x >= 0 branch: floor(0.0)+1 = 0+1 = 1 ✗
    # So 0.0 uses the x < 0 formula.  Boundary: x <= 0 uses floor(x)-1,
    # x > 0 uses floor(x)+1.
    #
    # Check x=0.001: x>0 branch: floor(0.001)+1 = 0+1 = 1 ✓
    # Check x=-0.001: x<=0 branch: floor(-0.001)-1 = -1-1 = -2 ✓
    # Check x=0.0: x<=0 branch: floor(0.0)-1 = -1 ✓
    #
    # This is clean and matches everything:
    #   if x <= 0: y = floor(x) - 1
    #   if x > 0:  y = floor(x) + 1
    #
    # Equivalent: y = floor(x) + sign(x) where sign(0) is treated as -1,
    # or y = floor(x) + (1 if x > 0 else -1).
    #
    # No noise observed: all outputs are exact integers.
    # No undefined regions observed in [-128, 128].
    # No history/state involved.

    import math

    xs = probe["x"]
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            xf = float(x)
        except Exception:
            ys.append(None)
            continue
        if math.isnan(xf) or math.isinf(xf):
            ys.append(None)
            continue
        if xf <= 0:
            y = math.floor(xf) - 1
        else:
            y = math.floor(xf) + 1
        ys.append(float(y))
    return {"y": ys}
