def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                outs.append(s)
                continue
            t = s.rstrip(" ")
            if len(t) == 0:
                outs.append(t)
                continue
            # 'H' + lowercase second char: strip first char (any length >= 2)
            if len(t) >= 2 and t[0] == "H" and t[1].islower():
                outs.append(t[1:])
            # All-uppercase starting with 'H', length >= 3: strip first char
            elif len(t) >= 3 and t[0] == "H" and t.isupper():
                outs.append(t[1:])
            # Single 'H' alone: strip to empty
            elif t == "H":
                outs.append("")
            else:
                outs.append(t)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
