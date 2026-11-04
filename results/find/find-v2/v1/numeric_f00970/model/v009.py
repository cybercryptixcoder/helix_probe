def predict(probe):
    """Piecewise model: noisy ~12.0 plateau on [-3.05, 3.05], zero-mean noise elsewhere."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            if -3.05 <= x <= 3.05:
                ys.append(12.0)
            else:
                ys.append(0.0)
        return {"y": ys}
    except Exception:
        return {"y": []}
