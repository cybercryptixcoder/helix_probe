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
            # lowercase the rest first
            rest = s[1:].lower()
            # index based on ORIGINAL string length
            idx = len(s) // 2
            # build the string with first char + lowercased rest, then insert '10' at idx
            transformed = s[0] + rest
            with10 = transformed[:idx] + "10" + transformed[idx:]
            # titlecase the first character (may expand)
            first = with10[0]
            titled = first.title()
            outs.append(titled + with10[1:])
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
