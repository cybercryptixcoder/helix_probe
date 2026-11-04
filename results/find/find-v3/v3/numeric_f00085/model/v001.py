def predict(probe):
    # Observations [E1]:
    # - Large |x| gives large positive y, roughly ~ x^2 scaled (88.2 -> 27090, 66 -> 15014)
    # - Small |x| (2.9, -6.0) gives ~ -22.8, a constant negative floor
    # - Negative moderate x (-20.3, -24.3, 21.3) gives ~1500-2150, positive
    # - -61.7 -> 13550, -50.4 -> 9077: increasing with |x|
    # Hypothesis: y ~ a*x^2 + b, with a small negative offset near x=0.
    # Fit: 88.2^2=7779.24 -> 27090.78 => a~3.482; 66^2=4356 -> 15014.02 => a~3.447
    # 61.7^2=3806.89 -> 13550.62 => a~3.560; 50.4^2=2540.16 -> 9077.30 => a~3.573
    # 20.3^2=412.09 -> 1545.22 => a~3.75; 24.3^2=590.49 -> 2154.09 => a~3.648
    # 21.3^2=453.69 -> 1532.72 => a~3.378
    # Not a clean constant a; likely an MLP approximating something like x^2 with offset.
    # Best simple guess: y = 3.5*x^2 - 22.8 for all x (floor at -22.8 near 0).
    # But small x gives exactly -22.8021 for both 2.9 and -6.0 -> looks like a flat region.
    # Try: y = max(3.5*x^2 - 22.8, -22.8)? For x=2.9: 3.5*8.41-22.8=6.6, not -22.8.
    # So near 0 it's flat at -22.8. Threshold: |x| where 3.5x^2-22.8 crosses -22.8 is 0.
    # Actually maybe y = 3.5*x^2 - 22.8 only for |x|>some threshold, else -22.8.
    # x=2.9 -> -22.8, x=6.0 -> -22.8, x=20.3 -> 1545. 3.5*20.3^2-22.8=1419, close-ish.
    # Let's use a piecewise: |x| < ~10 -> -22.8, else 3.5*x^2 - 22.8.
    # Refine a using larger points: avg of 3.482,3.447,3.560,3.573 ~ 3.515.
    a = 3.52
    out = []
    for x in probe["x"]:
        if abs(x) < 10:
            out.append(-22.8021)
        else:
            out.append(a * x * x - 22.8021)
    return {"y": out}
