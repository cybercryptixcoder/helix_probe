def predict(probe):
    # Main behavior: y = a*x^3 + c*x (pure odd cubic) for |x| >= ~1.5 [E1,E2,E3,E4,E5]
    # Fit: a ~ -3.9007, c ~ -10.47 from large points; small x shows extra structure
    # For |x| < 1.5: outputs are ~2-6, roughly constant-ish with noise, NOT following cubic [E6]
    # E6 shows values around 3.3 at x=0, varying 1.4-6.1 for |x|<1.3, no clear odd symmetry
    # E4: x=0.1->4.46, -0.1->4.49, 0.5->2.58, -0.5->1.51, 0.9->1.59, -0.9->5.38
    #   these are noisy around ~3, not cubic (cubic would give ~-1 to -9)
    # So: |x| < 1.5 region behaves like ~constant + noise (mean ~3.3)
    # Outside: pure odd cubic. Transition around |x|=1.5 [E4: x=1.5->-8.52 matches cubic]
    import math
    a = -3.9007
    c = -10.47
    out = []
    for x in probe["x"]:
        if abs(x) < 1.5:
            # small-magnitude region: roughly constant ~3.3 with noise [E6]
            # best guess: mean offset, deterministic prediction
            out.append(3.3)
        else:
            out.append(a*x**3 + c*x)
    return {"y": out}
