def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if len(s) == 0:
                outs.append("10")
                continue
            if len(s) == 1:
                outs.append("10" + s[0].lower())
                continue
            idx = len(s) // 2  # number of ORIGINAL chars before '10'
            pieces = []
            for i, ch in enumerate(s):
                if i == idx:
                    pieces.append("10")
                if i == 0:
                    pieces.append(ch.title())
                else:
                    pieces.append(ch.lower())
            if idx >= len(s):
                pieces.append("10")
            outs.append("".join(pieces))
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
