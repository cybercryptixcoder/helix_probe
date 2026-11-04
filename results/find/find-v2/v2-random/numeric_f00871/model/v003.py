import math

def predict(probe):
    # Most outputs are ±0.0: f is ~0 almost everywhere [E1-E6].
    # Nonzero values appear only at specific x: 2.2 at x=1.2 [E2],
    # 9.2 at x=-1.6 [E5], 0.0216 at x=-79.1 [E5], 0.2 at x=2.0 [E6].
    # These look like isolated spikes at particular input values, not a
    # smooth bump: 1.2->2.2, -1.6->9.2, 2.0->0.2, -79.1->0.0216.
    # Hypothesis (?): f(x) is zero except at a sparse set of special x
    # values where it returns a fixed nonzero value. Model as a lookup of
    # known spikes; everything else 0.
    spikes = {
        1.2: 2.2,
        -1.6: 9.2,
        2.0: 0.2,
        -79.1: 0.0216,
    }
    ys = []
    for x in probe["x"]:
        ys.append(spikes.get(x, 0.0))
    return {"y": ys}
