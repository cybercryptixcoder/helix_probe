def predict(probe):
    """Model: f(x) = round(x) (half away from zero) for |x| < 4.4, else 0."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                xv = float(x)
            except Exception:
                ys.append(None)
                continue
            if abs(xv) < 4.4:
                if xv >= 0:
                    ys.append(float(int(xv + 0.5)))
                else:
                    ys.append(float(-int(-xv + 0.5)))
            else:
                ys.append(0.0)
        return {"y": ys}
    except Exception:
        return {"y": []}
