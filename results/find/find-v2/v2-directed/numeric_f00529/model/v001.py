def predict(probe):
    # Function is constant -7.9 for x <= -2 [E1]
    # Function is constant -6.9 for x >= 5 [E1]
    # Between -2 and 5 there is a transition: values at -1,0,1,2 are -7.9, -7.8991, -7.8111, -6.9889 [E1]
    # Looks like a smooth sigmoid-like transition from -7.9 to -6.9 centered around x=1 [E1, ?]
    # Model: -7.9 for x<=-2, -6.9 for x>=5, linear-ish interpolation between using observed points
    # The observed transition points: (-1,-7.9),(0,-7.8991),(1,-7.8111),(2,-6.9889),(5,-6.9)
    # Fit a smooth curve. Try logistic: y = -6.9 - 1.0/(1+exp(k*(x-c)))
    # At x=1: -7.8111 => 1/(1+exp(k*(1-c))) = 0.9111 => exp(k*(1-c))=0.0976 => k*(1-c)=-2.327
    # At x=2: -6.9889 => 1/(1+exp(k*(2-c))) = 0.0889 => exp(k*(2-c))=10.25 => k*(2-c)=2.327
    # Adding: k = 4.654, then 1-c = -0.5 => c=1.5
    # Check x=0: 1/(1+exp(4.654*(-1.5)))=1/(1+exp(-6.98))=1/(1.00093)=0.99907 => y=-7.8991 ✓
    # Check x=-1: 1/(1+exp(4.654*(-2.5)))=1/(1+e^-11.6)≈1 => y=-7.9 ✓
    # Check x=5: 1/(1+exp(4.654*3.5))=1/(1+e^16.3)≈0 => y=-6.9 ✓
    import math
    out = []
    for x in probe["x"]:
        if x <= -2:
            y = -7.9
        elif x >= 5:
            y = -6.9
        else:
            y = -6.9 - 1.0/(1.0+math.exp(4.654*(x-1.5)))
        out.append(y)
    return {"y": out}
