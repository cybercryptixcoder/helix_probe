import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs:
    # 1. For |x| > ~90 the output is tiny (near 0.005-0.01), almost independent of x
    #    [E5 x=-127.7 -> 0.0046; E6 x=-107.4 -> 0.0055; E13 x=-122.5 -> 0.0048;
    #     E15 x=-117.9 -> 0.0050; E22 x=127.9 -> 0.1497 is an outlier? no wait...]
    #    Actually check: large |x| gives ~0.005 consistently on the negative side
    #    (E5 -127.7:0.0046, E6 -107.4:0.0055, E13 -122.5:0.0048, E15 -117.9:0.0050,
    #     E22 -106.6:0.0055, E23 -103.0:0.0057). On the positive side large x gives
    #    varied values (E10 127.0:-0.244, E22 127.9:0.1497, E2 123.6:-0.0946).
    #    Hmm, so positive large x is NOT tiny. Let me reconsider.
    #
    # 2. The output looks like a sum of a smooth oscillatory term and a small
    #    noise/floor term. The floor is about 0.005 magnitude.
    #
    # 3. Looking at mid-range x, output magnitude is up to ~0.3-0.4.
    #    E15 x=0.9 -> -0.3708 is the largest magnitude seen.
    #    E3 x=58.8 -> -0.3169.
    #
    # 4. There's clearly a periodic/oscillatory component. Values near x=0:
    #    E21 x=-1.4 -> -0.0524, x=-3.3 -> -0.0104, x=2.2 -> -0.0651 (E17),
    #    x=0.9 -> -0.3708 (E15), x=2.0 -> -0.0406 (E6), x=2.9 -> 0.0671 (E1).
    #    Very sensitive to x near 0 -> high frequency oscillation.
    #
    # 5. The tiny ~0.005 floor appears for large |x| on the negative side and
    #    sometimes positive. This looks like a "decay" region: for |x| beyond
    #    some threshold the main term is damped, leaving only a small residual.
    #    Threshold appears around |x| ~ 90-100.
    #
    # Best guess: f(x) = A(x) * sin(w*x + phi) + floor, where A(x) decays
    # outside a central band, and floor is a small constant with sign.
    #
    # Given the difficulty, I'll model the dominant behavior:
    # - A high-frequency sinusoid with amplitude ~0.2 in the central region
    # - Damping to ~0.005 for |x| > ~95
    #
    # Let me estimate frequency. Near x=0 consecutive probes:
    #   x=0.9 -> -0.3708, x=2.0 -> -0.0406, x=2.2 -> -0.0651, x=2.9 -> 0.0671
    #   x=-1.4 -> -0.0524, x=-3.3 -> -0.0104
    # Sign changes suggest period ~ 4-6 units, so w ~ 1.0-1.5.
    #
    # Amplitude: max |y| ~ 0.37. Let's use A ~ 0.2 central, decaying.
    #
    # This is a rough model. I'll produce a sinusoid-based prediction.

    def f(x):
        try:
            x = float(x)
        except Exception:
            return None
        if math.isnan(x) or math.isinf(x):
            return None

        # Central oscillatory term with amplitude envelope.
        # Envelope: peaks near x~0, decays for large |x|.
        # Use a Gaussian-ish envelope with width ~ 90.
        # Damping region: |x| > 95 -> amplitude ~ 0.005
        ax = abs(x)
        if ax > 95.0:
            # residual floor, small magnitude, sign varies
            # Use a tiny sinusoid to give variation
            return 0.005 * math.sin(0.7 * x)

        # amplitude envelope
        amp = 0.22 * math.exp(-(x * x) / (2 * 70.0 * 70.0))
        # high frequency oscillation, period ~ 5
        w = 1.25
        phi = 0.0
        val = amp * math.sin(w * x + phi)
        return val
    try:
        xs = probe.get("x", [])
        ys = [f(v) for v in xs]
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", [])) if isinstance(probe, dict) else []}
