def predict(probe):
    # Two plateaus: -7.9 for x<0, -6.9 for x>~3 [E1]
    # Transition is a smooth sigmoid centered near x=1.5, not x=0 [E2]
    # At x=0 value is -7.8991 (barely above -7.9), at x=1.5 it's -7.4 (midpoint),
    # at x=2 it's -6.9889, at x=3 it's -6.9009, at x=4 it's -6.9 [E2]
    # Midpoint -7.4 at x=1.5 -> center c=1.5, amplitude 1.0
    # Fit slope: at x=1.0, y=-7.8111 -> s=0.0889; at x=2.0, y=-6.9889 -> s=0.9111
    # sigmoid((1.0-1.5)*k)=0.0889 -> -0.5k=-2.32 -> k~4.64
    # sigmoid((2.0-1.5)*k)=0.9111 -> 0.5k=2.32 -> k~4.64
    # Check x=0.5: sigmoid(-1*4.64)=0.0096 -> -7.8904 (obs -7.8906) ok
    # Check x=0.2: sigmoid(-1.3*4.64)=0.0024 -> -7.8976 (obs -7.8976) ok
    # Check x=0.1: sigmoid(-1.4*4.64)=0.0015 -> -7.8985 (obs -7.8985) ok
    # Check x=0.0: sigmoid(-1.5*4.64)=0.00095 -> -7.89905 (obs -7.8991) ok
    # Check x=-0.1: sigmoid(-1.6*4.64)=0.00059 -> -7.8994 (obs -7.8994) ok
    # Check x=-0.2: sigmoid(-1.7*4.64)=0.00037 -> -7.8996 (obs -7.8996) ok
    # Check x=-0.5: sigmoid(-2*4.64)=0.000093 -> -7.8999 (obs -7.8999) ok
    # Check x=-1.0: sigmoid(-2.5*4.64)=0.0000092 -> -7.9 (obs -7.9) ok
    import math
    out = []
    for x in probe["x"]:
        z = (x - 1.5) * 4.64
        if z > 700:
            s = 1.0
        elif z < -700:
            s = 0.0
        else:
            s = 1.0/(1.0+math.exp(-z))
        out.append(-7.9 + 1.0*s)
    return {"y": out}
