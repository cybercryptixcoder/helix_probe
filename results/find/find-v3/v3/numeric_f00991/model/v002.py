def predict(probe):
    # f(x) = 4.1*x + 12.3*|x| - 2.5*sign(x), sign(0)=0 [E1,E2,E3,E4,E5]
    # BUT at x=0 the value is 2.5, not 0 [E6: f(0)=2.5]
    # Tiny values: f(1e-6) = -2.5, f(-1e-6) = 2.5 [E6]
    #   -> sign(0)=0 gives 0, but observed 2.5 at x=0 and -2.5 at +1e-6.
    #   This matches sign(x) with sign(0)=+1? No: at x=0 -> -2.5*1 = -2.5, not 2.5.
    #   Actually: f(0)=2.5 = -2.5*(-1) => sign(0) treated as -1.
    #   And f(+1e-6) = -2.5 => sign(+tiny) = +1 (normal). f(-1e-6)=2.5 => sign=-1 (normal).
    #   So only x==0 uses sign=-1 (i.e., the "x<0 branch" formula -8.2x+2.5 at x=0 gives 2.5).
    #   => x<=0 uses -8.2x+2.5, x>0 uses 16.4x-2.5. Check: x=0 -> 2.5 ✓
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(16.4 * x - 2.5)
        else:
            out.append(-8.2 * x + 2.5)
    return {"y": out}
