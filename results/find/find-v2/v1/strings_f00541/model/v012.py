def predict(probe):
    """Best-effort model. Strip trailing spaces always. Then strip first char iff
    first char uppercase, second char lowercase, and (length >= 4 OR string contains a space).
    This fits E12 (Hbllo->bllo, len 5) and E6 (Hello->ello) but keeps E3/E4 (Ab, Aa unchanged)
    and E10 (Abc, Abcd unchanged) — though E12 'Hxllo' (len 5) strips while 'Abcd' (len 4) doesn't,
    so length alone isn't the discriminator; flagged uncertain."""
    try:
        outs = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                outs.append(s)
                continue
            t = s.rstrip(" ")
            if (len(t) >= 2
                    and t[0].isupper() and t[1].islower()
                    and (len(t) >= 5 or " " in t)):
                outs.append(t[1:])
            else:
                outs.append(t)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
