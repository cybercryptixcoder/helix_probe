def predict(probe):
    # f(x) = quartic Q(x) = -1.2x^4 - 3x^3 + 0.9x^2 - 1.6x - 36.8 for x>0 [E2]
    # x=0 gives 472.73 (special point) [E2]
    # For x<0: Q(x) + 25.1, EXCEPT clamped at -24973124.7 for very negative x [E4,E6,E8]
    # E8: x=-100,-110,-120,-128 all give ~-24973124.7 (a floor/clamp), not Q+25.1
    # E8: x=-90 gives -76537577.7 = Q(-90)+25.1, so clamp kicks in between -90 and -100
    # E5: x=-102.2 gives -24973124.5612 (clamped); x=-48.6,-7.1,-16.9 unclamped [E5,E7]
    # E7: x=-124.4 gives -24973124.6994 (clamped) [E7]
    # So negative branch: y = max(Q(x)+25.1, -24973124.7)? Check: Q(-90)+25.1=-76537577.7 (below floor, so max gives floor... no)
    # Actually Q(-90) is very negative (-76537577), and observed is that value, so NOT clamped there.
    # Clamp is a LOWER bound on y? -24973124.7 > -76537577.7. So y = max(Q(x)+25.1, -24973124.7) would give -24973124.7 at x=-90. But observed -76537577.7. Contradiction.
    # Reconsider: clamp value -24973124.7 appears for x=-100..-128. Q(-100)+25.1 = -116990851.7 (much lower).
    # So for x <= some threshold, y is constant -24973124.7. Threshold between -90 and -100.
    # Let's find where Q(x)+25.1 = -24973124.7: solve -1.2x^4-3x^3+0.9x^2-1.6x-36.8+25.1 = -24973124.7
    # At x=-95: 95^4=81450625, *-1.2=-97740750; -3*(-857375)=+2572125; 0.9*9025=8122.5; +152; -11.7
    #   = -97740750+2572125+8122.5+152-11.7 = -95160362.2. Still below -24973124.7.
    # Hmm, so the clamp is not where Q crosses. It's a hard region boundary.
    # E8: -90 unclamped, -100 clamped. Boundary in (-100,-90].
    # E5: -102.2 clamped. E7: -124.4 clamped. All consistent with threshold ~ -95 to -100.
    # Guess threshold: x < -95 clamps to -24973124.7? Need to check -90 vs -100. 
    # Let's test: is it maybe |x|>95? or x<=-96? Unknown exact. Use -95 as guess? 
    # Actually maybe the clamp is a floor on |x|: for x <= -100? But -90 unclamped, -100 clamped.
    # Let me guess threshold at x < -95 (midpoint). Mark with ?.
    # Also check E4 small negatives: -0.5..-10 all match Q+25.1 exactly, no clamp. Good.
    # E6 tiny negatives match Q+25.1. Good.
    # The clamp constant: average of E8 values ~ -24973124.6. Use -24973124.7? 
    # E5 -102.2: -24973124.5612; E7 -124.4: -24973124.6994; E8 -100: -24973124.6658, -110: -24973124.7335, -120: -24973124.5692, -128: -24973124.4336
    # These vary slightly -> noisy. Use -24973124.6 as central estimate.
    def Q(x):
        return -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x - 36.8
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(472.73)
            elif x > 0:
                out.append(Q(x))
            else:
                if x < -95:  # ? clamp threshold between -90 and -100
                    out.append(-24973124.6)  # ? noisy constant
                else:
                    out.append(Q(x) + 25.1)
        except Exception:
            out.append(None)
    return {"y": out}
