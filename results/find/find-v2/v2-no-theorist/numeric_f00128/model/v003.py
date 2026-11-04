import math

def predict(probe):
    # Piecewise linear with a smooth transition near x=0 [E1, E2, E3, E4].
    # Left branch (x <= -2): y = -6.76*x + 2.4  [E1, E2]
    # Right branch (x >= 4): y = -16.90*x + 11.2  [E1, E2, E3]
    # Transition region roughly [-2, 4]: smooth S-curve between branches [E4].
    # At x=0, y=5.4186 [E2, E4].
    # E4 shows: -2->15.9142, -1.5->12.5417, -1->9.3469, -0.5->6.8447,
    #   -0.25->6.1321, 0->5.4186, 0.25->4.4171, 0.5->2.1182,
    #   1->-5.3245, 1.5->-13.7572, 2->-22.6804, 3->-39.4742, 4->-56.3287
    # Left line at -2: 15.92 (matches). Right line at 4: -56.4 (matches).
    # Transition is smooth, roughly sigmoid-shaped in slope.
    # Model: y = -11.83*x + 6.8 - 5.07*S(x) where S goes from -1 to +1.
    # Actually fit: use a smooth blend between left and right lines.
    # Let L(x) = -6.76*x + 2.4, R(x) = -16.90*x + 11.2.
    # y = L + (R-L)*w(x), w in [0,1], w=0 for x<=-2, w=1 for x>=4.
    # At x=0: L=2.4, R=11.2, obs 5.4186 => w = (5.4186-2.4)/(11.2-2.4)=3.0186/8.8=0.343
    # At x=-1: L=9.16, R=28.1, obs 9.3469 => w=(9.3469-9.16)/18.94=0.00987
    # At x=-0.5: L=5.78, R=19.65, obs 6.8447 => w=(6.8447-5.78)/13.87=0.0768
    # At x=0.5: L=-0.98, R=2.75, obs 2.1182 => w=(2.1182+0.98)/3.73=0.8306
    # At x=1: L=-4.36, R=-5.7, obs -5.3245 => w=(-5.3245+4.36)/(-1.34)=0.720
    # At x=1.5: L=-7.74, R=-14.15, obs -13.7572 => w=(-13.7572+7.74)/(-6.41)=0.9387
    # At x=2: L=-11.12, R=-22.6, obs -22.6804 => w=(-22.6804+11.12)/(-11.48)=1.007
    # So w rises from ~0 at -1 to ~1 at 2. Midpoint ~0.5 around x=0.1.
    # Fit logistic: w(x) = 1/(1+exp(-(x-x0)/s)). 
    # w(0)=0.343 => logit = ln(0.343/0.657) = -0.650
    # w(0.5)=0.831 => logit = ln(0.831/0.169)=1.593
    # slope = (1.593+0.650)/0.5 = 4.486 => s=0.2229
    # x0: -0.650 = (0-x0)/s => x0 = 0.650*0.2229 = 0.1449
    # Check w(1): logit=(1-0.1449)/0.2229=3.836 => w=0.979 (obs 0.720) - off
    # Hmm not logistic. The transition is sharper between 0 and 1.
    # Let's just interpolate the observed transition points directly with a smooth curve.
    # Use piecewise: for x in [-2,4], interpolate through E4 points via monotone cubic-ish.
    # Simpler: use a tanh blend with tuned params.
    # Try y = -11.83*x + 6.8 + A*tanh((x-x0)/s)
    # At x->+inf slope: -11.83 + A/s = -16.90 => A/s = -5.07
    # At x->-inf slope: -11.83 - A/s = -6.76 => A/s = -5.07 ✓
    # So A = -5.07*s.
    # At x=0: 6.8 + A*tanh(-x0/s) = 5.4186 => A*tanh(-x0/s) = -1.3814
    # At x=1: -11.83+6.8 + A*tanh((1-x0)/s) = -5.3245 => A*tanh((1-x0)/s) = -0.2945
    # At x=-1: 11.83+6.8 + A*tanh((-1-x0)/s) = 9.3469 => A*tanh((-1-x0)/s) = -9.2831
    # At x=2: -23.66+6.8 + A*tanh((2-x0)/s) = -22.6804 => A*tanh((2-x0)/s) = -5.8204
    # From x=0: A*tanh(-x0/s) = -1.3814
    # From x=2: A*tanh((2-x0)/s) = -5.8204
    # Ratio: tanh((2-x0)/s)/tanh(-x0/s) = 4.213
    # Try s=0.5, x0=0.5: tanh(3)=0.995, tanh(-1)=-0.762 => ratio -1.31 no
    # Try s=1, x0=0.5: tanh(1.5)=0.905, tanh(-0.5)=-0.462 => ratio -1.96
    # Try s=1.5, x0=0.5: tanh(1)=0.762, tanh(-0.333)=-0.321 => ratio -2.37
    # Try s=2, x0=0.5: tanh(0.75)=0.635, tanh(-0.25)=-0.245 => ratio -2.59
    # Try s=3, x0=0.5: tanh(0.5)=0.462, tanh(-0.167)=-0.165 => ratio -2.80
    # Need ratio 4.213 (positive). Hmm sign issue: tanh(-x0/s) negative, tanh((2-x0)/s) positive if 2>x0.
    # So ratio is negative. But we need positive 4.213. Contradiction => tanh model wrong sign.
    # Actually A negative, both tanh values... let's redo.
    # A*tanh(-x0/s) = -1.3814, A negative => tanh(-x0/s) positive => x0 negative.
    # A*tanh((2-x0)/s) = -5.8204, A negative => tanh((2-x0)/s) positive.
    # If x0 negative, -x0/s positive, tanh positive ✓. (2-x0)/s more positive, tanh closer to 1.
    # Ratio tanh((2-x0)/s)/tanh(-x0/s) = 5.8204/1.3814 = 4.213
    # Try s=1, x0=-0.5: tanh(2.5)=0.987, tanh(0.5)=0.462 => ratio 2.14
    # Try s=0.5, x0=-0.5: tanh(5)=0.9999, tanh(1)=0.762 => ratio 1.31
    # Try s=2, x0=-0.5: tanh(1.25)=0.848, tanh(0.25)=0.245 => ratio 3.46
    # Try s=3, x0=-0.5: tanh(0.833)=0.682, tanh(0.167)=0.165 => ratio 4.13 close!
    # s=3, x0=-0.5: A = -5.07*3 = -15.21
    # Check x=0: -15.21*tanh(0.5/3)= -15.21*0.165=-2.51, need -1.3814. Off.
    # Hmm. Let's just use direct interpolation of E4 points plus lines outside.
    # This is an MLP approximating something; the transition is smooth but not simple tanh.
    # Best practical: piecewise linear interpolation through E4 points in [-2,4],
    # and the linear branches outside.
    # E4 points: (-2,15.9142),(-1.5,12.5417),(-1,9.3469),(-0.5,6.8447),
    #   (-0.25,6.1321),(0,5.4186),(0.25,4.4171),(0.5,2.1182),
    #   (1,-5.3245),(1.5,-13.7572),(2,-22.6804),(3,-39.4742),(4,-56.3287)
    # Check left line at -2: 15.92 ✓, at -1.5: 12.54 ✓, at -1: 9.16 vs 9.3469 (close)
    # Right line at 4: -56.4 vs -56.3287 ✓, at 3: -39.5 vs -39.4742 ✓, at 2: -22.6 vs -22.6804 ✓
    # So transition is roughly [-1, 2], with smooth blend.
    # Use linear interpolation through these anchor points for x in [-2,4].
    # This will predict well for any x in that region.
    xs = probe.get("x", [])
    out = []
    anchors = [(-2.0,15.9142),(-1.5,12.5417),(-1.0,9.3469),(-0.5,6.8447),
               (-0.25,6.1321),(0.0,5.4186),(0.25,4.4171),(0.5,2.1182),
               (1.0,-5.3245),(1.5,-13.7572),(2.0,-22.6804),(3.0,-39.4742),(4.0,-56.3287)]
    for x in xs:
        try:
            if x <= -2.0:
                y = -6.76*x + 2.4
            elif x >= 4.0:
                y = -16.90*x + 11.2
            else:
                # linear interp through anchors
                for i in range(len(anchors)-1):
                    x0,y0 = anchors[i]
                    x1,y1 = anchors[i+1]
                    if x0 <= x <= x1:
                        t = (x-x0)/(x1-x0)
                        y = y0 + t*(y1-y0)
                        break
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
