import math

def predict(probe):
    # Observations:
    # - Same x gives different y on repeat [E2, E3]: output is noisy.
    # - But the *distribution* depends on x: for x>0 outputs skew high,
    #   for x<0 outputs skew low [E3]. E.g. x=0.5 -> ~2.5, x=-0.5 -> ~0.4/-0.03.
    # - E3 pairs: (0.5: 2.45,2.68), (3: 2.06,0.93), (5: -0.68,0.70), (10: 1.22,0.19),
    #   (20: 0.82,-0.11); negatives: (-0.5: 0.39,0.03), (-3: -0.28,-0.04),
    #   (-5: -1.46,-0.61), (-10: -1.82,-1.61), (-20: -0.89,-0.87).
    # - So mean rises with x, roughly: mean ~ a*tanh(x/scale) + b, with a>0.
    #   Positives average ~+1.2, negatives average ~-0.7. Range ~[-2,3] [E1].
    # - E1 broad sweep also consistent with a positive trend plus noise.
    # Model: y = 0.9*tanh(x/8) + 0.25 + noise (uniform-ish, sd ~0.9).
    # We can only predict the mean; return expected value per x.
    out = []
    for x in probe["x"]:
        try:
            x = float(x)
            m = 0.9 * math.tanh(x / 8.0) + 0.25
        except Exception:
            m = 0.25
        out.append(m)
    return {"y": out}
