import math

def predict(probe):
    # f is piecewise: two straight outer lines joined by a smooth transition
    # region on roughly [-2, 2].
    # Left line (x <= -2): slope -6.7601 [E2, E8]
    # Right line (x >= 2): slope -16.8999 [E2, E8]
    # Transition region [-2,2] is NOT a cubic Hermite [E4,E6,E10,E12].
    # The observed curve is very smooth and nearly linear in pieces;
    # it looks like a smooth (tanh-like / sigmoid-blend) interpolation
    # between the two lines. Best simple fit: a smoothstep blend of the
    # two line values, with the blend weight going 0->1 across [-2,2].
    #
    # Let L(x) = left line value, R(x) = right line value.
    # At x=-2: y=15.9142 (on left line), at x=2: y=-22.6804 (on right line).
    # Use w = smoothstep((x+2)/4) and y = (1-w)*L(x) + w*R(x).
    # This matches endpoints and slopes at the ends (smoothstep has zero
    # derivative at ends, but the lines differ in slope, so we instead
    # use a blend that matches slopes: a cubic Hermite in the *difference*
    # won't work either. Empirically the curve is close to a cosine blend.
    #
    # Simpler and accurate: fit the transition as a quadratic-ish curve
    # through the observed points. Use a cubic polynomial fit to the
    # transition data (E4,E6,E10,E12) on [-2,2].

    SL = -6.7601
    SR = -16.8999
    xL, yL = -128.0, 867.6846
    xR, yR = 128.0, -2151.9921

    def left(x):
        return yL + SL * (x - xL)

    def right(x):
        return yR + SR * (x - xR)

    # Transition polynomial fit on [-2,2] from observed data.
    # Use a cubic through endpoints with matching slopes is wrong;
    # instead use a smooth blend: y = left(x) + s(t)*(right(x)-left(x))
    # where t=(x+2)/4, s is a smoothstep-like function.
    # From data, at x=0: y=5.4186. left(0)=867.6846-6.7601*128=2.1918?
    # compute: left(0) = 867.6846 + (-6.7601)*(0-(-128)) = 867.6846-865.2928=2.3918
    # right(0) = -2151.9921 + (-16.8999)*(0-128) = -2151.9921+2163.1872=11.1951
    # Hmm, blend at x=0 gives between 2.39 and 11.20; observed 5.4186.
    # t=0.5, s(0.5) should give 5.4186: 2.3918 + s*(11.1951-2.3918)=5.4186
    # s = (5.4186-2.3918)/8.8033 = 0.3438. So s(0.5)~0.344, not 0.5.
    # Use s(t) = t^2*(3-2t) shifted? s(0.5)=0.5 for smoothstep. Not matching.
    # Try s(t)=t^p. 0.5^p=0.344 -> p=1.54. 
    # Check x=1 (t=0.75): left(1)=2.3918-6.7601=-4.3683
    # right(1)=11.1951-16.8999=-5.7048
    # blend: -4.3683 + 0.75^1.54*(-5.7048+4.3683)= -4.3683+0.638*(-1.3365)=-5.221
    # observed at x=1: -5.3245. Close-ish.
    # Check x=-1 (t=0.25): left(-1)=2.3918+6.7601=9.1519
    # right(-1)=11.1951+16.8999=28.095
    # blend: 9.1519+0.25^1.54*(28.095-9.1519)=9.1519+0.1176*18.943=11.38
    # observed at x=-1: 9.3469. Off.
    #
    # The blend model isn't great. Let's just fit a polynomial to the
    # transition data directly. Data on [-2,2] is smooth and monotone.
    # Fit cubic through (-2,15.9142),(2,-22.6804) with slopes -6.7601,-16.8999
    # was the old Hermite; it's wrong. The real curve is flatter in the
    # middle-left and steeper near x=2. 
    #
    # Look at differences (E12): from -2 to -1: 15.9142->9.3469, drop 6.5673 over 1
    # -1 to 0: 9.3469->5.4186, drop 3.9283
    # 0 to 1: 5.4186->-5.3245, drop 10.7431
    # 1 to 2: -5.3245->-22.6804, drop 17.3559
    # So slope: -6.57, -3.93, -10.74, -17.36. Non-monotone slope -> S-shape.
    # This is consistent with a smoothstep blend but with the lines.
    # Actually slope at -2 should be -6.76 (matches left line). Slope at 2 -16.9.
    # The middle has a flatter part around x=-0.5 then steepens.
    #
    # This looks like a tanh/sigmoid transition. Let's model:
    # y = A + B*x + C*tanh(k*(x-x0)) maybe. 
    # Or: the function is a smooth approximation of a piecewise-linear
    # with a smooth (sigmoid) kink. 
    #
    # Best practical approach: interpolate the observed transition points
    # with a smooth monotone cubic (PCHIP-like) using the dense data we have.
    # We have data at 0.1 spacing on [0,2] and [-2,0]. Build a lookup
    # table and interpolate linearly (dense enough).

    # Transition data table (x, y) from E4,E6,E10,E12, merged.
    table = [
        (-2.0, 15.9142), (-1.9, 15.2382), (-1.8, 14.5622), (-1.7, 13.8862),
        (-1.6, 13.2102), (-1.5, 12.5417), (-1.4, 11.8794), (-1.3, 11.2171),
        (-1.2, 10.5797), (-1.1, 9.9587), (-1.0, 9.3469), (-0.9, 8.7466),
        (-0.8, 8.1725), (-0.7, 7.6317), (-0.6, 7.1978), (-0.5, 6.8447),
        (-0.4, 6.5602), (-0.3, 6.2748), (-0.2, 5.9894), (-0.1, 5.704),
        (0.0, 5.4186), (0.1, 5.1041), (0.2, 4.6858), (0.3, 4.0718),
        (0.4, 3.2125), (0.5, 2.1182), (0.6, 0.8742), (0.7, -0.5835),
        (0.8, -2.1698), (0.9, -3.757), (1.0, -5.3245), (1.1, -6.9174),
        (1.2, -8.5666), (1.3, -10.2661), (1.4, -11.9849), (1.5, -13.7572),
        (1.6, -15.5714), (1.7, -17.3742), (1.8, -19.1557), (1.9, -20.9273),
        (2.0, -22.6804),
    ]

    def interp(x):
        # linear interpolation in table, clamped
        if x <= table[0][0]:
            return table[0][1]
        if x >= table[-1][0]:
            return table[-1][1]
        # binary search
        lo, hi = 0, len(table) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if table[mid][0] <= x:
                lo = mid
            else:
                hi = mid
        x0, y0 = table[lo]
        x1, y1 = table[hi]
        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

    def f(x):
        if x <= -2.0:
            return left(x)
        elif x >= 2.0:
            return right(x)
        else:
            return interp(x)

    return {"y": [f(x) for x in probe["x"]]}
