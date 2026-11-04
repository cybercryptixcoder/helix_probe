def predict(probe):
    try:
        outs = []
        for x in probe.get("inputs", []):
            if " " not in x:
                outs.append("lmKA" + x[::-1])
                continue
            words = x.split(" ")
            # drop leading empty words (from leading spaces)
            while len(words) > 1 and words[0] == "":
                words.pop(0)
            if len(words) == 1:
                outs.append("lmKA" + words[0][::-1])
                continue
            rev = [w[::-1] for w in words]
            # insert lmKA before the last word, no space between
            result = " ".join(rev[:-1]) + " lmKA" + rev[-1]
            outs.append(result)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
