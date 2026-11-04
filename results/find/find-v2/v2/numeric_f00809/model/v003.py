import math

def predict(probe):
    # Observations / beliefs:
    # - Outputs are bounded roughly in [-0.25, 0.25] [E1-E5].
    # - Values look irregular/noisy; no clean single sinusoid fits [E2, E4].
    # - Dense sweeps over x in [-60,65] show rapid irregular variation, not a smooth low-freq wave [E2, E4].
    # - Adjacent x values (5 apart) give wildly different outputs -> high-frequency content or noise [E2, E4].
    # - No clear piecewise region change visible; large |x| outputs still small [E3, E5].
    # - Best guess: a high-frequency oscillation (period ~ a few units) with amplitude ~0.15,
    #   plus noise-like jitter. The exact form is unknown ("?").
    #
    # Model: y = 0.15 * sin(x * k + phi) with k chosen to give rapid variation,
    # plus a small secondary term. Since we can't identify the true period, use a
    # pseudo-random-looking but deterministic high-frequency combination.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # high-frequency oscillation (period ~ 2*pi/1.3 ~ 4.8) plus ripple
            y = 0.15 * math.sin(1.3 * x + 0.7)
            y += 0.06 * math.sin(2.7 * x + 1.1)
            y += 0.03 * math.sin(5.1 * x)
            # clamp to observed range
            if y > 0.25:
                y = 0.25
            if y < -0.25:
                y = -0.25
            ys.append(round(y, 4))
        except Exception:
            ys.append(None)
    return {"y": ys}
