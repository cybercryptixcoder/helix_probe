def predict(probe):
    # f(x) = ceil(x) when x lies in a band, else 0 [E2,E3,E4,E6]
    # Positive band: x in (0, 4.3] roughly -> ceil in 1..5; 4.3->5, 4.4->0 [E6]
    #   so upper cutoff is between 4.3 and 4.4. 4.01->5, 4.2->5, 4.3->5, 4.4->0.
    #   Lower positive cutoff: 0.2->1, 0.999->1, 0->0. So x>0.
    # Negative band: -4.3->-4, -4.4->0 [E6]; -4.2->-4, -4.001->-4, -4.999->0 [E4]
    #   so lower cutoff between -4.3 and -4.4. -0.001->0, -0.2->0, -0.8->0, -1.2->-1.
    #   So negative band is x in [-4.3, -1) roughly; -0.8->0 means x<=-1 needed.
    #   Check: -1.2->-1, -0.8->0. So cutoff between -0.8 and -1.2.
    #   -0.001->0, so negatives need x <= -1 (approx). Use x <= -1? -1.0->-1 [E2].
    #   -0.8->0, -1.0->-1: cutoff at -1.0.
    # Positive: 0->0, 0.2->1: cutoff at 0.
    # Upper positive: 4.3->5, 4.4->0: cutoff between 4.3 and 4.4.
    # Lower negative: -4.3->-4, -4.4->0: cutoff between -4.3 and -4.4.
    # Output = ceil(x) within band.
    # Bands: 0 < x <= 4.3 (approx) and -4.3 <= x <= -1 (approx).
    # Need exact cutoffs. 4.3->5 but 4.4->0. -4.3->-4 but -4.4->0.
    # Symmetric-ish: cutoff at 4.3 and -4.3? But 4.49->0, 4.51->0 [E6].
    # Actually 4.3->5, 4.4->0. So cutoff in (4.3,4.4]. Use x <= 4.3.
    # Negative: -4.3->-4, -4.4->0. Use x >= -4.3.
    # But wait, is it symmetric? Positive cutoff ~4.3, negative ~-4.3. 
    # Hmm but 4.3 gives 5 = ceil(4.3). -4.3 gives -4 = ceil(-4.3). Consistent with ceil.
    # What about exact boundary? Use 4.3 and -4.3 inclusive.
    import math
    out = []
    for x in probe["x"]:
        if 0 < x <= 4.3:
            out.append(float(math.ceil(x)))
        elif -4.3 <= x <= -1:
            out.append(float(math.ceil(x)))
        else:
            out.append(0.0)
    return {"y": out}
