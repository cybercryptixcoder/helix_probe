import math

def predict(probe):
    # Model of the black box f(x):
    # Regions determined by floor(x):
    #   floor(x) <= -6  ->  y = -0.7 * floor(x)   [E1,E2,E3,E5,E7,E8,E9]
    #   -5 <= floor(x) <= 18 -> y ≈ -402.37 (noisy constant)  [E4,E6,E8]
    #   floor(x) >= 19 -> y = -16.8 * floor(x)   [E1,E3,E5,E6,E9,E10]
    # E10 shows the positive transition is at x=18.9 already linear (-302.4),
    # i.e. the boundary is x >= 18.9, not floor(x)>=19. Check: 18.9 -> -302.4.
    # -16.8*18 = -302.4, so the linear rule uses floor(x) but starts when x>=18.9?
    # Actually -302.4 = -16.8*18, so at x=18.9 floor=18 gives -302.4.
    # So the linear regime begins at x >= 18.9 (not floor>=19). Plateau holds below 18.9.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            fx = math.floor(x)
        except Exception:
            ys.append(None)
            continue
        if fx <= -6:
            ys.append(-0.7 * fx)
        elif x >= 18.9:
            # linear regime; uses floor(x)
            ys.append(-16.8 * fx)
        else:
            ys.append(-402.37)
    return {"y": ys}
