import math

def predict(probe):
    # f(x) = sign-based level + large noise (~1 std) [E10: no local smoothness;
    #   E4: no periodicity; E12: same sign, wildly varying values]
    # Empirical means: positive x -> ~1.4, negative x -> ~-0.85, x=0 -> ~0.7
    #   [averaged over E1-E12]
    # No magnitude dependence [E12: x=0.5 and x=120 both ~1.5]
    # No dependence on fractional part [E10: x and x+0.1 differ by ~1]
    out = []
    for x in probe["x"]:
        if x > 0:
            out.append(1.4)
        elif x < 0:
            out.append(-0.85)
        else:
            out.append(0.7)
    return {"y": out}
