def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            if not words:
                out.append("")
                continue
            first = words[0][::-1]
            if len(words) == 1:
                out.append(first)
            else:
                rest = "".join(words[1:])[::-1]
                out.append(first + " " + rest)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
