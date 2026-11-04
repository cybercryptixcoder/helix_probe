def predict(probe):
    """Best guess: 26 on [-2, 2], 25 outside."""
    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            try:
                if -2 <= x <= 2:
                    ys.append(26.0)
                else:
                    ys.append(25.0)
            except Exception:
                ys.append(None)
        return {"y": ys}
    except Exception:
        return {}
