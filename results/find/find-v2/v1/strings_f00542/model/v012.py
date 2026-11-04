def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            if not words:
                out.append("")
                continue
            w = words[0]
            rev = w[::-1]
            stripped = rev.lstrip("o")
            if stripped != rev:
                # some leading o's were removed; keep exactly one
                first = "o" + stripped
            else:
                first = rev
            if len(words) == 1:
                out.append(first)
            else:
                rest = "".join(words[1:])[::-1]
                out.append(first + " " + rest)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
