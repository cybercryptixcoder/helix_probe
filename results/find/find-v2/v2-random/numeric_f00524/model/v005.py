import math

def predict(probe):
    # Beliefs:
    # The function is zero almost everywhere [E1-E10].
    # It is nonzero only at a few isolated points, and the nonzero value
    # appears to be an integer equal to a small count/rank-like quantity.
    #
    # Observed nonzero points:
    #   x=2.9  -> 3.0   [E1]
    #   x=1.2  -> 2.0   [E2]
    #   x=-1.6 -> -1.0  [E5]
    #   x=2.0  -> 2.0   [E6]
    #   x=-3.5 -> -3.0  [E10]
    #
    # All other sampled x in [-128,128] give 0.0 (or -0.0).
    #
    # The nonzero inputs are all near small integers / near the origin.
    # The mapping matches ceil(x):
    #   ceil(2.9)=3, ceil(1.2)=2, ceil(-1.6)=-1, ceil(2.0)=2, ceil(-3.5)=-3.
    # That matches ALL nonzero observations.
    #
    # So hypothesis: f(x) = ceil(x) when x is in some special interval,
    # else 0. The nonzero x values are 1.2, 2.0, 2.9, -1.6, -3.5.
    # These lie in [-4, 3]. All other probes give 0.
    #
    # So: f(x) = ceil(x) if x is in (-4, 3) (or similar), else 0.
    # Check: -3.5 in (-4,3) -> ceil(-3.5) = -3.0 ✓
    #        -1.6 -> ceil = -1 ✓
    #        1.2 -> ceil = 2 ✓
    #        2.0 -> 2 ✓
    #        2.9 -> 3 ✓
    #        All other x outside -> 0 ✓
    #
    # Boundary uncertainty: we have no samples between -4 and -3.5, or
    # between 2.9 and 3, or just outside. I'll use [-4, 3] as the interval.
    # Marked with "?".

    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # Nonzero region: x in [-4, 3] (boundaries uncertain)
            if -4.0 <= x <= 3.0:
                ys.append(float(math.ceil(x)))
            else:
                ys.append(0.0)
        return {"y": ys}
    except Exception:
        try:
            n = len(probe.get("x", []))
            return {"y": [0.0] * n}
        except Exception:
            return {"y": []}
