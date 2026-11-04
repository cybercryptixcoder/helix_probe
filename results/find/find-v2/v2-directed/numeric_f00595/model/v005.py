import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs (evidence):
    # - For x < 0: f(x) = floor(x) - 1  [E1, E2, E3, E4, E5]
    #   e.g. x=-1 -> -2, x=-0.5 -> -2, x=-2.5 -> -4, x=-128 -> -129
    # - For x >= 0: f(x) = floor(x) + 1  [E1, E2, E3, E4, E5]
    #   e.g. x=0 -> 1, x=0.5 -> 1, x=1 -> 2, x=128 -> 129
    #   (Note: floor at exact integers; x=1 -> 2, x=2 -> 3, x=32 -> 33)
    # - Exception region: x in (33.4, 35.0] (approximately) gives a
    #   different, noisy-looking value near -0.3 to -0.7  [E6]
    #   E6: 33.4 -> -0.365, 33.49 -> -0.7087, 33.5 -> -0.3402,
    #       33.51 -> -0.3417, 33.6 -> -0.3255, 33.75 -> -0.3244,
    #       33.9 -> -0.4361, 33.99 -> -0.4528, 34.0 -> -0.5581,
    #       34.01 -> -0.5372, 34.1 -> -0.4911, 34.5 -> -0.3262,
    #       35.0 -> -0.3767
    #   Values at/below 33.25 follow the normal rule (33.25 -> 34).
    #   The exact left boundary is between 33.25 and 33.4; best guess 33.3.
    #   The right boundary: 35.0 is still in the region; unknown beyond.
    #   We model it as a noisy value; best guess: mean ~ -0.4 with noise.
    #   Since outputs are deterministic-ish but irregular, we approximate
    #   with a smooth-ish function. Use a fixed pseudo-random-ish value
    #   near -0.4 based on x to mimic the scatter (?).
    #
    # - E5 anomaly: x=33.5 -> -0.4681 (consistent with exception region),
    #   x=64.5 -> 65.0 (normal rule), x=127.5 -> 128.0 (normal rule).
    #   So exception region is localized around x ~ 33.4 to 35.0.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Exception region (noisy values) [E6]
        # Left boundary guessed at 33.3 (between 33.25 and 33.4)
        # Right boundary guessed at 35.0 inclusive (35.0 is in region)
        if 33.3 < x <= 35.0:
            # Approximate the noisy outputs near -0.4.
            # Use a deterministic pseudo-noise based on x.
            # Best guess: values scatter roughly -0.3 to -0.7.
            # A simple model: -0.4 + 0.15*sin(100*x) (?) — just to
            # produce plausible irregular values.
            val = -0.4 + 0.15 * math.sin(97.0 * x) + 0.05 * math.cos(53.0 * x)
            ys.append(round(val, 4))
            continue

        # Normal rule
        fl = math.floor(x)
        if x < 0:
            ys.append(float(fl - 1))
        else:
            ys.append(float(fl + 1))

    return {"y": ys}
