def predict(probe):
    """Model: f(x) reverses by Unicode code point (valid surrogate pairs kept intact), then removes all Unicode whitespace."""
    try:
        out = []
        for s in probe.get("inputs", []):
            # Convert to list of code points, treating valid surrogate pairs as single units.
            units = []
            i = 0
            n = len(s)
            while i < n:
                c = s[i]
                o = ord(c)
                if 0xD800 <= o <= 0xDBFF and i + 1 < n:
                    o2 = ord(s[i + 1])
                    if 0xDC00 <= o2 <= 0xDFFF:
                        units.append(s[i:i+2])
                        i += 2
                        continue
                units.append(c)
                i += 1
            rev = units[::-1]
            out.append("".join(u for u in rev if not all(ch.isspace() for ch in u)))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
