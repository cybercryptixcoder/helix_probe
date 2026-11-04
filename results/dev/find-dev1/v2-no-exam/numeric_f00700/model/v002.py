def predict(probe):
    # f(x) = floor(x) + 1 for x >= 0 [E1, E2, E3]
    #   x=0→-1? No: E1 x=0→-1, E2 x=0→-1. So floor(0)+1=1 is wrong.
    # Recheck: E1: 0→-1, 1→2, 2→3, 4→5, 8→9, 16→17, 32→33, 64→65, 100→101, 127→128, 128→129
    #   For x>=1: f(x)=x+1. For x=0: f(0)=-1.
    # E2: 0.1→2, 0.25→2, 0.5→2, 0.75→2, 1.0→2, 1.25→3, 1.5→3
    #   So for 0<x<1.25: f=2; 1.25<=x<2: f=3; 2<=x<3: f=4; 3<=x<4: f=5
    #   That's f(x)=floor(x)+2 for x>0? floor(0.1)+2=2 ✓, floor(1.0)+2=3 ✗ (E2 says 2)
    #   Hmm. 1.0→2 but floor(1)+2=3. So threshold is at 1.25, not 1.
    #   Check: 0.75→2, 1.0→2, 1.25→3. Threshold between 1.0 and 1.25.
    #   E3: 1.0→2, 1.25→3, 1.5→3, 2.0→3, 3.0→4, 4.0→5
    #   So 2.0→3, 3.0→4, 4.0→5: f(x)=x+1 for integer x>=2.
    #   But 1.0→2 = 1+1 ✓, 1.25→3, 1.5→3, 2.0→3.
    #   So for x in [1,2): f=2 except x>=1.25 gives 3? 1.25→3, 1.5→3, but 2.0→3.
    #   Wait 1.0→2, 1.25→3, 1.5→3, 2.0→3, 3.0→4.
    #   Looks like f(x)=round(x)+1? round(1.0)+1=2 ✓, round(1.25)+1=2 ✗ (need 3)
    #   Try f(x)=ceil(x)+1 for x>0: ceil(0.1)+1=2 ✓, ceil(0.75)+1=2 ✓, ceil(1.0)+1=2 ✓,
    #     ceil(1.25)+1=3 ✓, ceil(1.5)+1=3 ✓, ceil(2.0)+1=3 ✓, ceil(3.0)+1=4 ✓, ceil(4.0)+1=5 ✓
    #   Check E1: ceil(1)+1=2 ✓, ceil(2)+1=3 ✓, ceil(4)+1=5 ✓, ceil(8)+1=9 ✓, ceil(16)+1=17 ✓,
    #     ceil(32)+1=33 ✓, ceil(64)+1=65 ✓, ceil(100)+1=101 ✓, ceil(127)+1=128 ✓, ceil(128)+1=129 ✓
    #   So for x>0: f(x)=ceil(x)+1.
    # For x<0: E1: -128→-129, -100→-101, -64→-65, -32→-33, -16→-17, -8→-9, -4→-5, -2→-3, -1→-2
    #   That's f(x)=x-1 for integer x<0.
    # E2: -1.5→-2, -1.25→-2, -1.0→-2, -0.75→-1, -0.5→-1, -0.25→-1, -0.1→-1
    #   floor(-1.5)-1=-3 ✗. ceil(-1.5)-1=-2 ✓, ceil(-1.25)-1=-2 ✓, ceil(-1.0)-1=-2 ✓,
    #   ceil(-0.75)-1=-1 ✓, ceil(-0.5)-1=-1 ✓, ceil(-0.25)-1=-1 ✓, ceil(-0.1)-1=-1 ✓
    #   So for x<0: f(x)=ceil(x)-1.
    # x=0: E1 and E2 both give -1. ceil(0)-1=-1 ✓ (using x<0 branch would fail; x>=0 branch ceil(0)+1=1 ✗)
    #   So x=0 uses the x<0 formula: f(0)=-1.
    # Summary: f(x)=ceil(x)+1 if x>0, else ceil(x)-1.
    import math
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(math.ceil(x) + 1)
        else:
            out.append(math.ceil(x) - 1)
    return {"y": out}
