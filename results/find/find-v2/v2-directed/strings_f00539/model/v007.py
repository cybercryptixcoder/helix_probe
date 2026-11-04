def predict(probe):
    # Collapse runs of identical letters (case-sensitive) [E1,E2,E10]
    # Single word: collapse; then append 'h' unless the collapsed word is
    #   all-lowercase, ends in o/y, AND was changed by collapse -> no h [E10]
    #   (hello->helo no h; jello->jelo no h; yellow->yelowh keeps h because
    #    'yellow' collapses to 'yelow' which ends in 'w', not o/y) [E10]
    #   Uppercase/mixed-case changed words keep h (Hello->Heloh, HELLO->HELOh) [E10]
    # Multi-word: first word collapsed; later words filtered to remove chars
    #   whose lowercase appears in first word, then collapsed, concatenated [E3,E4]
    #   h appended to tail unless first word (all-lower, ends o/y, changed) OR
    #   last original word (all-lower, ends o/y, changed) suppresses it [E5,E6,E8]
    def collapse(s):
        res = []
        prev = None
        for c in s:
            if c == prev:
                continue
            res.append(c)
            prev = c
        return ''.join(res)

    def all_lower(s):
        letters = [c for c in s if c.isalpha()]
        return bool(letters) and all(c.islower() for c in letters)

    def ends_oy(s):
        return bool(s) and s[-1] in 'oy'

    def suppress(w):
        # all-lower, ends in o/y, and changed by collapse
        return all_lower(w) and ends_oy(w) and collapse(w) != w

    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                w = collapse(s)
                if suppress(s):
                    out.append(w)
                else:
                    out.append(w + 'h')
            else:
                first = collapse(words[0])
                first_letters = set(first.lower())
                tail_parts = []
                for w in words[1:]:
                    filtered = ''.join(c for c in w if c.lower() not in first_letters)
                    tail_parts.append(collapse(filtered))
                tail = ''.join(tail_parts)
                add = True
                if suppress(words[0]):
                    add = False
                elif suppress(words[-1]):
                    add = False
                if add:
                    tail = tail + 'h'
                out.append(first + ' ' + tail)
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
