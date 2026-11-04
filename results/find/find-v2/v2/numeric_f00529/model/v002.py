def predict(probe):
    # Output is ~ -6.9 for x>0 and ~ -7.9 for x<0 [E1, E2]
    # x=0 and x=-0 give -7.8991 (negative side) [E2]
    # Near-zero positive x: values approach -7.9 as x->0+ [E2: 0.5->-7.8906, 1.0->-7.8111, 2.0->-6.9889, 2.5->-6.9094, 3.0->-6.9009, 3.5->-6.9001]
    #   This looks like -7.9 + something decaying, or a smooth transition.
    # Negative side is flat -7.9 for x<=-1, but -0.5 gives -7.8999 (tiny offset) [E2]
    # Hypothesis: y = -7.9 + 1.0 * sigmoid-like(x) for x>0, approaching -6.9.
    #   Fit: at x=3.5 -> -6.9001 (offset 0.9999); x=3.0 -> -6.9009 (0.9991);
    #        x=2.5 -> -6.9094 (0.9906); x=2.0 -> -6.9889 (0.9111);
    #        x=1.0 -> -7.8111 (0.0889); x=0.5 -> -7.8906 (0.0094)
    #   Looks like offset ~ 1/(1+exp(-k(x-x0)))? Try: offset(1.0)=0.0889, offset(2.0)=0.9111.
    #   Symmetric around x0=1.5: offset(1.5)=0.5. Check logistic: 1/(1+e^{-k(x-1.5)}).
    #   At x=1: 1/(1+e^{0.5k})=0.0889 -> e^{0.5k}=10.25 -> k=4.65
    #   At x=2: 1/(1+e^{-0.5k})=0.9111 -> e^{-0.5k}=0.0976 -> k=4.65. Consistent!
    #   Check x=2.5: 1/(1+e^{-4.65})=0.9906 ✓. x=3: 1/(1+e^{-6.975})=0.99906 ✓
    #   x=0.5: 1/(1+e^{4.65})=0.00941 ✓. x=3.5: 1/(1+e^{-9.3})=0.99991 ✓
    # So for x>0: y = -7.9 + 1/(1+exp(-4.65*(x-1.5)))
    # For x<0: y = -7.9 (flat), except tiny offset near 0-: -0.5 -> -7.8999
    #   offset(0.5 neg) = 0.0001. Maybe symmetric logistic on negative side with tiny amplitude?
    #   Or: y = -7.9 + 1/(1+exp(-4.65*(x-1.5))) works for x=-0.5? 
    #   1/(1+e^{4.65*2})=1/(1+e^{9.3})=0.000091 -> -7.89991 ≈ -7.8999 ✓!
    #   x=-1: 1/(1+e^{4.65*2.5})=1/(1+e^{11.6})=9e-6 -> -7.9 ✓ (rounds to -7.9)
    # So single formula: y = -7.9 + 1/(1+exp(-4.65*(x-1.5))) for ALL x!
    # Check x=10.5: 1/(1+e^{-4.65*9})=1 -> -6.9 ✓
    # Check x=-10.5: ~0 -> -7.9 ✓
    # Check x=0: 1/(1+e^{4.65*1.5})=1/(1+e^{6.975})=0.00093 -> -7.89907 ≈ -7.8991 ✓
    # Check x=2.9: 1/(1+e^{-4.65*1.4})=1/(1+e^{-6.51})=0.99852 -> -6.90148 ≈ -6.9015 ✓
    # Check x=88.2: -6.9 ✓, x=-6: -7.9 ✓
    import math
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
        else:
            try:
                y = -7.9 + 1.0/(1.0 + math.exp(-4.65*(x - 1.5)))
            except OverflowError:
                y = -6.9 if x > 1.5 else -7.9
            out.append(round(y, 4))
    return {"y": out}
