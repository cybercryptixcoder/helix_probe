def predict(probe):
    # f(x) = 1 when |x| is in a band around 0, else 0 [E2, E3, E4, E5, E6, E7]
    # Symmetric about 0 [E4, E6, E8]
    # Upper boundary: 1 at 1.850, 0 at 1.851 -> threshold ~1.8505 [E8, E10]
    # Lower boundary: 1 at -1.850, 0 at -1.851 -> threshold ~-1.8505 [E8, E10]
    # So nonzero for |x| <= ~1.850 [E8, E10]
    def f(x):
        return 1.0 if abs(x) <= 1.8505 else 0.0
    return {"y": [f(x) for x in probe["x"]]}
