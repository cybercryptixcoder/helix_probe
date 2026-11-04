def predict(probe):
    # Output takes only two values: -12.4 or 8.8 [E1]
    # Sign of x determines value: x>0 -> -12.4, x<0 -> 8.8 [E1]
    # Exception: x=2.9 gives -11.4, not -12.4 [E1] (a special region near small positive x?)
    # ? The 2.9 case is odd; maybe a narrow interval, but only one point seen.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x > 0:
            out.append(-12.4)
        else:
            out.append(8.8)
    return {"y": out}
