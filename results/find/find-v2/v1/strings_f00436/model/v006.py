def predict(probe):
    try:
        out = []
        for s in probe["inputs"]:
            if " " in s:
                stripped = s.strip(" ")
                if stripped == "":
                    out.append("I")
                    continue
                tokens = stripped.split(" ")
                rev_tokens = [t[::-1] for t in tokens]
                joined = " ".join(rev_tokens)
                i = len(joined) // 2
                out.append(joined[:i] + "I" + joined[i:])
            else:
                r = s[::-1]
                i = (len(r) + 1) // 2
                out.append(r[:i] + "I" + r[i:])
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
