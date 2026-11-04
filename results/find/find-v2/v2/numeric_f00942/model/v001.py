def predict(probe):
    # Piecewise linear: for x>0, y = -404.2*x - 154.8 [E1]
    # For x<0, y = -35.72*x - 17.1 [E1]
    # Boundary at x=0; use positive formula at 0 (?)
    result = []
    for x in probe["x"]:
        if x > 0:
            y = -404.2*x - 154.8
        elif x < 0:
            y = -35.72*x - 17.1
        else:
            y = -154.8  # ? guess
        result.append(y)
    return {"y": result}
