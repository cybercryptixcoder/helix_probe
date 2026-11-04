def predict(probe):
    # Region A: x < -9.5 (approx): y ≈ 8 (constant, small noise) [E2: -25..-10 all ~8; E4: -9.9,-9.75,-9.5 ~8]
    # Region B: x >= -9.5: y = 8 - 9.6*x [E1, E2, E3, E4 all exact]
    # Boundary: E4 shows -9.5->~8, -9.25->96.8 (=8-9.6*-9.25). So threshold between -9.5 and -9.25.
    #   Pick -9.5 as cutoff: x <= -9.5 -> 8, else linear. (boundary in (-9.5,-9.25], guess -9.5)
    out = []
    for x in probe["x"]:
        if x <= -9.5:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}
