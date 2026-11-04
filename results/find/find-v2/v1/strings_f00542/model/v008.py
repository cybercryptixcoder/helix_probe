def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            if not words:
                out.append("")
                continue
            w = words[0]
            # strip trailing 'o' chars, then reverse; all-'o' words -> 'o'
            stripped = w.rstrip("o")
            if stripped == "":
                first = "o"
            else:
                first = stripped[::-1]
            if len(words) == 1:
                out.append(first)
            else:
                rest = "".join(words[1:])[::-1]
                out.append(first + " " + rest)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
