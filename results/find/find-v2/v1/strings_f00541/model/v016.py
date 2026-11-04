def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                outs.append(s)
                continue
            t = s.rstrip(" ")
            # Uppercase-then-lowercase strip: applies to 'H' first letter, length >= 3,
            # but NOT to 'A' or 'X' (and apparently not other letters per E16).
            if (len(t) >= 3 and t[0] == "H" and t[1].islower()):
                outs.append(t[1:])
            # All-uppercase strip: applies to 'H' first letter, length >= 3, not 'A'.
            elif len(t) >= 3 and t.isupper() and t[0] == "H":
                outs.append(t[1:])
            else:
                outs.append(t)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
