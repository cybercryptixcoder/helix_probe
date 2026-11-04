def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                if x == 0:
                    out.append(2058.0)
                elif x > 0:
                    if x < 1:
                        out.append(17.8)
                    else:
                        out.append(16.0 * x + 0.8)
                else:  # x < 0
                    if x > -1:
                        out.append(-8.4)
                    else:
                        out.append(x - 8.4)
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
