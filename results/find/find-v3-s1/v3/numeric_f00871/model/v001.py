def predict(probe):
    # Almost all outputs are 0.0/-0.0, except near x ≈ -1.2 where output is 8.2 [E1]
    # Hypothesis (?): a narrow bump centered near x = -1.2; elsewhere 0.
    # Only one nonzero point observed, so bump shape is unknown; guess a small Gaussian-like spike.
    import math
    out = []
    for x in probe["x"]:
        # narrow bump centered at -1.2
        d = x - (-1.2)
        if abs(d) < 1.0:
            out.append(8.2 * math.exp(-(d*d) / 0.5))
        else:
            out.append(0.0)
    return {"y": out}
