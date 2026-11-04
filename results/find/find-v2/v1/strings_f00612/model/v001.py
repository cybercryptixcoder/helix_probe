def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            r = []
            for ch in s:
                if ch == " ":
                    r.append("Y")
                else:
                    r.append(chr(ord(ch) + 1))
            out.append("".join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
