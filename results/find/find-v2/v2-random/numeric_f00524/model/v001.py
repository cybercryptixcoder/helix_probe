def predict(probe):
    # Only one data point: f(2.9)=3.0, all other tested x give 0.0 [E1]
    # Hypothesis (?): f(x) = round(x) only near a small region around x=3,
    #   else 0. But with one nonzero sample we can't pin the region.
    # Simplest guess (?): f(x) = round(x) if |x-3| < 1 else 0.
    # This is a placeholder pending more experiments.
    out = []
    for x in probe["x"]:
        if abs(x - 3.0) < 1.0:
            out.append(float(round(x)))
        else:
            out.append(0.0)
    return {"y": out}
