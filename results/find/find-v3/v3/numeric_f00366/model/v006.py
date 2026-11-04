import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Structure: sign(x) picks a family; |x| picks inner/outer value.
    #   x == 0: 1548.92 (isolated spike) [E2]
    #   x < 0: 9.8 if |x| < B, else 8.8 [E1,E2,E4,E5,E7,E9]
    #   x > 0: -11.4 if |x| < B, else -12.4 [E1,E2,E4,E5,E7,E9]
    # No special near-zero band: tiny nonzero values follow sign rule [E6].
    #
    # Boundary B (symmetric on both sides):
    #   Negative: -4.04..-3.96 -> 9.8 (inner); -4.05 -> 9.8 (inner) [E8,E10]
    #     So |x| <= 4.05 is inner on negative side. Need upper bound: E4 -4.1 -> 9.8 inner.
    #     Wait E10 only tested up to -3.96; E4 -4.1 -> 9.8 inner. So negative inner up to at least 4.1?
    #     But E8: -4.05 -> 9.8 inner. E4: -4.1 -> 9.8 inner, -4.5 -> 8.8 outer.
    #     Hmm, but E10 title says "both are below 4.05/4.15" — yet E10 negative values all inner.
    #     Actually E10 negatives are all between -4.04 and -3.96, all inner. Doesn't pin upper.
    #     E4: -4.1 inner, -4.5 outer. So negative boundary in (4.1, 4.5].
    #   Positive: E10: 4.04..4.10 -> -11.4 inner; 4.11..4.15 -> -12.4 outer.
    #     So positive boundary in (4.10, 4.11]. Very tight! B_pos ≈ 4.105.
    #     E4: 4.1 inner, 4.5 outer — consistent.
    #   Negative side: E8 -4.05 inner, E4 -4.1 inner, -4.5 outer. 
    #     E10 didn't test beyond -4.04 on negative side. So negative boundary in (4.1, 4.5].
    #     But symmetry suggests same boundary as positive (~4.105). E8 -4.05 inner consistent.
    #     Let's assume symmetric B ≈ 4.105.
    #   Actually check: is negative boundary maybe also ~4.105? E4 -4.1 inner (4.1 < 4.105 ✓).
    #     Yes consistent. Use B = 4.105 for both. "?" on exact value.
    #
    # Values: 9.8, 8.8, -11.4, -12.4, 1548.92 at 0.

    B = 4.105  # boundary, positive side pinned to (4.10,4.11] [E10]; assume symmetric "?"

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            xv = float(x)
        except (TypeError, ValueError):
            ys.append(None)
            continue
        if math.isnan(xv):
            ys.append(None)
            continue
        if xv == 0.0:
            ys.append(1548.92)
        elif xv < 0:
            ys.append(9.8 if abs(xv) < B else 8.8)
        else:
            ys.append(-11.4 if abs(xv) < B else -12.4)
    return {"y": ys}
