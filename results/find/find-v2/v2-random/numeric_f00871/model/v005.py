import math

def predict(probe):
    # Most outputs are ±0.0: f is ~0 almost everywhere [E1-E14].
    # Nonzero outputs cluster near x = -80, but they are NOT a smooth bump:
    #   -79.1 -> 0.0216 [E5]
    #   -79.5 -> 0.0837 [E8]
    #   -80.2 -> 0.0164 [E8]
    #   -80.6 -> 0.3173 [E13]
    #   -81.8 -> 0.0731 [E14]
    # These are irregular in x and magnitude, so treat them as isolated
    # spikes at specific x values rather than a Gaussian [E5,E8,E13,E14].
    # Other isolated spikes: 1.2->2.2 [E2], -1.6->9.2 [E5], 2.0->0.2 [E6].
    spikes = {
        1.2: 2.2,
        -1.6: 9.2,
        2.0: 0.2,
        -79.1: 0.0216,
        -79.5: 0.0837,
        -80.2: 0.0164,
        -80.6: 0.3173,
        -81.8: 0.0731,
    }
    ys = []
    for x in probe["x"]:
        ys.append(spikes.get(x, 0.0))
    return {"y": ys}
