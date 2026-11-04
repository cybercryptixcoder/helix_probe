def predict(probe):
    # E1: all outputs -0.0 across wide range of ordinary x
    # E2: most outputs are -0.0, but a few are nonzero:
    #     x=0.5 -> -1.625, x=-0.5 -> -3.425, x=0.0 -> -1.7
    # So f is zero almost everywhere, but nonzero near x=0 (within |x|<1?).
    # Hypothesis: there is a special interval around 0 where f behaves differently.
    # Need to pin down boundaries. For now: nonzero only for |x| < 1.
    # Values: f(0.5)=-1.625, f(-0.5)=-3.425, f(0)=-1.7.
    # Guess a linear form? f(x) = a + b*x through these three points?
    #   f(0) = a = -1.7
    #   f(0.5) = -1.7 + 0.5b = -1.625 -> b = 0.15
    #   f(-0.5) = -1.7 - 0.5b = -3.425 -> b = 3.45  (inconsistent)
    # Not linear. Could be noisy. Use piecewise constant / interpolation guess.
    # ? Best guess: within |x|<1, f(x) = -1.7 + something; use nearest known.
    # For safety, model as: |x|<1 -> interpolate from known points; else 0.
    ys = []
    for x in probe["x"]:
        if x is None:
            ys.append(None)
        elif abs(x) < 1.0:
            # ? crude: linear between (-0.5,-3.425),(0,-1.7),(0.5,-1.625)
            if x <= 0:
                # between -0.5 and 0
                t = (x + 0.5) / 0.5
                ys.append(-3.425 + t * (-1.7 + 3.425))
            else:
                t = x / 0.5
                ys.append(-1.7 + t * (-1.625 + 1.7))
        else:
            ys.append(-0.0)
    return {"y": ys}
