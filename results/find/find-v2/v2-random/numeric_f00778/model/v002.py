def predict(probe):
    # f(x) ≈ a*x^3 with a ≈ -3.9e-3, but the scale is ~1000x larger than v1 assumed [E4-E16]
    # Check: x=93.5 -> -3189421; 93.5^3=817400, ratio -3.902e-3. x=127 -> -7991663; 127^3=2048383, ratio -3.901e-3 [E10]
    # So a ≈ -3.9e-3, pure cubic, no linear term needed [E4-E16]
    # Small-x values: x=0.9 -> 3.4625; 0.9^3=0.729, ratio 4.75e-3 (noisy/small) [E15]
    # x=2.0 -> -26.0762; 8*3.9e-3=0.0312... too small. Hmm, x=2 gives -26, so not pure cubic at small x?
    # x=-1.6 -> 13.9787; 1.6^3=4.096, ratio 3.41e-3. x=2.0 -> -26.0762; 8, ratio 3.26e-3. Close enough to cubic.
    # x=-6.0 -> 826.575; 216*3.9e-3=0.842... but observed 826.6, ratio 3.83. So scale ~1000x: a≈-3.9
    # Wait: 826.575/216 = 3.827. And 3189421/817400 = 3.902. So a≈-3.9 (not -3.9e-3)!
    # Recheck x=0.9: 0.9^3=0.729, 3.9*0.729=2.84, observed 3.46. x=2: 8*3.9=31.2, observed 26.08. OK cubic a≈-3.9.
    # x=-1.6: 4.096*3.9=15.97, observed 13.98. Reasonable.
    a = -3.9
    out = []
    for x in probe["x"]:
        try:
            out.append(a * x**3)
        except Exception:
            out.append(None)
    return {"y": out}
