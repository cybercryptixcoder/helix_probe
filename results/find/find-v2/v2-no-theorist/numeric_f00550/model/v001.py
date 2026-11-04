def predict(probe):
    # f(x) returns 0.0 for all tested inputs [E1]
    # Hypothesis: f is the zero function over the whole domain (or at least
    #   over the tested range -128..128); no evidence of any other region.
    return {"y": [0.0 for _ in probe["x"]]}
