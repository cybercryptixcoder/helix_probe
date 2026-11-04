def predict(probe):
    # For x<0: y = -35.72*x - 17.1 [E1, E2] (linear, matches all negatives)
    # For x>0: y = -404.2*x - 154.8 [E1, E2] (linear, matches all positives)
    # At x=0: y = -5401.17 [E2] -- a spike/different value at exactly zero
    result = []
    for x in probe["x"]:
        if x > 0:
            y = -404.2*x - 154.8
        elif x < 0:
            y = -35.72*x - 17.1
        else:
            y = -5401.17
        result.append(y)
    return {"y": result}
