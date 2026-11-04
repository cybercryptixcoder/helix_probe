def predict(probe):
    def collapse(s):
        seen = set()
        res = []
        for c in s:
            if c in seen:
                continue
            seen.add(c)
            res.append(c)
        return ''.join(res)

    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                coll = collapse(s)
                out.append(coll if coll[:1] == 'h' else coll + 'h')
            else:
                first = collapse(words[0])
                first_chars = set(first)  # case-sensitive
                tail_raw = ''.join(words[1:])
                filtered = ''.join(c for c in tail_raw if c not in first_chars)
                tail = collapse(filtered)
                add = not (first[:1] == 'h' or tail[:1] == 'h')
                if add:
                    tail = tail + 'h'
                out.append(first + ' ' + tail)
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
