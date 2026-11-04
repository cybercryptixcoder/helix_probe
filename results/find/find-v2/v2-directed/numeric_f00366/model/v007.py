def predict(probe):
    # Mechanism inferred from the evidence:
    # The output takes only a few discrete values: 8.8, 9.8, -11.4, -12.4, and 1548.92 at x=0.
    # There are two "bands": a positive-x band and a negative-x band.
    #
    # Negative side (x < 0):
    #   x < -4.1  -> 8.8
    #   -4.1 <= x < 0 -> 9.8
    #   (boundary near -4.1; E5 puts -4.15->8.8 and -4.1->9.8, E6 puts -4.115->8.8, -4.105->9.8)
    #
    # Positive side (x > 0):
    #   small positive x -> -11.4
    #   larger positive x -> -12.4
    #   boundary near 4.3: E5/E6 put 4.305..4.345 -> -12.4, and 4.3? E4 4.3->-12.4,
    #   E5 4.35->-12.4. E4 4.0->-11.4, 4.3->-12.4. E6 4.305->-12.4.
    #   So boundary is between 4.0 and 4.3; E5 4.35 is -12.4. Need finer: E6 has 4.305 already -12.4.
    #   Lower positive boundary: 0.0001->-11.4, 0.01->-11.4, 0.1->-11.4, 0.4->-11.4, 0.5->-11.4,
    #   0.6->-11.4, 1.9->-11.4, 2.1->-11.4, 2.5->-11.4, 3.0->-11.4.
    #   So positive band: 0 < x < ~4.3 -> -11.4; x >= ~4.3 -> -12.4.
    #   Also x=5.0001->-12.4, 4.99->-12.4, 5.01->-12.4, 4.9->-12.4, 5.1->-12.4.
    #
    # Special: x = 0 -> 1548.92 (E1).
    #
    # Boundaries more precisely:
    #   Negative band boundary: between -4.15 (8.8) and -4.105 (9.8). E5: -4.15->8.8, -4.1->9.8.
    #     E6: -4.125->8.8, -4.115->8.8, -4.105->9.8, -4.095->9.8.
    #     So boundary between -4.115 and -4.105. Guess -4.11.
    #   Positive band boundary: E4 4.3->-12.4, 4.0->-11.4. E6 4.305->-12.4.
    #     E5 4.35->-12.4. Need lower: 4.0->-11.4, 4.3->-12.4. E4 4.3->-12.4.
    #     Guess boundary ~4.3? But 4.305->-12.4 and 4.3->-12.4, so maybe 4.3 exactly or lower.
    #     E4 4.2? not tested. 4.0->-11.4. Guess boundary 4.25? E4 4.3->-12.4.
    #     Actually E4 has 4.3->-12.4 and 4.0->-11.4; E6 4.305->-12.4.
    #     Let's guess boundary at 4.3 (x >= 4.3 -> -12.4). But 4.3 itself is -12.4.
    #     Hmm E5 4.35->-12.4. So threshold <= 4.3. Guess 4.3.
    #     Wait, is there a chance threshold is 4.25? Unknown. Use 4.3.
    #
    # Also negative side far: -5.0001->8.8, -4.9999->8.8 (E3). -5.5->8.8. -6->8.8.
    #   -4.8..-4.2->8.8 (E4). -4.0->9.8. -3.8..-3.0->9.8.
    #   So negative: x < -4.11 -> 8.8; -4.11 <= x < 0 -> 9.8.
    #
    # Positive: 0 < x < 4.3 -> -11.4; x >= 4.3 -> -12.4.
    #   Check E1: 20,50,100 -> -12.4. 10->-12.4. 5->-12.4. 2->-11.4. 1->-11.4. 0.5->-11.4.
    #   E1 -0.5->9.8, -1->9.8, -2->9.8, -5->8.8, -10->8.8. Good.
    #
    # The 1548.92 at 0 is a spike.
    #
    # Boundaries uncertain (marked ?): negative threshold -4.11, positive threshold 4.3.
    # Could be -4.11 and 4.3, or nearby. Use these.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            xv = float(x)
        except Exception:
            ys.append(None)
            continue
        if xv == 0:
            ys.append(1548.92)
        elif xv < 0:
            if xv < -4.11:  # ? boundary between -4.115 and -4.105
                ys.append(8.8)
            else:
                ys.append(9.8)
        else:  # xv > 0
            if xv < 4.3:  # ? boundary between 4.0 and 4.3
                ys.append(-11.4)
            else:
                ys.append(-12.4)
    return {"y": ys}
