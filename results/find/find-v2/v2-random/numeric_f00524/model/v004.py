import math

def predict(probe):
    # Beliefs:
    # The function is zero almost everywhere [E1-E6].
    # It is nonzero only at a few isolated points, and the nonzero value
    # appears to be an integer equal to a small count/rank-like quantity.
    #
    # Observed nonzero points:
    #   x=2.9  -> 3.0   [E1]
    #   x=1.2  -> 2.0   [E2]
    #   x=-1.6 -> -1.0  [E5]
    #   x=2.0  -> 2.0   [E6]
    #
    # All other sampled x in [-128,128] give 0.0 (or -0.0).
    #
    # The nonzero inputs are all near small integers / near the origin.
    # A simple mechanism consistent with the data is:
    #   f(x) = round(x) if x is within some small distance of an integer
    #          and that integer is in a small set; otherwise 0.
    # But the values do not match round(x) exactly:
    #   2.9 -> 3 (matches round)
    #   1.2 -> 2 (does NOT match round; round(1.2)=1)
    #   -1.6 -> -1 (round(-1.6)=-2, so no)
    #   2.0 -> 2 (matches)
    #
    # Better guess: the output is the nearest integer n such that x lies in
    # an interval around n, but the intervals are shifted/asymmetric.
    # The data are too sparse to pin down exact boundaries.
    #
    # Most likely mechanism given the evidence:
    # f(x) = n for x in a narrow interval around n, where n is a small
    # integer, and 0 elsewhere. The nonzero region seems confined to
    # roughly [-2, 3].
    #
    # I will model it as: if x is within 0.5 of an integer n in {-1,0,1,2,3},
    # return n, else 0. This captures 2.0->2, 1.2->? (would be 1, but data says 2),
    # so adjust: use nearest integer with a bias.
    #
    # Given 1.2 -> 2 and -1.6 -> -1 and 2.9 -> 3, the mapping looks like
    # ceil(x) for positive and trunc/ceil for negative:
    #   ceil(1.2)=2, ceil(2.9)=3, ceil(2.0)=2, ceil(-1.6)=-1.
    # That matches ALL nonzero observations!
    #
    # So hypothesis: f(x) = ceil(x) when x is in some special interval,
    # else 0. But ceil is defined everywhere; the zero outputs mean the
    # function is zero outside a small interval.
    #
    # The nonzero x values are 1.2, 2.0, 2.9, -1.6. These lie in [-2, 3].
    # All other probes (many across [-128,128]) give 0.
    #
    # So: f(x) = ceil(x) if x is in (-2, 3) (or similar), else 0.
    # Check: -1.6 in (-2,3) -> ceil(-1.6) = -1.0 ✓
    #        1.2 -> ceil = 2 ✓
    #        2.0 -> 2 ✓
    #        2.9 -> 3 ✓
    #        All other x outside -> 0 ✓
    #
    # Boundary uncertainty: we have no samples between -2 and -1.6, or
    # between 2.9 and 3, or just outside. I'll use [-2, 3] as the interval.
    # Marked with "?".

    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # Nonzero region: x in [-2, 3] (boundaries uncertain)
            if -2.0 <= x <= 3.0:
                ys.append(float(math.ceil(x)))
            else:
                ys.append(0.0)
        return {"y": ys}
    except Exception:
        # Never raise
        try:
            n = len(probe.get("x", []))
            return {"y": [0.0] * n}
        except Exception:
            return {"y": []}
