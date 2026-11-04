import math

def predict(probe):
    # f(x) = sign-dependent mean + large noise (~1 std) [E10: no local smoothness;
    #   E4: no periodicity; E12/E14: no magnitude trend within a sign]
    # Positive x mean ~1.4, negative x mean ~-1.0, x=0 ~0.7 [E1-E14 averages]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(1.4)
        elif x < 0:
            out.append(-1.0)
        else:
            out.append(0.7)
    return {"y": out}
