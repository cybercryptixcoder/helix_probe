def predict(probe):
    # Region 1: x < -12 (approx): y ≈ 8 (constant, small noise) [E2: -25..-12 all ~8]
    # Region 2: x >= -12: y = 8 - 9.6*x [E1: -6->65.6, 2.9->-19.84, 21.3->-196.48, 66, 88.2, 72.7 all exact]
    #   E2: -8->84.8 = 8-9.6*(-8)=84.8 ✓; -4->46.4 ✓; -2->27.2 ✓; 0->8 ✓; 5->-40 ✓; 10->-88 ✓; 15->-136 ✓; 18->-164.8 ✓; 19->-174.4 ✓
    # Boundary between -12 and -10: -12->7.7969 (~8), -10->7.8936 (~8), -8->84.8 (linear).
    #   So boundary is between -10 and -8. Guess -9? or -10? -10 gives ~8 (7.89). -8 gives linear.
    #   Threshold: x <= -10 -> 8, x > -10 -> 8-9.6x. (boundary between -10 and -8, pick -10)
    out = []
    for x in probe["x"]:
        if x <= -10:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}
