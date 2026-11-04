def predict(probe):
    try:
        out = []
        for s in probe["inputs"]:
            r = s[::-1]
            i = (len(r) + 1) // 2
            out.append(r[:i] + "I" + r[i:])
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
