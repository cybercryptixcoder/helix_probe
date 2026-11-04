def predict(probe):
    try:
        outs = []
        for x in probe.get("inputs", []):
            words = x.split()
            if len(words) == 0:
                outs.append("lmKA")
                continue
            rev = [w[::-1] for w in words]
            if len(words) == 1:
                if x[-1:].isspace():
                    outs.append(rev[0] + " lmKA")
                else:
                    outs.append("lmKA" + rev[0])
                continue
            result = " ".join(rev[:-1]) + " lmKA" + rev[-1]
            outs.append(result)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
