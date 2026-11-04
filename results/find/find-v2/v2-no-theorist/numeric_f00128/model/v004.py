import math

def predict(probe):
    # Left branch (x <= -2): y = -6.76*x + 2.4  [E1, E2, E8]
    # Right branch (x >= 4): y = -16.90*x + 11.2  [E1, E2, E3, E8]
    # Transition region roughly [-2, 4]: smooth S-curve between branches [E4, E6, E10]
    # E10 shows the transition is a smooth curve, not piecewise linear.
    # The slope in the transition is roughly constant ~ -15 to -17 per unit x,
    # suggesting the transition is a smooth blend (sigmoid-like) between branches.
    # Fit a tanh blend: y = a*x + b + c*tanh((x-x0)/s)
    # Left slope: a - c/s = -6.76 ; Right slope: a + c/s = -16.90
    # => a = -11.83, c/s = -5.07
    # Use E4 anchors to fit x0, s, and offset.
    # At x=0: y=5.4186 ; at x=2: y=-22.6804 ; at x=-1: y=9.3469
    # Try s=0.9, x0=0.35: 
    #   tanh((0-0.35)/0.9)=tanh(-0.389)=-0.370
    #   tanh((2-0.35)/0.9)=tanh(1.833)=0.950
    #   tanh((-1-0.35)/0.9)=tanh(-1.5)=-0.905
    # c = -5.07*s = -4.563
    # b from x=0: 5.4186 = -11.83*0 + b + c*(-0.370) => b = 5.4186 + 4.563*0.370 = 7.107
    # Check x=2: -11.83*2 + 7.107 + (-4.563)*0.950 = -23.66+7.107-4.335 = -20.888 (obs -22.68) off
    # Try s=0.7, x0=0.3:
    #   tanh(-0.3/0.7)=tanh(-0.4286)=-0.404
    #   tanh(1.7/0.7)=tanh(2.429)=0.985
    #   tanh(-1.3/0.7)=tanh(-1.857)=-0.953
    #   c = -3.549
    #   b = 5.4186 + 3.549*0.404 = 6.852
    #   x=2: -23.66+6.852-3.549*0.985 = -20.303 (obs -22.68) still off
    # The transition seems sharper than tanh. Let's use a steeper sigmoid.
    # Actually, let's fit a logistic blend w(x) between L and R.
    # w = (y - L)/(R - L). From E4:
    #   x=-1: L=9.16, R=28.1, y=9.3469 => w=0.00987
    #   x=0: L=2.4, R=11.2, y=5.4186 => w=0.343
    #   x=0.5: L=-0.98, R=2.75, y=2.1182 => w=0.8306
    #   x=1: L=-4.36, R=-5.7, y=-5.3245 => w=0.720 (noisy?)
    #   x=1.5: L=-7.74, R=-14.15, y=-13.7572 => w=0.9387
    #   x=2: L=-11.12, R=-22.6, y=-22.6804 => w=1.007
    # Logistic fit: logit(w) = (x-x0)/s
    #   x=0: logit(0.343)=-0.650
    #   x=0.5: logit(0.831)=1.593
    #   x=1.5: logit(0.939)=2.735
    #   x=2: logit(0.999)=6.9 (saturated)
    # From x=0 and x=0.5: slope=(1.593+0.650)/0.5=4.486, s=0.223, x0=0.145
    # Check x=1.5: (1.5-0.145)/0.223=6.08 => w=0.998 (obs 0.939) - too sharp
    # The transition is asymmetric. Let's just use a smooth interpolation.
    # Use cubic Hermite / monotone interpolation through E4+E6+E10 anchors.
    # Collect all transition-region observations (x in [-2,4]):
    anchors = [
        (-2.0,15.9142),(-1.9,15.2382),(-1.75,14.2242),(-1.5,12.5417),
        (-1.25,10.8971),(-1.0,9.3469),(-0.75,7.8986),(-0.6,7.1978),
        (-0.5,6.8447),(-0.4,6.5602),(-0.25,6.1321),(-0.1,5.704),
        (0.0,5.4186),(0.1,5.1041),(0.2,4.6858),(0.25,4.4171),
        (0.3,4.0718),(0.35,3.6502),(0.4,3.2125),(0.45,2.6897),
        (0.5,2.1182),(0.55,1.5026),(0.6,0.8742),(0.65,0.1665),
        (0.7,-0.5835),(0.75,-1.3675),(0.8,-2.1698),(0.85,-2.9733),
        (0.9,-3.757),(0.95,-4.5408),(1.0,-5.3245),(1.05,-6.1083),
        (1.1,-6.9174),(1.15,-7.7325),(1.2,-8.5666),(1.25,-9.4067),
        (1.3,-10.2661),(1.35,-11.1255),(1.4,-11.9849),(1.45,-12.8618),
        (1.5,-13.7572),(1.75,-18.2649),(2.0,-22.6804),(2.5,-31.1292),
        (3.0,-39.4742),(3.5,-47.9015),(3.9,-54.6433),(4.0,-56.3287),
    ]
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            if x <= -2.0:
                y = -6.76*x + 2.4
            elif x >= 4.0:
                y = -16.90*x + 11.2
            else:
                # linear interp through anchors
                y = None
                for i in range(len(anchors)-1):
                    x0,y0 = anchors[i]
                    x1,y1 = anchors[i+1]
                    if x0 <= x <= x1:
                        t = (x-x0)/(x1-x0)
                        y = y0 + t*(y1-y0)
                        break
                if y is None:
                    y = -16.90*x + 11.2
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
