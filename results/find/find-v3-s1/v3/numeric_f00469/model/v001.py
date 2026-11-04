def predict(probe):
    # Only one data point: f(-1.2)=1, all others (far from 0) = 0 [E1]
    # Hypothesis: f(x)=1 only in a small interval around 0, else 0.
    # Boundaries unknown; guess a narrow band around 0. [?]
    out = []
    for x in probe["x"]:
        out.append(1.0 if abs(x) < 2.0 else 0.0)
    return {"y": out}
