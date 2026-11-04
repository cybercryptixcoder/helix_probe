def predict(probe):
    # Piecewise linear: x<0 -> 2.4x+11.7; x>0 -> 2.4x+1.8 [E1]
    # At x=0: y=-228.87, a special value (not on either line) [E2]
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(round(2.4*x + 11.7, 4))
        elif x > 0:
            out.append(round(2.4*x + 1.8, 4))
        else:
            out.append(-228.87)
    return {"y": out}
