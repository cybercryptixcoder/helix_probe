import math

def predict(probe):
    # f(x) ≈ 16.8*|x| for |x| >= ~1 [E1,E2,E3,E4,E5,E7,E9,E11,E13]
    # For small |x| (<~1), there is substantial noise/irregularity [E6,E8,E10,E12,E14]
    #   E14: +x and -x give DIFFERENT values at same |x| -> not a deterministic even function
    #   E12/E14: residuals are irregular, not smooth -> noise dominates at small |x|
    #   E8: at |x|=0.001, y ranges -0.14..1.81 -> noise amplitude ~1-2
    #   E6: at x=0, y=-0.15; at 0.001, y=0.6/0.07 -> noise
    # Best guess: y = 16.8*|x| + noise, noise ~ N(0, sigma) with sigma ~1.5 at small |x|,
    #   shrinking relative to signal as |x| grows (ordinary probes match to ~0.1%)
    # Since noise is unpredictable, predict the mean: 16.8*|x|. But small-|x| probes
    #   are scored on match, and mean prediction is poor there. Use 16.8*|x| + small
    #   positive bias? E14 positives average ~2.4 at |x|~0.08 (16.8*0.08=1.34), 
    #   negatives average ~1.3. E12 positives similar. Suggests slight positive offset ~0.5-1.
    #   E6 x=0 -> -0.15, so offset near 0. Noise mean ~0.5? Use +0.5 for small |x|.
    # Model: y = 16.8*|x| + 0.5 for |x| < 1, else 16.8*|x| (noise negligible at large |x|)
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax < 1.0:
                out.append(16.8 * ax + 0.5)
            else:
                out.append(16.8 * ax)
        except Exception:
            out.append(None)
    return {"y": out}
