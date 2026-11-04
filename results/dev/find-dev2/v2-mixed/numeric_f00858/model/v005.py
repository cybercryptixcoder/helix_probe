def predict(probe):
    # f(x) = 1 when |x| is in a band around 0, else 0 [E2, E3, E4, E5, E6, E7]
    # Symmetric about 0 [E4, E6, E8]
    # Upper boundary: 1 at 1.85, 0 at 1.86 -> threshold ~1.855 [E6, E8]
    # Lower boundary: 1 at -1.85, 0 at -1.86 -> threshold ~-1.855 [E6, E8]
    # So nonzero for |x| < ~1.855 [E6, E8]
    def f(x):
        return 1.0 if abs(x) < 1.855 else 0.0
    return {"y": [f(x) for x in probe["x"]]}
