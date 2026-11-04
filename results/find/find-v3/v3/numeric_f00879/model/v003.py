import math

def predict(probe):
    # Beliefs (revised after E8-E12):
    # - The rapid oscillation is GLOBAL, not confined to a band near 0 [E10, E12].
    #   E10 shows wiggles at x~20 and x~-20; E12 shows wiggles at x~40.
    # - The oscillation is not a clean sinusoid: it looks like a fast, somewhat
    #   irregular jitter with amplitude ~1-1.5 and no fixed simple period [E6,E8,E10,E12].
    # - There is a slow trend: roughly y increases with x, from ~-0.5 at x=-128
    #   to ~+1 at x=+128, but with substantial scatter [E2,E4,E5,E7,E9,E11].
    # - The "special interval" idea is wrong: no narrow band; behavior is similar
    #   everywhere, just noisy/oscillatory [E10,E12].
    # - Outputs are bounded roughly in [-3, 4] [all].
    # Model: y = slow(x) + fast_jitter(x) + noise.
    #   slow(x) = a*x + b, a~0.006, b~0.3
    #   fast_jitter: a sum of a couple of incommensurate sines to mimic irregular
    #   high-frequency wiggle, amplitude ~1.2, with a deterministic phase.
    # Since exact values are unpredictable (noise), aim for the right distribution.

    xs = probe["x"]
    out = []
    for x in xs:
        slow = 0.006 * x + 0.3
        # irregular fast jitter: combine two sines with different frequencies
        j = (0.9 * math.sin(7.3 * x + 1.1)
             + 0.6 * math.sin(11.7 * x + 2.3)
             + 0.4 * math.sin(3.1 * x + 0.7))
        out.append(slow + j)
    return {"y": out}
