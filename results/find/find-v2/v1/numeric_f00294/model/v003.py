def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            try:
                if x == 0:
                    out.append(2058.0)
                elif x <= -1:
                    out.append(x - 8.4)
                elif x < 0:
                    out.append(-8.4)
                elif x <= 1:
                    out.append(17.8)
                else:
                    # uncertain region just above 1: E3 shows flat 18.8 up to 1.5
                    if x <= 1.5:
                        out.append(18.8)
                    else:
                        out.append(16.0 * x + 0.8)
            except Exception:
                out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
