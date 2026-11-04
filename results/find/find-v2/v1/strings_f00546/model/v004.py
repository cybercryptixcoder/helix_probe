def predict(probe):
    try:
        outs = []
        for x in probe.get("inputs", []):
            words = x.split()
            if len(words) == 0:
                outs.append("lmKA")
                continue
            if len(words) == 1:
                outs.append("lmKA" + words[0][::-1])
                continue
            rev = [w[::-1] for w in words]
            result = " ".join(rev[:-1]) + " lmKA" + rev[-1]
            outs.append(result)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
