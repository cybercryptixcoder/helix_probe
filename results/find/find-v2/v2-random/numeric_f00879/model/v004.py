import math

def predict(probe):
    # Beliefs:
    # The output is a smooth oscillatory function of x, roughly sin-like in x/30 to x/40,
    # with amplitude growing with |x| and a phase shift. There is no obvious discontinuity.
    # A pure sinusoid fits poorly; the data look like sin(x/30) modulated by a slowly varying amplitude.
    # I model y = A(x) * sin(x/30 + phi) + B(x), with A,B low-order polynomials in x.
    # This is a guess from the overall pattern: positive x often gives positive-ish y, but not monotonic.
    # The function seems roughly odd-ish but with drift; large |x| gives larger amplitude.
    # No region change detected; treat as global smooth function.
    # Fit-free heuristic constants chosen to match scale (values ~ -3..4).
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # amplitude grows mildly with |x|
            A = 1.0 + 0.012 * abs(x)
            # phase shift
            phi = 0.3
            # baseline drift
            B = 0.0
            y = A * math.sin(x / 30.0 + phi) + B
            ys.append(y)
        return {"y": ys}
    except Exception:
        try:
            return {"y": [None for _ in probe.get("x", [])]}
        except Exception:
            return {"y": []}
