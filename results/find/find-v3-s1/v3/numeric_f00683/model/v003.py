def predict(probe):
    # Positive side: y = 13.1*x - 4.5 (approx), with small noise [E4,E5,E6,E7,E8,E15,E17]
    # Negative far side (x <= -3): y = 1.3*x - 11.0 (approx) [E4,E5,E6,E7,E15]
    # Negative near-zero region (-3 < x < 0): the output is NOT a clean line.
    #   Observations show a repeating sawtooth/zigzag pattern with period ~0.1
    #   in x, superimposed on a slowly varying baseline. [E10,E12,E14,E16,E18]
    #   The zigzag amplitude is ~1.0 and the pattern repeats every 0.1 in x.
    #   Baseline near 0 is around -11 to -12, decreasing as x decreases.
    # x == 0: special value -385.12 [E2]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(-385.12)
        elif x > 0:
            out.append(13.1 * x - 4.5)
        elif x <= -3:
            out.append(1.3 * x - 11.0)
        else:
            # -3 < x < 0: sawtooth with period 0.1 plus baseline
            # baseline: roughly linear from -11 at x=0 to -14.9 at x=-3
            base = -11.0 + 1.3 * x
            # sawtooth: period 0.1, amplitude ~1.0
            # Use fractional part of x/0.1 to make a triangle wave
            t = (x / 0.1) % 1.0
            # triangle wave in [-0.5, 0.5]
            tri = abs(2.0 * t - 1.0) - 0.5
            out.append(base + 2.0 * tri)
    return {"y": out}
