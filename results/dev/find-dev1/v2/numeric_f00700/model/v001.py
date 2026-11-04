def predict(probe):
    # f(x) = x + 1 for x >= 0 [E1: 0->-1? no...]
    # Re-examine E1: x=-128->-129, -96->-97 ... -1->-2, -0.5->-1, 0->-1, 0.5->2, 1->2, 2->3, 4->5, 8->9, 16->17, 32->33, 64->65, 128->129
    # For x>0: y = x+1 (0.5->2? no, 0.5->2 is x+1.5... wait 0.5+1=1.5 not 2)
    # Let's check: 0.5->2, 1->2, 2->3, 4->5, 8->9: y = x+1 for x>=1. But 0.5->2 = 0.5+1.5.
    # Actually 0.5->2 and 1->2: looks like ceil(x)+1? ceil(0.5)=1, +1=2. ceil(1)=1,+1=2. ceil(2)=2,+1=3. ceil(4)=4,+1=5. Yes!
    # For x<0: -1->-2, -0.5->-1, -2->-3, -4->-5, -8->-9: y = x-1 for x<=-1. -0.5->-1 = floor(-0.5)-1 = -1-1=-2? no, -0.5->-1.
    # floor(-0.5)=-1, -1? -0.5->-1 means floor(-0.5)=-1. So y=floor(x) for -1<x<0? -0.5->-1 yes.
    # -1->-2: floor(-1)-1=-2. -2->-3: floor(-2)-1=-3. So y=floor(x)-1 for x<=-1, and y=floor(x) for -1<x<0.
    # 0->-1: floor(0)-1=-1. So x=0 behaves like x<=-1 branch? Or floor(0)-1=-1.
    # Hmm, simpler: for x<0: y = floor(x) if x>-1 else floor(x)-1. At x=0: -1.
    # Alternative: y = floor(x) + (1 if x>0 else -1)? x=0: floor(0)-1=-1 ✓. x=0.5: floor(0.5)+1=0+1=1, but observed 2. ✗
    # Try: y = ceil(x)+1 for x>0, y=floor(x)-1 for x<=0? x=0: -1 ✓. x=-0.5: floor(-0.5)-1=-2, observed -1 ✗.
    # Try: y = floor(x)+1 for x>0: 0.5->1, observed 2 ✗.
    # Try: y = round(x)+1 for x>0? 0.5->round=0 or 1... 0.5->2 means round(0.5)=1, +1=2. 1->2 ✓. 2->3 ✓. 4->5 ✓.
    # For x<0: -0.5->-1: round(-0.5)=-1 (banker's? round(-0.5)=0 in Python). Hmm.
    # Let's just use: x>0: ceil(x)+1; x<=0: floor(x)-1? Check -0.5: floor(-0.5)-1=-2 ✗.
    # x<=0: -0.5->-1, -1->-2, -2->-3, 0->-1. So for x in (-1,0]: y=-1. For x<=-1: y=x-1.
    # x>0: 0.5->2, 1->2, 2->3, 4->5. So for x in (0,1]: y=2. For x>=1: y=x+1.
    # Check: x=1 -> 2 = 1+1 ✓. x=0.5 -> 2 (in (0,1]) ✓. x=2->3=2+1 ✓.
    # x=-1 -> -2 = -1-1 ✓. x=-0.5 -> -1 (in (-1,0]) ✓. x=0 -> -1 (in (-1,0]) ✓.
    # So: x>1: x+1; 0<x<=1: 2; -1<x<=0: -1; x<=-1: x-1.
    # Equivalently: y = x+1 if x>1; y=2 if 0<x<=1; y=-1 if -1<x<=0; y=x-1 if x<=-1.
    # This is like x + sign-ish with clamping near 0. Actually: y = x + 1 for x>0 except clamp at 2 near 0; y=x-1 for x<0 except clamp at -1 near 0.
    # Simpler unified: y = x + 1 if x>0 else x-1, but with floor/ceil adjustments near zero.
    # Let's just implement piecewise.
    out = []
    for x in probe["x"]:
        if x > 1:
            y = x + 1
        elif x > 0:
            y = 2
        elif x > -1:
            y = -1
        else:
            y = x - 1
        out.append(y)
    return {"y": out}
