import math

def predict(probe):
    # Observations / beliefs:
    # - Outputs are small, roughly in [-0.25, 0.25], look like a smooth-ish function of x [E1-E3].
    # - No obvious piecewise jump visible in the data; values vary irregularly with x [E1-E3].
    # - Magnitudes look like a product of a bounded oscillation and a slowly varying envelope.
    # - Best simple guess: y = A * sin(x / P + phi) * something, but data look noisy.
    # - Try a smooth low-frequency sinusoid plus small higher-frequency term; fit roughly to evidence.
    #
    # Since we cannot fit exactly, use a plausible mechanism:
    #   y = 0.12 * sin(x/7 + 0.5) * cos(x/23) + 0.03 * sin(x/3.1)
    # This is a guess ("?") but captures bounded, irregular-looking oscillation.
    #
    # ? There may be a special interval (e.g., |x|>100) where behaviour changes;
    #   E3 has x near 104-124 with outputs still small, so no clear change. Keep uniform.

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # main oscillation with slowly varying envelope
            y = 0.12 * math.sin(x / 7.0 + 0.5) * math.cos(x / 23.0)
            # small higher-frequency ripple
            y += 0.03 * math.sin(x / 3.1)
            # slight damping at large |x| (?)
            if abs(x) > 100:
                y *= 0.9
            ys.append(round(y, 4))
        except Exception:
            ys.append(None)
    return {"y": ys}
