def predict(probe):
    # Observations suggest f is roughly linear with slope ~ -2.6 for positive x
    # and slope ~ -1.6 for negative x? Let's check ratios.
    # E1: x=88.2 -> -228.97 (ratio -2.596); x=66 -> -173.49 (-2.629)
    # x=72.7 -> -190.23 (-2.617); x=21.3 -> -61.81 (-2.902)
    # x=2.9 -> -15.84 (-5.46)  <- not linear near 0?
    # x=-6 -> 1.91 (ratio -0.318)
    # x=-20.3 -> 26.97 (-1.329); x=-24.3 -> 33.98 (-1.398)
    # x=-50.4 -> 79.75 (-1.582); x=-61.7 -> 99.56 (-1.614)
    # Looks like f(x) ≈ -2.6*x for x>0, and ≈ -1.6*x for x<0, with a smooth
    # transition near 0 (maybe tanh-like). Near 0 slope is steeper.
    # Try f(x) = -a*x for large |x|, with a blending.
    # Actually ratios: positive side ~ -2.6, negative side ~ -1.6.
    # A plausible MLP approximation: f(x) = -2.1*x - 0.5*x*tanh(x/s) ...
    # Let's fit: at x=2.9, y=-15.84 => effective slope -5.46 (steeper).
    # at x=-6, y=1.91 => slope -0.318 (shallower, near zero crossing?).
    # Hmm, maybe f has a nonlinear shape. Let's try f(x) = A*x + B*tanh(C*x).
    # For large x>0: slope A+B*C ~ -2.6. For large x<0: slope A+B*C ~ -2.6 too
    # (tanh saturates symmetric). But observed negative slope is -1.6, so
    # asymmetric. Maybe f(x) = A*x + B*tanh(C*x) + D? 
    # Let's just try a simple piecewise linear guess with a smooth blend.
    # Use f(x) = -2.6*x for x>0, -1.6*x for x<0, but near 0 it's steeper.
    # Actually at x=2.9 slope -5.46, at x=-6 slope -0.318. That's weird.
    # Maybe f(x) = -2.6*x + something. At x=2.9: -2.6*2.9=-7.54, observed -15.84,
    # diff -8.3. At x=-6: -2.6*-6=15.6, observed 1.91, diff -13.7.
    # Try f(x) = -2.6*x - 10*tanh(x/10)? At x=2.9: -7.54 - 10*tanh(0.29)= -7.54-2.83=-10.37 no.
    # Let's try f(x) = a*x + b*tanh(c*x) with a=-2.1, b=-0.5, c=1?
    # x=88.2: -185.2 -0.5 = -185.7 no.
    # Let's estimate: for large positive, slope -2.6; large negative slope -1.6.
    # Asymmetric tanh: f(x) = -2.1*x - 0.5*x*tanh(x/10) - ... 
    # Simpler: f(x) = -2.1*x - 0.5*|x|*tanh(x/10)? 
    # At x=88: -184.8 - 0.5*88 = -228.8 ✓ (approx -228.97)
    # At x=66: -138.6 - 33 = -171.6 (obs -173.49) close
    # At x=-61.7: 129.6 - 0.5*61.7*(-1)= 129.6+30.85=160.4 no (obs 99.56)
    # Hmm sign wrong. Try f(x) = -2.1*x + 0.5*|x|*tanh(x/10):
    # x=88: -184.8+44=-140.8 no.
    # Let's just do piecewise: f(x) = -2.6*x for x>0, -1.6*x for x<0, with
    # a smooth transition. Check x=2.9: -2.6*2.9=-7.54 vs obs -15.84. Not great.
    # Maybe there's an offset: f(x) = -2.6*x + k for x>0. At x=88.2: -229.3+k=-228.97 => k=0.36
    # x=66: -171.6+0.36=-171.24 vs -173.49. Off by 2.
    # Slope from (66,-173.49) and (88.2,-228.97): (-228.97+173.49)/(88.2-66)= -55.48/22.2=-2.499
    # From (21.3,-61.81) and (66,-173.49): -111.68/44.7=-2.498
    # From (2.9,-15.84) and (21.3,-61.81): -45.97/18.4=-2.498
    # So slope is -2.5 for x>0! Intercept: -15.84 - (-2.5*2.9)= -15.84+7.25=-8.59
    # Check x=88.2: -2.5*88.2-8.59=-220.5-8.59=-229.09 ✓ (obs -228.97)
    # x=66: -165-8.59=-173.59 ✓
    # x=72.7: -181.75-8.59=-190.34 ✓
    # x=21.3: -53.25-8.59=-61.84 ✓
    # So for x>0: f(x) = -2.5*x - 8.6
    # For x<0: from (-20.3,26.97) and (-61.7,99.56): slope=(99.56-26.97)/(-61.7+20.3)=72.59/-41.4=-1.753
    # From (-24.3,33.98) and (-50.4,79.75): 45.77/-26.1=-1.754
    # From (-6,1.91) and (-20.3,26.97): 25.06/-14.3=-1.752
    # So slope -1.75 for x<0. Intercept: 1.91 - (-1.75*-6)=1.91-10.5=-8.59
    # Check x=-61.7: -1.75*-61.7-8.59=107.975-8.59=99.385 ✓
    # So f(x) = -2.5*x - 8.6 for x>0, and -1.75*x - 8.6 for x<0.
    # At x=0 both give -8.6. So it's continuous! 
    # So f(x) = -8.6 + (-2.5*x if x>0 else -1.75*x)
    # This is a piecewise linear with kink at 0.
    def f(x):
        if x > 0:
            return -2.5*x - 8.6
        else:
            return -1.75*x - 8.6
    return {"y": [f(x) for x in probe["x"]]}
