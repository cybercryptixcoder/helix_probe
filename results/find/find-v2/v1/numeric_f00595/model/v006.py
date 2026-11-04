import math

def predict(probe):
    """Model: f(x) = floor(x) + sign(x) for x != 0; f(0) = -1.
    Anomalous interval roughly (32.0, 42.25) where f returns small non-integer values.
    Exact anomalous function unknown; approximate with a smooth guess."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                if x is None:
                    out.append(None)
                elif 32.5 <= x < 42.25:
                    # Anomalous smooth region (E14-E18). Values observed ~ -0.3 to -0.65.
                    # Best guess: gentle oscillation around -0.45.
                    out.append(-0.45 + 0.12 * math.sin(x * 1.7))
                elif x == 0:
                    out.append(-1.0)
                elif x > 0:
                    out.append(float(math.floor(x)) + 1.0)
                else:
                    out.append(float(math.floor(x)) - 1.0)
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
