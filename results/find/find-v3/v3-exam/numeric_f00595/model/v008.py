import math

def predict(probe):
    # Model of the black box f(x).
    #
    # - Outside the anomalous interval, f(x) = floor(x)+1 for x>0, floor(x)-1 for x<=0.
    #   [E1,E2,E3,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14,E17,E19,E21]
    # - Anomalous noisy interval: outputs are small negative values (~-0.3..-0.7), noisy.
    #   Lower boundary: E22 shows 33.0 -> 34 (normal), 33.5 -> -0.5494 (noisy).
    #     So boundary is in (33.0, 33.5]. Guess 33.5? Actually 33.5 is noisy, 33.0 normal.
    #     E20 x=35.0 noisy. So lower boundary between 33.0 and 33.5. Guess 33.5? 
    #     But 33.5 already noisy, so boundary <= 33.5. Use 33.5 as boundary (v<=33.5 normal? no).
    #     Let's set lower boundary = 33.5: v > 33.5 -> noisy? But 33.5 is noisy. So v >= 33.5 noisy.
    #     Hmm, could be exactly 33.5. Use: 33.5 <= v < upper.
    #   Upper boundary: E20 x=42.0 -> -0.3499 (noisy), x=42.05 -> 43 (normal).
    #     So boundary in (42.0, 42.05]. Guess 42.05.
    #   Inside: noisy. Return -0.5 as best guess (mean-ish). Cannot predict exact.
    x = probe["x"]
    ys = []
    for v in x:
        if v is None:
            ys.append(None)
            continue
        if 33.5 <= v < 42.05:
            ys.append(-0.5)
        else:
            if v > 0:
                ys.append(float(math.floor(v) + 1))
            else:
                ys.append(float(math.floor(v) - 1))
    return {"y": ys}
