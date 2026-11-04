import math

def predict(probe):
    # Beliefs (revised after E14):
    # - High-frequency jitter is real and very fast: values change substantially over
    #   0.05 spacing [E14, E12, E10, E8, E6]. Period < 0.1, so freq > 60 rad/unit.
    # - There IS a slow trend: negative around x=-40..-20, positive around x=0..60
    #   [E14 local means -1.4 vs +1.0; E10 x=-20 mean -0.84 vs x=20 mean +1.1].
    # - Roughly linear rise with a small bump near x~5 [E8, E6 means ~1.2-1.4].
    # - Jitter amplitude ~1.0-1.2; total output range ~[-3, 5] [all].
    # - Exact values unpredictable (fast jitter phase unknown); predict local mean
    #   plus a modest deterministic jitter to capture some structure.
    xs = probe["x"]
    out = []
    for x in xs:
        slow = 0.02 * x - 0.3 + 1.2 * math.exp(-((x - 5.0) / 15.0) ** 2)
        j = (0.6 * math.sin(60.0 * x + 1.0)
             + 0.4 * math.sin(97.0 * x + 2.0))
        out.append(slow + j)
    return {"y": out}
