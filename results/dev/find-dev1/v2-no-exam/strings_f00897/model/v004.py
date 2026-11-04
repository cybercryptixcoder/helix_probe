def predict(probe):
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, ch in enumerate(s):
            if i == 0 and (('a' <= ch <= 'n') or ('A' <= ch <= 'N')):
                r.append(chr(ord(ch) + 2))
            else:
                r.append(chr(ord(ch) + 4))
        out.append("".join(r))
    return {"outputs": out}
