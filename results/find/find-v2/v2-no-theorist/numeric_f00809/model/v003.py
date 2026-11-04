import math

def predict(probe):
    # Observations are small, bounded roughly in [-0.25, 0.25] [E1-E10].
    # Nearby inputs give wildly different outputs: not smooth, looks like noise/high-freq [E6, E8].
    # f(-x) != -f(x) [E2]. No simple magnitude/sign structure [E4].
    # KEY: for large |x| (>=80), outputs are tiny and nearly constant ~0.005 [E4, E10].
    #   E4: x=-120..-80 -> 0.0049,0.0059,0.0074 ; E10: -120..-80 -> 0.0049..0.0074
    #   This is a special interval: |x|>=~80 gives ~0.005 (very small positive).
    # For |x|<80, outputs look like noise in [-0.25,0.25], no structure found.
    # Best guess: deterministic pseudo-random-ish function; model as noise with
    #   a special small-value plateau for |x|>=80.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax >= 80:
                # plateau: small positive, slowly varying ~0.005
                v = 0.005 + 0.00003 * (ax - 80)
            else:
                # placeholder: bounded pseudo-random in [-0.25,0.25]
                v = 0.25 * math.sin(x * 12.9898 + 78.233) * math.cos(x * 4.1414)
            out.append(v)
        except Exception:
            out.append(None)
    return {"y": out}
