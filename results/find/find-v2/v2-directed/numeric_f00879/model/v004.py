import math

def predict(probe):
    # Observations:
    # - Output is noisy; repeated x gives different y [E2,E3,E4,E5,E6,E7,E8,E9,E10].
    # - Mean depends on x, not constant [E5,E10]: x=-3 mean ~0.02, x=-1 mean ~0.31,
    #   x=1 mean ~2.28, x=3 mean ~2.28.
    # - Sign-dependent step: negatives near 0 or slightly negative, positives ~2 [E10].
    # - E9: x=-12..-3 mean ~ -1.5, x=1 mean ~2.7, x=3 mean ~2.9.
    # - E7: x=-10..-0.5 mean ~ -1.0, x=0 mean ~0.06, x=0.5 mean ~1.7.
    # - E6: x=-30..-1 mean ~ -1.0, x=0 mean ~0.6.
    # - E3: x=0.5 mean ~2.5, x=3 mean ~1.5, x=5 mean ~0.0, x=10 mean ~0.7, x=20 mean ~0.35;
    #   negatives: x=-0.5 ~0.2, x=-3 ~-0.16, x=-5 ~-1.0, x=-10 ~-1.7, x=-20 ~-0.88.
    # - E4: x=0.25..8 mean ~1.5; x=-0.25..-1.5 mean ~-0.5.
    # - E1: large |x| noisy, near 0 mean; positives slightly higher.
    # - Best guess: step function. Negative x -> mean ~ -1 (but near 0 slightly positive),
    #   positive x -> mean ~ +2 (but decays for large x). Noise sd ~1.2.
    # Model: mean = -1 for x<-1, ramp to +2 for x in [-1,1], +2 for 1<x<4, decay for x>4.
    out = []
    for x in probe["x"]:
        try:
            x = float(x)
            if x < -1:
                m = -1.0
            elif x < 1:
                m = -1.0 + 3.0 * (x + 1.0) / 2.0
            elif x < 4:
                m = 2.0
            else:
                m = 2.0 * math.exp(-(x - 4.0) / 8.0)
        except Exception:
            m = 0.0
        out.append(m)
    return {"y": out}
