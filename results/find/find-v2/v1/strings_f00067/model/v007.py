def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            segs = s.split()
            rev = [seg[::-1] for seg in segs]
            if rev:
                # extra copy only if no leading/trailing whitespace on raw input
                if s == s.strip():
                    rev[-1] = rev[-1][0] + rev[-1]
            outputs.append(" ".join(rev))
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
