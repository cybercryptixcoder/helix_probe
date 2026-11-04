def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                if x == 0:
                    out.append(2058.0)
                elif x >= 1:
                    out.append(16.0 * x + 0.8)
                elif x <= -1:
                    out.append(x - 8.4)
                else:
                    # between -1 and 0: interpolate toward the spike? unknown
                    # use negative branch as best guess
                    out.append(x - 8.4)
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
