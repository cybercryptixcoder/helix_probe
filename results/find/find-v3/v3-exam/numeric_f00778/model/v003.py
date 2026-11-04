def predict(probe):
    # Main behavior: y = a*x^3 + c*x (pure odd cubic) for |x| >= ~1.5 [E1,E2,E3,E4,E5,E7]
    # Fit: a ~ -3.9007, c ~ -10.47 from large points
    # For |x| < 1.5: outputs scatter around ~3.3 with substantial noise [E6,E8]
    # E8 shows no deterministic asymmetry: x,-x pairs are unrelated (e.g. 0.02->2.32, -0.02->2.33; 0.15->3.88, -0.15->1.77)
    # E6 also shows scatter 1.4-6.1 with no sign pattern
    # So small region is a noisy plateau ~3.3; best deterministic guess is the mean
    a = -3.9007
    c = -10.47
    out = []
    for x in probe["x"]:
        if abs(x) < 1.5:
            out.append(3.3)
        else:
            out.append(a*x**3 + c*x)
    return {"y": out}
