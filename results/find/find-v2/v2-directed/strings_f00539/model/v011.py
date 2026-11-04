def predict(probe):
    # Collapse = keep first occurrence of each char (global dedup, case-sensitive)
    #   [E1 test->tes, E10, E13 memo->meo, E18 hollo->hol, E19 yoyo->yo]
    # h appended to output unless the collapsed segment STARTS WITH LOWERCASE 'h'
    #   (first char == 'h'). Case-sensitive: 'H' keeps h [E1 Hello, E20 Hello/HELLO/Hallo/Hullo/H2ello].
    #   Lowercase 'h' start suppresses regardless of other case/digits [E20 hEllo, h2ello, hEllo1].
    #   Ending in o/y is NOT required [E20 hEllo1->hElo1].
    #   Single word: segment = whole word [E10 hello->helo, hallo->hlo].
    #   Multi-word: first word collapsed; later words filtered to drop chars whose
    #   lowercase is in first word, then collapsed, concatenated [E3,E4].
    #   h suppressed if first word OR tail starts with lowercase 'h' [E8,E16,E17].
    def collapse(s):
        seen = set()
        res = []
        for c in s:
            if c in seen:
                continue
            seen.add(c)
            res.append(c)
        return ''.join(res)

    def suppresses(coll):
        return coll[:1] == 'h'

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
