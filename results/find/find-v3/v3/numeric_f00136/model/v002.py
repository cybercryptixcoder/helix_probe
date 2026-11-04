import math

def predict(probe):
    # Beliefs:
    # Far field is a smooth, nearly-linear ramp in x: y ~ 0.03 + 0.0001*x
    #   [E10: -128->0.048, -120->0.046, -100->0.039, -80->0.034, -60->0.028,
    #    -40->0.022, -30->0.019, -25->0.018, -15->0.015, 12->-0.021,
    #    15->-0.015, 25->0.001, 40->0.009, 60->0.020, 80->0.031,
    #    100->0.042, 120->0.052, 128->0.057]
    #   Slope ~ (0.057-0.048)/256 ~ 0.00004; intercept ~0.043 at x=0.
    #   Actually fit: y ~ 0.043 + 0.00005*x roughly. Check E1: x=-20.3 -> 0.0163
    #   (0.043-0.001=0.042, too high). Let's fit better.
    # Origin structure: positive lobe peaking ~0.078 at x=-2, crossing 0 near x=0,
    #   negative trough ~-0.095 at x=1, decaying back toward baseline by x~12.
    #   [E2, E8]
    # The far-field ramp and the origin structure appear to be one smooth
    #   function: the "baseline" at x=0 is ~0 (not 0.03). The ramp passes
    #   through ~0 near x=0. So the origin structure sits on a ramp that
    #   crosses zero at x~0.
    # Model: y = ramp(x) + origin_bump(x)
    #   ramp(x) = a + b*x, fit to far-field points.
    #   origin_bump = positive Gaussian at -2 minus negative Gaussian at 1.
    xs = probe.get("x", [])
    out = []
    for x in xs:
        # Far-field linear ramp. Fit from E10 far points.
        # Using points: (-128,0.0479),(-100,0.0394),(-60,0.0277),(-25,0.0177),
        #   (25,0.0009),(60,0.0198),(100,0.0415),(128,0.0565)
        # Slope ~ (0.0565-0.0479)/256 = 0.0000336; but midpoints suggest
        #   more curvature. Try: y_ramp = 0.0001*x + 0.030? Check x=-128: 0.0172 no.
        # Let's just fit linear: slope=(0.0565-0.0479)/256=3.36e-5, intercept
        #   from x=0: average of extrapolations. At x=25 ->0.0009 => a=-0.0009+... 
        # Use two-point: (25,0.0009) and (100,0.0415): slope=0.000541, no.
        # The far field is NOT linear. It looks like a smooth S / sigmoid-ish.
        # Values: -128:0.048, -100:0.039, -60:0.028, -25:0.018, 25:0.001,
        #   60:0.020, 100:0.042, 128:0.057
        # This is roughly antisymmetric-ish around x~0 but with offset.
        # Try: y_ramp = 0.0004*x + 0.001? x=-128 -> -0.050 no.
        # Hmm. Let's model far field as: 0.03 + 0.0002*x won't fit either.
        # Actually: at x=-128 y=0.048, x=128 y=0.057. Nearly symmetric positive.
        # At x=-25 y=0.018, x=25 y=0.001. Not symmetric.
        # Let's use a smooth function: y_ramp = 0.0002*x + 0.03 gives
        #   -128->0.0044 (no). 
        # Reconsider: maybe far field ~ 0.03 + 0.0002*x is wrong.
        # Data: x=-128:0.048, -100:0.039, -60:0.028, -25:0.018, -15:0.015,
        #   12:-0.021, 15:-0.015, 25:0.001, 40:0.009, 60:0.020, 80:0.031,
        #   100:0.042, 120:0.052, 128:0.057
        # Between -25 and 25 it dips negative. This is the origin structure
        #   bleeding out! The far field beyond |x|>40 is roughly linear.
        # Fit far field |x|>40: (-128,0.048),(-100,0.039),(-60,0.028),
        #   (60,0.020),(100,0.042),(128,0.057)
        # Slope from -128 to -60: (0.028-0.048)/68 = -0.000294
        # Slope from 60 to 128: (0.057-0.020)/68 = 0.000544
        # Not linear either. It's curved (concave up on right, concave down left).
        # Looks like a smooth sigmoid centered near x=0 with range ~0.02-0.05.
        # Try: y_ramp = 0.038 + 0.00015*x? -128->0.019 no.
        # Let's just use a smooth interpolation: y_ramp = 0.038 + 0.0001*x
        #   won't fit. 
        # Better: model far field as 0.038 + 0.00015*x won't work.
        # I'll fit a quadratic through far points: 
        #   (-128,0.048),(0,?), (128,0.057). At x=0 far-field extrapolation?
        # The origin structure dominates near 0 so we can't read it there.
        # Use (-60,0.028) and (60,0.020): midpoint 0.024 at x=0.
        # Use (-100,0.039),(100,0.042): midpoint 0.0405 at x=0. Inconsistent.
        # So far field is not a simple polynomial. 
        # Let me try: y_ramp = 0.03 + 0.0001*x + 0.000001*x^2
        #   x=-128: 0.03-0.0128+0.0164=0.0336 (obs 0.048) no.
        # 
        # Alternative: the whole thing is one smooth function. Let me just
        #   model far field as a gentle curve: y = 0.03 + 0.0002*x won't.
        # 
        # Given difficulty, use piecewise: far field ~ 0.03 + 0.00015*x
        #   but that's wrong. Let me instead use a smooth function that
        #   matches: y_ramp(x) = 0.03 + 0.0001*x + 0.0000005*x^2
        #   x=-128: 0.03-0.0128+0.0082=0.0254 no.
        #
        # OK simpler: use a tanh-like ramp. y_ramp = 0.038 + 0.0002*x
        #   won't fit. 
        # 
        # Let me just fit linear to the outer points and accept error:
        # Using (-128,0.048) and (128,0.057): slope=3.5e-5, intercept=0.0525
        #   x=-60: 0.0525-0.0021=0.0504 (obs 0.028) BAD.
        # 
        # The far field clearly has a dip near x=0 that extends to +-40.
        # So maybe the "origin structure" is wider than I thought.
        # Actually the negative region extends from x~0 to x~40 (E10: 12->-0.021,
        #   15->-0.015, 25->0.001, 40->0.009). And positive lobe from -128 to -15.
        # 
        # New theory: the function is roughly y = 0.03 + 0.0002*x for far field
        #   PLUS a broad negative dip centered around x~10-15.
        # Hmm, but E10 shows smooth transition.
        #
        # Let me try: y = 0.03 + 0.0002*x won't. 
        # 
        # I'll model far field as: 0.038 + 0.00015*x won't.
        #
        # Final approach: use a smooth global function.
        # Fit: y = A + B*tanh((x-c)/w) + origin bumps.
        # Far field: left asymptote ~0.05, right asymptote ~0.06? 
        #   At -128:0.048, at 128:0.057. So A~0.0525, B~0.0045, but
        #   at -60:0.028 (below both) - so there's a dip in middle.
        # 
        # The dip in the middle IS the origin structure. So:
        #   far field = 0.0525 + 0.000035*x (roughly flat, slight rise)
        #   origin structure = broad negative dip + local lobes.
        # At x=-60: far=0.0504, obs=0.028, so origin contributes -0.022.
        # At x=-25: far=0.0516, obs=0.018, origin=-0.034.
        # At x=25: far=0.0534, obs=0.001, origin=-0.052.
        # At x=60: far=0.0546, obs=0.020, origin=-0.035.
        # At x=100: far=0.056, obs=0.042, origin=-0.014.
        # At x=128: far=0.057, obs=0.057, origin=0.
        # At x=-100: far=0.049, obs=0.039, origin=-0.010.
        # At x=-128: far=0.048, obs=0.048, origin=0.
        # So origin structure is a broad negative dip centered ~x=10-20,
        #   width ~60, depth ~0.05, PLUS the local positive lobe at -2 and
        #   negative trough at 1.
        # 
        # Hmm but at x=-2 obs=0.078, far=0.052, origin=+0.026. So positive.
        # At x=1 obs=-0.095, far=0.052, origin=-0.147.
        # 
        # This is getting complex. Let me just build:
        #   far(x) = 0.0525 + 0.000035*x
        #   broad_dip(x) = -0.05 * exp(-((x-15)^2)/(2*50^2))
        #   pos_lobe(x) = 0.05 * exp(-((x+2)^2)/(2*2^2))
        #   neg_lobe(x) = -0.15 * exp(-((x-1)^2)/(2*1.5^2))
        # Check x=-2: 0.0525-0.00007-0.05*exp(-289/5000)-... 
        #   broad: exp(-0.0578)=0.944, -0.0472. pos: +0.05. neg: -0.15*exp(-9/4.5)=-0.0203
        #   total: 0.0525-0.0472+0.05-0.0203=0.035. Obs 0.078. Too low.
        # 
        # The broad dip shouldn't apply at x=-2. Maybe broad dip is only
        #   on the right side? Or the far field baseline is lower.
        # 
        # Let me reconsider. Maybe there's no broad dip, and far field is
        #   just curved. Let me fit far field with a smooth function:
        #   y_far(x) = 0.03 + 0.0002*x won't.
        # 
        # Try: y_far(x) = 0.038 + 0.00015*x + 0.0000008*x^2
        #   x=-128: 0.038-0.0192+0.0131=0.0319 (obs 0.048) no.
        # 
        # I'll go with: far field is a smooth curve through the far points,
        #   and origin structure is added on top. Use a piecewise-linear
        #   interpolation of far-field anchor points, plus local lobes.
        # 
        # Far-field anchors (|x|>40, plus extrapolation):
        #   (-128,0.048),(-100,0.039),(-60,0.028),(60,0.020),(100,0.042),(128,0.057)
        # But we need values near 0 too. From E10: -25:0.018, -15:0.015,
        #   12:-0.021, 15:-0.015, 25:0.001, 40:0.009.
        # These near-0 values include the origin structure. 
        # 
        # Simplest robust approach: use a smooth global fit. Let me use
        #   a cubic-ish spline via a few anchors and linear interpolation,
        #   then add local lobes for the sharp origin features.
        # 
        # Anchors for the "smooth part" (excluding sharp origin lobes):
        #   x=-128:0.048, -100:0.039, -60:0.028, -40:0.022, -30:0.019,
        #   -15:0.015, 12:-0.021, 15:-0.015, 25:0.001, 40:0.009,
        #   60:0.020, 80:0.031, 100:0.042, 120:0.052, 128:0.057
        # Wait these ARE the observations. If I interpolate these, I get
        #   the smooth part. Then the sharp origin lobes (at -2 and 1) are
        #   extra. But the anchors at -15 and 12 already include some lobe.
        # 
        # Actually the origin lobes are sharp (width ~2-3), so at x=-15 and
        #   x=12 they've decayed. So the anchors are mostly "smooth part".
        # Let me interpolate these anchors and add sharp lobes.
        # 
        # But at x=-2, the smooth part from interpolation (-15:0.015 to
        #   12:-0.021) would be ~0.015 + (13/27)*(-0.036) = 0.015-0.0173=-0.002.
        #   Obs at -2 is 0.078. So lobe adds +0.080.
        # At x=1, smooth ~0.015+(16/27)*(-0.036)=0.015-0.0213=-0.006.
        #   Obs -0.095. Lobe adds -0.089.
        # 
        # OK let me just do: smooth interpolation of anchors + two Gaussians.
        # 
        # Anchors (x, y):
        anchors = [
            (-128, 0.0479), (-120, 0.0455), (-100, 0.0394), (-80, 0.0335),
            (-60, 0.0277), (-40, 0.0219), (-30, 0.0191), (-25, 0.0177),
            (-15, 0.0146), (-12, 0.0187), (12, -0.0208), (15, -0.0146),
            (25, 0.0009), (40, 0.0089), (60, 0.0198), (80, 0.0307),
            (100, 0.0415), (120, 0.0522), (128, 0.0565),
        ]
        # Linear interpolation
        def smooth(x):
            if x <= anchors[0][0]:
                return anchors[0][1]
            if x >= anchors[-1][0]:
                return anchors[-1][1]
            for i in range(len(anchors)-1):
                x0,y0 = anchors[i]
                x1,y1 = anchors[i+1]
                if x0 <= x <= x1:
                    t = (x-x0)/(x1-x0)
                    return y0 + t*(y1-y0)
            return anchors[-1][1]
        
        # Sharp origin lobes
        pos = 0.080 * math.exp(-((x+2.0)**2)/(2*2.0**2))
        neg = -0.089 * math.exp(-((x-1.0)**2)/(2*1.5**2))
        y = smooth(x) + pos + neg
        out.append(round(y, 4))
    return {"y": out}
