def predict(probe):
    # Small |x| (roughly -20..20) gives ~8 + small wiggle: y ≈ 8 + x/10? [E1]
    #   x=-1.2 -> 19.52, x=-12.9 -> 8.13, x=-62.7 -> 8.03, x=-93.6 -> 7.90
    # Large positive x gives large negative y: 88.9->-845.44, 67.5->-640, 73.9->-701.44, 38.8->-364.48
    # Large negative x gives ~8 (same as small): -104 -> 7.97, -120.7 -> 8.06
    # Pattern: for x>~20, y ≈ -9.5*x (88.9*-9.5=-844.6; 67.5*-9.5=-641; 73.9*-9.5=-702; 38.8*-9.5=-368.6)
    # For x<20, y ≈ 8 + something small; x=-1.2 -> 19.52 is odd (maybe 8 + 9.6*|x|/... ?)
    # Best guess: piecewise. x>20: y = -9.5*x. x<=20: y ≈ 8 + 9.6*exp(-|x|/something)?
    #   -1.2 -> 19.52 (extra 11.5), -12.9 -> 8.13 (extra 0.13), -62.7 -> 8.03
    #   Try y = 8 + 11.6*exp(-(x+1.2)^2/...)? too speculative. Use 8 + 11.5*exp(-(x+1.2)^2/2)?
    #   At x=-12.9: exp(-(11.7)^2/2)≈0 -> 8. ok. At x=-1.2: 8+11.5=19.5 ok.
    #   At x=-62.7: 8. ok. At x=-93.6: 8. ok.
    import math
    out = []
    for x in probe["x"]:
        if x > 20:
            y = -9.5 * x
        else:
            y = 8 + 11.5 * math.exp(-((x + 1.2) ** 2) / 2.0)
        out.append(round(y, 4))
    return {"y": out}
