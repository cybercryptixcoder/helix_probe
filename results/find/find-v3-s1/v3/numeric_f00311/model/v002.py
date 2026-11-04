def predict(probe):
    # Piecewise linear, no noise [E1, E2]:
    #   x <= 20:  y = 2*x        (x=15->30? no: -136/15... check)
    # Actually E2 shows x=15->-136, 18->-164.8, 20->-184: slope -9.2, intercept ~2
    #   x=5->-40, 10->-88, 15->-136, 18->-164.8, 20->-184, 21->-193.6 ...
    #   All fit y = -9.2*x + 2 exactly (5*-9.2+2=-44? no). Try y = -9.2x+2: 5->-44 wrong.
    #   x=5->-40 => -8x; x=10->-88 => -8.8x; x=15->-136 => -9.067x
    #   Fit line through (5,-40),(100,-952): slope=-9.6, intercept=8. Check: 5*-9.6+8=-40 ✓
    #   10->-88 ✓, 15->-136 ✓, 18->-164.8 ✓, 20->-184 ✓, 100->-952 ✓, 80->-760 ✓
    # So for x>~? y = 8 - 9.6*x. But small |x| gave ~8 (x=-1.2->19.52 is odd).
    # Negative x: -30->8.07, -50->8.15, -80->7.98, -104->7.97: y≈8.
    # x=-1.2->19.52 is the outlier; maybe noise or special point. Treat as ~8 baseline.
    # Rule: x > 0 (or some threshold): y = 8 - 9.6*x ; x <= 0: y ≈ 8.
    # Check x=5 positive -> -40 ✓. x=-1.2 -> 8 (observed 19.52, off but single point).
    out = []
    for x in probe["x"]:
        if x > 0:
            y = 8 - 9.6 * x
        else:
            y = 8.0
        out.append(round(y, 4))
    return {"y": out}
