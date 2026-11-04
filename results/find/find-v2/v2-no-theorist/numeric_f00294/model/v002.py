def predict(probe):
    # f(x) = x + 17.8 for x > 0 [E1, E2]
    # f(x) = x - 8.4 for x < 0 [E1, E2]
    # f(0) = 2058.0 [E2]
    out = []
    for x in probe.get("x", []):
        try:
            if x > 0:
                out.append(x + 17.8)
            elif x < 0:
                out.append(x - 8.4)
            else:
                out.append(2058.0)
        except Exception:
            out.append(None)
    return {"y": out}
