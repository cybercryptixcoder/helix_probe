import math

def predict(probe):
    # Most outputs are ±0.0: f is ~0 almost everywhere [E1-E13].
    # Nonzero outputs occur near x = -80: -79.1->0.0216 [E5], -79.5->0.0837,
    #   -80.2->0.0164 [E8], -80.6->0.3173 [E13]. This is a bump/peak
    #   centered near x ~ -80, not an isolated spike.
    # Other nonzero values (1.2->2.2 [E2], -1.6->9.2 [E5], 2.0->0.2 [E6])
    #   are isolated spikes at specific x values.
    # Hypothesis: f(x) = spike(x) + bump(x), where bump is a narrow
    #   Gaussian-like peak around x=-80, and spikes are at known x.
    spikes = {
        1.2: 2.2,
        -1.6: 9.2,
        2.0: 0.2,
    }
    ys = []
    for x in probe["x"]:
        y = spikes.get(x, 0.0)
        # bump near -80: fit from (-79.1,0.0216),(-79.5,0.0837),
        # (-80.2,0.0164),(-80.6,0.3173). Peak ~ -80.6, width ~0.5.
        # Use Gaussian centered at -80.6 with amplitude ~0.32, sigma ~0.5.
        y += 0.32 * math.exp(-((x + 80.6) ** 2) / (2 * 0.5 ** 2))
        ys.append(y)
    return {"y": ys}
