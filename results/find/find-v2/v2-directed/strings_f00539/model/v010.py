def predict(probe):
    # Collapse = keep first occurrence of each char (global dedup, case-sensitive)
    #   [E1 test->tes, E10, E13 memo->meo, E18 hollo->hol, E19 yoyo->yo]
    # h appended to output unless the LAST collapsed segment starts with 'h'
    #   (all-lower) [E10 hello->helo, E12 hallo->hlo, E16 dog hello->hel,
    #   E18 hobo->hob, E19 yoyo->yoh]. Unified for single word (segment=word)
    #   and multi-word (segment=tail). Case-sensitive: 'H' keeps h [E1 Hello].
    # Multi-word: first word collapsed; later words filtered to drop chars whose
    #   lowercase is in first word, then collapsed, concatenated [E3,E4].
    #   h suppressed if first word OR tail starts with 'h' [E8,E16].
    # ? Single-word suppression "starts h" (vs also requiring ends o/y) is
    #   untested for h-words ending in consonants; using "starts h" for
    #   consistency with the tail rule.
    def collapse(s):
        seen = set()
        res = []
        for c in s:
            if c in seen:
                continue
            seen.add(c)
            res.append(c)
        return ''.join(res)

    def all_lower(s):
        letters = [c for c in s if c.isalpha()]
        return bool(letters) and all(c.islower() for c in letters)

    def suppresses(coll):
        return coll[:1] == 'h' and all_lower(coll)

    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                coll = collapse(s)
                out.append(coll if suppresses(coll) else coll + 'h')
            else:
                first = collapse(words[0])
                first_letters = set(first.lower())
                tail_parts = []
                for w in words[1:]:
                    filtered = ''.join(c for c in w if c.lower() not in first_letters)
                    tail_parts.append(collapse(filtered))
                tail = ''.join(tail_parts)
                add = not (suppresses(first) or suppresses(tail))
                if add:
                    tail = tail + 'h'
                out.append(first + ' ' + tail)
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
