def predict(probe):
    def collapse(s):
        letters = [c for c in s if c.isalpha()]
        if letters and (all(c.islower() for c in letters) or all(c.isupper() for c in letters)):
            res = []
            prev = None
            for c in s:
                if c == prev:
                    continue
                res.append(c)
                prev = c
            return ''.join(res)
        return s
    def all_lower(s):
        letters = [c for c in s if c.isalpha()]
        return bool(letters) and all(c.islower() for c in letters)
    def ends_oy(s):
        return bool(s) and s[-1] in 'oy'
    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                w = collapse(s)
                changed = (w != s)
                if all_lower(w) and ends_oy(w) and changed:
                    out.append(w)
                else:
                    out.append(w + 'h')
            else:
                first = collapse(words[0])
                first_changed = (first != words[0])
                first_letters = set(first.lower())
                tail_parts = []
                for w in words[1:]:
                    filtered = ''.join(c for c in w if c.lower() not in first_letters)
                    filtered = collapse(filtered)
                    tail_parts.append(filtered)
                tail = ''.join(tail_parts)
                last_orig = words[-1]
                last_changed = (collapse(last_orig) != last_orig)
                add = True
                if all_lower(first) and ends_oy(first) and first_changed:
                    add = False
                elif all_lower(last_orig) and ends_oy(last_orig) and last_changed:
                    add = False
                if add:
                    tail = tail + 'h'
                out.append(first + ' ' + tail)
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
