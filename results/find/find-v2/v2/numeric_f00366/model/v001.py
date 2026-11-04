def predict(probe):
    # Output takes only two values: 8.8 or -12.4 [E1]
    # Sign of x decides: x<0 -> 8.8, x>0 -> -12.4 [E1]
    # Exception: x=2.9 gave -11.4, not -12.4 [E1] (near-zero region differs?)
    # ? Boundary of exception unknown; guess small |x| region gives -11.4
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(8.8)
        elif abs(x) < 5:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}
