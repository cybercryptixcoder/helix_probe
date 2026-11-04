import math

def predict(probe):
    # Beliefs:
    # - Output is 1.0 on an interval, 0.0 elsewhere [E1-E9]
    # - Upper edge: 1.0 at x=1.5, 0.0 at x=1.52 [E8]; so upper bound ~1.5 (inclusive-ish)
    # - Lower edge: 0.0 at x=-1.6 [E9], 1.0 at x=-1.5 [E4]; so lower bound ~-1.5
    # - E2 shows -2 -> 0.0, -1 -> 1.0; consistent with lower bound between -2 and -1 (likely -1.5)
    # - E2 shows 1 -> 1.0, 2 -> 0.0; consistent with upper bound ~1.5
    # - E4: -1.5 -> 1.0, 1.5 -> 1.0; consistent
    # - E6: 1.4 -> 1.0, 1.55 -> 0.0; consistent with upper ~1.5
    # - E8: 1.5 -> 1.0, 1.52 -> 0.0; upper bound in (1.5, 1.52]
    # - E9: -1.6 -> 0.0; lower bound in (-1.6, -1.5]
    # Model: 1.0 if -1.5 <= x <= 1.5, else 0.0
    result = []
    for x in probe["x"]:
        if x is None:
            result.append(None)
        else:
            if -1.5 <= x <= 1.5:
                result.append(1.0)
            else:
                result.append(0.0)
    return {"y": result}
