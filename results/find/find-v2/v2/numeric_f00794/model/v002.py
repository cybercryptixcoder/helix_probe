import math

def predict(probe):
    # Observations:
    # - Outputs are bounded in [-1,1] for ordinary x, but x=0 gives ~475 [E2,E4]
    # - Same x gives DIFFERENT y across experiments (E1 vs E2: 88.2 -> -0.8284 vs 0.1028) [E1,E2]
    #   => f depends on position/index, not just x. E4 confirms: same x repeated gives different y.
    # - E4: [21.3,-6.0,...] vs E2: [88.2,66.0,...] — values differ per position.
    # - E4 duplicates: 88.2 at pos 9,10 -> 0.5269,0.6398 (different); 0.0 at pos 16,17 -> 474.05,475.16
    #   => output depends on index i, and x=0 spike varies slightly with index too.
    # - E4 got 100% match with v1 by luck? No — v1 used sin(x) and matched E4 exactly.
    #   Wait: E4 match=1.00 means sin(x) matched E4. But E1/E2/E3/E5 don't match sin(x).
    #   E4's observed values ARE sin(x)? Check: sin(21.3)=0.637... but E4 y[0]=-0.9926. No.
    #   Actually match 1.00 for E4 is suspicious. Re-examine: v1 predicted sin(x) values.
    #   E4 observed y[0]=-0.9926, v1 predicted 0.6374. That's NOT a match. So "match 1.00" is wrong?
    #   Trust the data: E4 observed does NOT equal sin(x). So v1 did not truly match E4.
    # - Best hypothesis: f(x) = sin(x + phase(index)) or similar index-dependent oscillation.
    #   E1: x=88.2,i=0 -> -0.8284; E2: x=88.2,i=0 -> 0.1028. Same index, different y!
    #   => not index alone either. So it's genuinely noisy/random per call.
    # - Given noise, best deterministic guess: bounded oscillation. Use sin(x) as baseline.
    # - x=0 special: ~475 (varies 474-475.4) [E2,E4]
    out = []
    for x in probe["x"]:
        try:
            if x == 0:
                out.append(475.0)  # spike at zero, varies slightly [E2,E4]
            else:
                out.append(math.sin(x))
        except Exception:
            out.append(None)
    return {"y": out}
