def predict(probe):
    # f(x) = x + 1 for x >= 0, and x - 1 for x < 0 [E1]
    # Evidence: f(0)= -1, f(0.5)=2, f(1)=2, f(2)=3, f(4)=5, f(8)=9, f(16)=17, f(32)=33, f(64)=65, f(128)=129
    #   => for x>=0: f(x)=x+1
    # Evidence: f(-0.5)=-1, f(-1)=-2, f(-2)=-3, f(-4)=-5, f(-8)=-9, f(-16)=-17, f(-32)=-33, f(-64)=-65, f(-100)=-101, f(-128)=-129
    #   => for x<0: f(x)=x-1
    # Note: f(0)=-1 fits the x<0 branch (0-1=-1), so the boundary is x<=0 vs x>0.
    # Check: f(0.5)=2 = 0.5+1? No, 1.5. But observed 2. Hmm.
    # Re-examine: f(0)=-1, f(0.5)=2, f(1)=2. So f(0.5)=2 and f(1)=2.
    # For x>0: f(0.5)=2, f(1)=2, f(2)=3, f(4)=5, f(8)=9 => f(x)=x+1 for x>=1, but f(0.5)=2 = 0.5+1.5?
    # Actually f(0.5)=2 could be round(x)+1 = 1+1=2. f(1)=2=1+1. f(2)=3. So f(x)=floor(x)+1 for x>0?
    # f(0.5): floor(0.5)+1=1. No, that's 1, not 2.
    # Try ceil(x)+1 for x>0: ceil(0.5)+1=2 ✓, ceil(1)+1=2 ✓, ceil(2)+1=3 ✓, ceil(4)+1=5 ✓. 
    # For x<0: f(-0.5)=-1, f(-1)=-2, f(-2)=-3. floor(x)-1? floor(-0.5)-1=-2 ✗. 
    # ceil(x)-1: ceil(-0.5)-1=0-1=-1 ✓, ceil(-1)-1=-2 ✓, ceil(-2)-1=-3 ✓, ceil(-4)-1=-5 ✓, ceil(-128)-1=-129 ✓.
    # f(0)=-1: ceil(0)-1=-1 ✓.
    # So f(x) = ceil(x)+1 for x>0, ceil(x)-1 for x<=0? Check f(0.5)=2=ceil(0.5)+1=2 ✓.
    # But simpler: f(x) = ceil(x) + sign-ish. For x>0: +1, x<=0: -1.
    # Actually f(x)=ceil(x)+1 for x>0 and ceil(x)-1 for x<=0. Check f(1)=2 ✓, f(0.5)=2 ✓.
    # Alternative: f(x)=ceil(x)+1 if x>0 else ceil(x)-1.
    import math
    out = []
    for x in probe["x"]:
        c = math.ceil(x)
        if x > 0:
            out.append(float(c + 1))
        else:
            out.append(float(c - 1))
    return {"y": out}
