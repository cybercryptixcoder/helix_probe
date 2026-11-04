def predict(probe):
    """Best guess: f(x)=1 for x in [-1, 1.5], else 0."""
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                if x is None:
                    out.append(None)
                elif -1 <= x <= 1.5:
                    out.append(1.0)
                else:
                    out.append(0.0)
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
