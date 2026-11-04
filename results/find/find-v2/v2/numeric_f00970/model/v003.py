import math

def predict(probe):
    # Inside |x| < ~3.0: output ~12 (mean ~11.5) [E2,E4,E6]
    # Outside |x| > ~3.0: output is noise-like, roughly in [-2, 2], not ~0 [E1,E3,E5,E7]
    # Boundary: plateau ends between 2.9 (high) and 3.1 (low) on positive side [E6]
    #   and between -2.9 (high) and -3.1 (low) on negative side [E6]
    # So threshold ~3.0, symmetric [E4,E6]
    # Outside values look like noise with std ~1, mean ~0; can't predict exactly [E1,E3,E5,E7]
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif abs(x) < 3.0:
            out.append(11.5)
        else:
            out.append(0.0)
    return {"y": out}
