import math

def predict(probe):
    # Outputs are ~0 almost everywhere [E1-E21].
    # Nonzero outputs occur at scattered x values, irregular in x and magnitude:
    #   1.2->2.2 [E2], -1.6->9.2 [E5], 2.0->0.2 [E6], 0.9->2.95 [E15]
    #   -1.4->8.7 [E21], -87.6->0.1256 [E21]
    #   -79.1->0.0216 [E5], -79.5->0.0837 [E8], -80.2->0.0164 [E8],
    #   -80.6->0.3173 [E13], -81.8->0.0731 [E14], -84.6->0.0645 [E15],
    #   -83.2->0.1689 [E16], -78.8->0.1758 [E19]
    # Spikes near -80..-88 form a noisy/irregular region; treat as isolated points.
    # ? No smooth rule fits; keep as isolated spikes.
    spikes = {
        1.2: 2.2,
        -1.6: 9.2,
        2.0: 0.2,
        0.9: 2.95,
        -1.4: 8.7,
        -87.6: 0.1256,
        -79.1: 0.0216,
        -79.5: 0.0837,
        -80.2: 0.0164,
        -80.6: 0.3173,
        -81.8: 0.0731,
        -84.6: 0.0645,
        -83.2: 0.1689,
        -78.8: 0.1758,
    }
    ys = []
    for x in probe["x"]:
        ys.append(spikes.get(x, 0.0))
    return {"y": ys}
