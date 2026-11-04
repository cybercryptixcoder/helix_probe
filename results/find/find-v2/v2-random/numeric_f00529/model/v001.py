def predict(probe):
    # Outputs cluster near -6.9 or -7.9, with occasional precise values like -6.9015 [E1]
    # Pattern: sign of x seems to select the value [E1]
    #   positive x -> -6.9 ; negative x -> -7.9 (roughly)
    # But x=2.9 gave -6.9015 (a near -6.9 but slightly off) [E1]
    # x=-6.0 gave -7.9, x=-20.3 gave -7.9, x=-24.3 gave -7.9, x=-50.4 gave -7.9, x=-61.7 gave -7.9 [E1]
    # x=21.3, 66.0, 72.7, 88.2 gave -6.9 [E1]
    # Hypothesis (?): y = -7.9 if x < 0 else -6.9, but small |x| gives a perturbed value
    # The 2.9 case (-6.9015) suggests a small correction near zero, maybe -6.9 - something*exp(-|x|) or similar.
    # Without more data, guess: y = -7.9 for x<0, -6.9 for x>=0, with a tiny perturbation for small positive x.
    # ?: perturbation only observed at x=2.9; could be noise or a real near-zero effect.
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                out.append(-7.9)
            else:
                # small positive x gets a slight offset; larger x -> -6.9
                if x < 5:
                    out.append(-6.9015)
                else:
                    out.append(-6.9)
        except Exception:
            out.append(None)
    return {"y": out}
