def predict(probe):
    # y = 2.4x + 1.8 for x >= 0 [E1, E2]
    # y = 2.4x + 11.7 for x < 0 [E1, E2]
    # Exception: x == 0 gives -228.87, not 1.8 [E2]
    #   (a spike/dip at exactly 0; neighbors 0.1? unknown, only x=0 tested)
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(-228.87)
        elif x < 0:
            out.append(2.4 * x + 11.7)
        else:
            out.append(2.4 * x + 1.8)
    return {"y": out}
