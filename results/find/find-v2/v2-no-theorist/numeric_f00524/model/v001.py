import math

def predict(probe):
    # Observations: most outputs are 0.0 (or -0.0); only x=2.9 gave 3.0 [E1]
    # Hypothesis: f(x) = round(x) when x is in some small interval near 3, else 0
    # The single nonzero (3.0 at x=2.9) suggests a narrow window around 3.
    # Best guess: nonzero only for x in [2.5, 3.5), returning round(x)=3.
    # Everything else -> 0.0. Sign of zero is unreliable/noisy, so output 0.0.
    out = []
    for x in probe.get("x", []):
        try:
            if 2.5 <= x < 3.5:
                out.append(float(round(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
