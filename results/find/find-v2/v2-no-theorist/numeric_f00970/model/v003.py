import math

def predict(probe):
    # Beliefs:
    # - Large-value region on positive side: x in [~0.2, ~3.0], y ~ 10-13 [E2, E4].
    # - Large-value region on negative side: x in [~-3.0, ~-0.5], y ~ 10-13 [E4, E6].
    #   E6 shows -0.5 already large (10.05), -3.0 large (10.08), -3.1 small.
    # - Both bumps are smooth, peaked near |x|~2, ~13 at center, ~10 at edges [E6].
    # - Outside bumps, y is small noisy |y| < ~3.5 [E1, E2, E3, E5].
    # - No pole/divergence; values bounded [E2, E4, E6].
    # - Outside-bump values look random-ish; use small pseudo-random-ish value.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if 0.2 <= ax <= 3.0:
                # smooth bump peaked near |x|=2, ~13 center, ~10 at edges
                # Gaussian-ish: 13 - 3*((ax-2)/1.0)^2 clipped
                d = (ax - 2.0)
                val = 13.0 - 2.5 * d * d
                if val < 9.5:
                    val = 9.5
                out.append(val)
            else:
                # small noisy tail; decaying oscillation placeholder
                out.append(1.5 * math.sin(x) / (1.0 + ax))
        except Exception:
            out.append(None)
    return {"y": out}
