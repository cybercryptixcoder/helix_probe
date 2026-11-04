def predict(probe):
    try:
        outs = []
        for x in probe.get("inputs", []):
            if " " in x:
                # reverse whole string, then insert 'lmKA' after first reversed word
                rev = x[::-1]
                # first reversed word = chars up to first space in rev
                idx = rev.find(" ")
                if idx == -1:
                    outs.append("lmKA" + rev)
                else:
                    outs.append(rev[:idx] + "lmKA" + rev[idx:])
            else:
                outs.append("lmKA" + x[::-1])
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
