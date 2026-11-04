def predict(probe):
    # y = -6.9 for large positive x, -7.9 for negative x [E1]
    # Step is at x=0: f(0)=-7.8991, f(-0.5)=-7.8999, f(0.5)=-7.8906 [E2]
    # Smooth transition from -7.9 to -6.9 over roughly x in [0, 4] [E2]
    # Looks like a sigmoid/logistic: -7.9 + 1.0 * sigmoid-ish centered ~1.5 [E2]
    # Check: x=1.0 -> -7.8111, x=1.5 -> -7.4, x=2.0 -> -6.9889, x=2.5 -> -6.9094
    # This matches -7.9 + 1.0/(1+exp(-k*(x-x0))) with x0~1.5, k~2.5?
    # At x=1.5: -7.9+0.5 = -7.4 ✓ exactly
    # At x=1.0: -7.9 + 1/(1+e^1.25) = -7.9+0.2227 = -7.677, but observed -7.8111
    # Try logistic: 1/(1+e^{-k(x-x0)}). x0=1.5, want f(1.0)=0.0889 -> 1/(1+e^{0.5k})=0.0889
    #   e^{0.5k}=10.25 -> k=4.65. Check x=2.0: 1/(1+e^{-2.325})=0.9109 -> -6.989 ✓ (obs -6.9889)
    # Check x=0.5: 1/(1+e^{4.65})=0.00949 -> -7.8905 ✓ (obs -7.8906)
    # Check x=0: 1/(1+e^{6.975})=0.00094 -> -7.8991 ✓ (obs -7.8991)
    # Check x=-0.5: ~0 -> -7.9 ✓ (obs -7.8999)
    # Check x=2.5: 1/(1+e^{-4.65})=0.9905 -> -6.9095 ✓ (obs -6.9094)
    # Check x=3.0: 1/(1+e^{-6.975})=0.99906 -> -6.9009 ✓ (obs -6.9009)
    # Check x=3.5: 1/(1+e^{-9.3})=0.99991 -> -6.9001 ✓ (obs -6.9001)
    # Check x=2.9: 1/(1+e^{-6.51})=0.99852 -> -6.9015 ✓ (obs -6.9015)
    # Logistic with x0=1.5, k=4.65 fits everything!
    import math
    out = []
    for x in probe["x"]:
        out.append(-7.9 + 1.0/(1.0+math.exp(-4.65*(x-1.5))))
    return {"y": out}
