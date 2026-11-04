import math

def predict(probe):
    # Observations:
    # - The box is NOISY: same x gives different y across experiments
    #   (x=1.5: E4->3.23, E6->1.61; x=3.5: E4->1.57, E6->-0.07) [E4,E6].
    # - So the "rapid oscillation" in E4 is mostly noise, not signal [E4,E6].
    # - Underlying signal is a smooth ramp: low (~-1.5) for x<0, high (~+1.0) for x>0 [E2].
    # - E2 means: negatives ~-1.49, positives ~+0.98 -> center ~-0.25, amplitude ~1.25 [E2].
    # - Transition is near x=0, fairly gradual (E2: -5->-1.14, 0->0.87) [E2].
    # - No period-1 structure (E6 fractional parts disagree) [E6].
    # ? Best guess: y = -0.25 + 1.3*tanh(x/5) + noise. Predict the mean.
    out = []
    for x in probe.get("x", []):
        try:
            v = -0.25 + 1.3 * math.tanh(x / 5.0)
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}
