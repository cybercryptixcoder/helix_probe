import math

def predict(probe):
    # Observations:
    # - The box is NOISY: same x gives different y across experiments
    #   (x=1.5: E4->3.23, E6->1.61; x=0: E2->0.87, E4->-0.43, E6->0.46) [E2,E4,E6].
    # - Signal is essentially a sign step: negatives ~-1.4, positives ~+1.0..1.3 [E2,E5,E7].
    # - Pooled means: negatives ~-1.4, positives ~+1.2 (E1 high, E2/E7 lower) [E1,E2,E5,E7].
    # - Transition near x=0; E2 shows x=0 already positive, x<0 negative [E2].
    # - Noise std ~1, so predict the conditional mean: smooth step centered ~0 [all].
    # ? Best guess: y = -0.1 + 1.4*tanh(x/3) + noise. Predict the mean.
    out = []
    for x in probe.get("x", []):
        try:
            v = -0.1 + 1.4 * math.tanh(x / 3.0)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}
