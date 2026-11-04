def predict(probe):
    try:
        outs = []
        for x in probe.get("inputs", []):
            words = x.split()
            if len(words) == 0:
                outs.append("lmKA")
                continue
            rev = [w[::-1] for w in words]
            trailing = x[-1:].isspace()
            if len(words) == 1:
                if trailing:
                    outs.append(rev[0] + " lmKA")
                else:
                    outs.append("lmKA" + rev[0])
                continue
            if trailing:
                outs.append(" ".join(rev) + " lmKA")
            else:
                outs.append(" ".join(rev[:-1]) + " lmKA" + rev[-1])
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
