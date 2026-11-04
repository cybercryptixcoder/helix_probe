def predict(probe):
    # Output takes one of two values depending on sign of x [E1]
    # Positive x -> 52.2, negative x -> -14.96 [E1]
    # (zero case unknown; guess positive branch)
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(52.2)
        else:
            out.append(-14.96)
    return {"y": out}
