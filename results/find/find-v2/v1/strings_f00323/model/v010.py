def predict(probe):
    """Model: f(x) reverses by code point (grouping adjacent valid surrogate pairs as one unit),
    then removes all Unicode whitespace."""
    try:
        out = []
        for s in probe.get("inputs", []):
            units = []
            i = 0
            n = len(s)
            while i < n:
                c = s[i]
                if 0xD800 <= ord(c) <= 0xDBFF and i + 1 < n:
                    d = s[i + 1]
                    if 0xDC00 <= ord(d) <= 0xDFFF:
                        units.append(c + d)
                        i += 2
                        continue
                units.append(c)
                i += 1
            rev = "".join(reversed(units))
            out.append("".join(ch for ch in rev if not ch.isspace()))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
