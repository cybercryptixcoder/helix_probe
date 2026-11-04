def predict(probe):
    # Two-valued step function: outputs 52.2 or -14.96 [E1]
    # Sign rule: positive x -> 52.2, negative x -> -14.96 [E1]
    # (2.9, 21.3, 66.0, 72.7, 88.2 positive -> 52.2; negatives -> -14.96) [E1]
    # Zero/undefined behavior unknown; guess x>=0 -> 52.2 [?]
    out = []
    for x in probe["x"]:
        try:
            out.append(52.2 if x >= 0 else -14.96)
        except Exception:
            out.append(None)
    return {"y": out}
