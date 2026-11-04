import math

def predict(probe):
    """Model: f(x) = floor(x) + sign(x) for x != 0; f(0) = -1.
    Known anomaly near x=40.5 (E14) where f returned -0.5767; uncertain interval."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                if x is None:
                    out.append(None)
                elif x == 0:
                    out.append(-1.0)
                elif 40.0 < x < 41.0:
                    # Anomalous interval observed at 40.5 (E14); best guess: constant -0.5767
                    out.append(-0.5767)
                elif x > 0:
                    out.append(float(math.floor(x)) + 1.0)
                else:
                    out.append(float(math.floor(x)) - 1.0)
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
