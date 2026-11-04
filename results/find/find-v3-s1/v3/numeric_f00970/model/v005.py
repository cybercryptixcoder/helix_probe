import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # - Outside a central interval, f is essentially noise-like with small values,
    #   roughly in [-2, 2], no clear smooth structure [E1, E3, E7, E9, E12].
    # - Inside a central interval around x in [-4, 4], outputs are large,
    #   around 10-14, and vary irregularly [E2, E6].
    # - The transition is sharp: |x| ~ 4 is the boundary [E2, E6].
    # - Within the central interval the value is not a simple smooth function;
    #   it looks like a deterministic but complicated/noisy large value.
    # - Outside, values look like small pseudo-random noise; no reproducible
    #   smooth formula is evident from the evidence.
    #
    # Since the outside region shows no consistent smooth rule across probes
    # (same/nearby x give unrelated small values), the best guess is that the
    # box is a noisy function. We model the *mechanism* as:
    #   - a central "active" region [-4, 4] where output is a large value
    #     (centered ~12),
    #   - outside, small noise around 0.
    #
    # For prediction we return a representative value: large near the center,
    # small outside. Exact noise is unpredictable, so we return the mean
    # behavior of each regime.

    x = probe.get("x", [])
    ys = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            ys.append(None)
            continue

        if -4.0 <= v <= 4.0:
            # Central region: large values, mean ~12 [E2, E6]
            ys.append(12.0)
        else:
            # Outside region: small noise around 0 [E1, E3, E7, E9, E12]
            ys.append(0.0)

    return {"y": ys}
