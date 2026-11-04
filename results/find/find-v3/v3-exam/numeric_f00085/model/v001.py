def predict(probe):
    # Observations from E1:
    # f(88.2)=27090.784, f(66.0)=15014.0187, f(-20.3)=1545.2188,
    # f(-61.7)=13550.6196, f(2.9)=-22.8021, f(-24.3)=2154.0941,
    # f(72.7)=18241.8226, f(-50.4)=9077.3007, f(-6.0)=-22.8021,
    # f(21.3)=1532.7222
    #
    # Pattern: y ≈ x^2 * k for large |x|, but small |x| gives ~ -22.8.
    # Check: 88.2^2 = 7779.24; 27090.784/7779.24 ≈ 3.482
    #        66^2 = 4356; 15014.0187/4356 ≈ 3.447
    #        72.7^2 = 5285.29; 18241.8226/5285.29 ≈ 3.451
    #        61.7^2 = 3806.89; 13550.6196/3806.89 ≈ 3.559
    #        50.4^2 = 2540.16; 9077.3007/2540.16 ≈ 3.573
    #        20.3^2 = 412.09; 1545.2188/412.09 ≈ 3.750
    #        24.3^2 = 590.49; 2154.0941/590.49 ≈ 3.648
    #        21.3^2 = 453.69; 1532.7222/453.69 ≈ 3.378
    # Small |x| (2.9, -6.0) gives -22.8021 — looks like a floor/offset.
    # Hypothesis: y = max(x^2 * a, b) with a≈3.5, b≈-22.8? But b is negative,
    # so max wouldn't give -22.8 for small x. Maybe y = x^2*3.5 - 22.8 for small,
    # but large x gives ~3.5x^2 not 3.5x^2-22.8.
    # Actually: for x=2.9, 3.5*8.41=29.4, minus 22.8 = 6.6, not -22.8.
    # Try: y = relu-like? -22.8 for |x| small suggests a constant region.
    # Check x=21.3: 3.5*453.69=1588, observed 1532.7. Close-ish.
    # x=20.3: 3.5*412=1442, observed 1545. Hmm.
    # Best guess: y ≈ 3.5*x^2 - 22.8 for |x| above threshold, and -22.8 below.
    # Threshold between 6 and 20.3. Let's say |x| < ~10 -> -22.8.
    # Refine: 3.5*x^2 - 22.8: x=88.2 -> 27204 (obs 27090, ok)
    #   x=66 -> 15246 (obs 15014, ok)
    #   x=72.7 -> 18498 (obs 18241, ok)
    #   x=61.7 -> 13304 (obs 13550, ok)
    #   x=50.4 -> 8869 (obs 9077, ok)
    #   x=24.3 -> 2043 (obs 2154, ok)
    #   x=21.3 -> 1565 (obs 1532, ok)
    #   x=20.3 -> 1419 (obs 1545, hmm)
    # So y = 3.5*x^2 - 22.8 works reasonably for |x| >= ~20.
    # For small |x|, y = -22.8 (constant). Threshold somewhere in (6, 20.3).
    # Use threshold 10 as guess (?).
    out = []
    for x in probe["x"]:
        if abs(x) < 10:
            out.append(-22.8021)
        else:
            out.append(3.5 * x * x - 22.8021)
    return {"y": out}
