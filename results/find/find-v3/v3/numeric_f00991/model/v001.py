def predict(probe):
    # y = 4.1*x + 12.3*|x| - 2.5*sign(x), with sign(0)=0 [E1]
    # Equivalently: x>0 -> 16.4x - 2.5 ; x<0 -> -8.2x + 2.5 ; x=0 -> 0 [E1]
    out = []
    for x in probe["x"]:
        s = (x > 0) - (x < 0)
        out.append(4.1 * x + 12.3 * abs(x) - 2.5 * s)
    return {"y": out}
