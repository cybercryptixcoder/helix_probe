def predict(probe):
    # Region A: x < -9.375 -> y ≈ 8 (constant, small noise) [E2, E4, E6]
    # Region B: x >= -9.375 -> y = 8 - 9.6*x [E1..E6]
    # Boundary: E6 shows -9.4 -> ~8, -9.375 -> 98.0 (=8-9.6*-9.375). Sharp threshold at -9.375.
    out = []
    for x in probe["x"]:
        if x < -9.375:
            out.append(8.0)
        else:
            out.append(8.0 - 9.6 * x)
    return {"y": out}
