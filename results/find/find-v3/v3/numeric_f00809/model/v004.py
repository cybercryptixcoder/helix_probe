import math

def predict(probe):
    # Observations:
    # - Outputs are mostly small scatter in ~[-0.25, 0.25], uncorrelated at fine scale [E6,E10,E12].
    # - No smooth low-frequency trend visible [E4,E8,E14].
    # - BUT: for large |x| (roughly |x| > ~60-70), outputs become tiny (~0.005-0.01) [E4,E9,E11,E15].
    #   E4: x=-120..-72 -> ~0.005-0.007; x=-60 -> 0.129 (transition); x=120 -> -0.04 (hmm)
    #   E9: x=-127.7 -> 0.0046; x=-79.1 -> 0.0074; x=-65.6 -> -0.0245
    #   E11: x=-107.4 -> 0.0055; x=-100.1 -> 0.0059; x=-46.1 -> -0.1639 (normal)
    #   E15: x=-79.5 -> 0.0074; x=-80.2 -> 0.0073; x=-105.0 -> 0.0056
    #   So for x < ~-70, output is tiny positive ~0.005-0.007 (looks like a decaying tail).
    #   Positive large x: E4 x=120 -> -0.0404, x=96 -> 0.0753, x=84 -> -0.0134 (not tiny).
    #   E11 x=110.8 -> -0.1859 (normal). E15 x=108.4 -> -0.1099 (normal).
    #   So the tiny-output region is only on the NEGATIVE side, roughly x < -70.
    # - Elsewhere: pseudo-random scatter, magnitude ~0.25, no structure [E6,E10,E12].
    ys = []
    for x in probe["x"]:
        if x < -70:
            # decaying tail: ~0.006 * exp((x+70)/30)? At x=-80 -> 0.0074, x=-105 -> 0.0056, x=-127 -> 0.0046
            # fit roughly: value ~ 0.004 + 0.004*exp((x+70)/20)
            v = 0.004 + 0.004 * math.exp((x + 70) / 20.0)
            ys.append(round(v, 4))
        else:
            h = math.sin(x * 12.9898 + 78.233) * 43758.5453
            frac = h - math.floor(h)
            ys.append(round((frac - 0.5) * 0.5, 4))
    return {"y": ys}
