def predict(probe):
    # Overall shape: f is smooth, monotone decreasing in x [E1]
    # For x in [-128,-16]: linear with slope ~ -1.75 per unit [E1]
    #   check: f(-128)=215.77, f(-16)=19.44 -> slope (19.44-215.77)/112 = -1.753
    # For x in [-16, 0]: still decreasing but flattening, slope ~ -1.75 near -16,
    #   ~ -1.88 near 0? Actually f(-16)=19.44, f(0)=-8.67 -> slope -1.757, consistent
    # For x>0: curve steepens sharply (convex), f(128)=-328 [E1]
    # So f looks like a smooth decreasing function, roughly linear on the left,
    #   curving downward (accelerating negative) on the right.
    # Guess: f(x) = a*x + b + c*something? Try a cubic-ish / softplus-like curve.
    # Fit: left linear slope ~ -1.753, intercept at 0 ~ -8.67.
    #   At x=128 linear would give -8.67 -1.753*128 = -233; actual -328, extra -95.
    #   At x=32 linear: -8.67-56.1=-64.8; actual -88.5, extra -23.7.
    #   At x=16 linear: -36.7; actual -48.6, extra -11.9.
    #   At x=8 linear: -22.7; actual -28.6, extra -5.9.
    #   At x=4 linear: -15.7; actual -18.6, extra -2.9.
    #   At x=2 linear: -12.2; actual -13.6, extra -1.4.
    #   At x=1 linear: -10.4; actual -11.1, extra -0.7.
    #   Extra term ~ -0.74*x for x>0? At x=128: -94.7 yes! x=32: -23.7 yes!
    #   x=16: -11.8 yes, x=8: -5.9 yes, x=4: -3.0 yes, x=2: -1.5 yes, x=1: -0.74 yes.
    # So for x>=0: f(x) = -8.67 - 1.753*x - 0.74*x = -8.67 - 2.49*x? 
    #   Check x=128: -8.67-318.7=-327.4 vs -328.4 close.
    #   But wait, that's just linear with slope -2.49 for x>=0.
    # For x<0: slope -1.753. So piecewise linear with a kink at 0!
    #   f(-8)=5.42; -8.67 -1.753*(-8)=5.35 close.
    #   f(-1)=-6.79; -8.67+1.753=-6.92 close.
    #   f(-2)=-5.08; -8.67+3.51=-5.16 close.
    #   f(-4)=-1.63; -8.67+7.01=-1.66 close.
    #   f(-128)=215.77; -8.67+224.4=215.7 yes!
    # So: f(x) = -8.67 - 1.753*x for x<=0; f(x) = -8.67 - 2.49*x for x>=0.
    # Slight curvature likely; refine with a smooth kink. Use exact-ish fit.
    # Refine intercept/slopes from data:
    #   left: f(-128)=215.7687, f(-16)=19.4414 -> slope=-1.75292, b at 0 = 19.4414+16*1.75292=47.488? 
    #   Wait recompute: f(0) should be b. f(-16)=b+16*1.75292 -> b=19.4414-28.047=-8.605.
    #   f(-128)=b+128*1.75292=-8.605+224.37=215.77 yes.
    #   right: f(128)=-328.4446, f(1)=-11.1045 -> slope=(-328.4446+11.1045)/127=-2.49874
    #   b = -11.1045+2.49874=-8.606. Consistent!
    # So b=-8.606, left slope -1.7529, right slope -2.4987.
    # Likely smooth (MLP) so use a soft kink. But piecewise linear is close.
    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            if v <= 0:
                y = -8.606 - 1.7529 * v
            else:
                y = -8.606 - 2.4987 * v
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
