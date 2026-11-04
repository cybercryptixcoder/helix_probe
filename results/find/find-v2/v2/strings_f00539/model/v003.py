def predict(probe):
    # Deduplicate characters keeping first occurrence, case-sensitively [E1, E2, E3]
    # Space is a normal character, deduplicated too [E1, E2, E3, E4]
    # Append 'h' only if the result does not already end with 'h' [E2]
    # BUT: if the input contains 'h', no 'h' is appended at all [E4: "hello hello"->"helo ",
    #   "the cat sat"->"the cas", "abcdefghij"->"abcdefghij"]
    #   Wait: "banana split"->"ban splith" has no h in input, appended. "good morning"->"god mrnih"
    #   ends in h from input? "morning" has no h... "god mrnih" ends with h appended.
    #   Re-examine: "hello hello" -> "helo " (no h appended, input had h)
    #   "the cat sat" -> "the cas" (no h appended, input had h)
    #   "abcdefghij" -> "abcdefghij" (no h appended, input had h)
    #   So rule: if 'h' appears anywhere in input, do NOT append 'h'. [E4]
    #   Check E2: "Hello"->"Heloh" has h in input but appended h! Contradiction?
    #   "Hello" -> "Heloh": dedup gives "Helo", ends not with h, appended h. Input has 'H' (uppercase).
    #   So rule is case-sensitive: only lowercase 'h' in input suppresses append. [E2, E4]
    #   E2 "h"->"h", "hh"->"h", "Hh"->"Hh" (dedup "Hh", ends with h, no append).
    #   "Hello"->"Heloh": input has 'H' not 'h', so append. Consistent.
    #   E4 "hello hello": has lowercase h, suppress append -> "helo ". Consistent.
    def transform(s):
        seen = set()
        out = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
        r = ''.join(out)
        if 'h' not in s and not r.endswith('h'):
            r += 'h'
        return r

    return {"outputs": [transform(x) for x in probe["inputs"]]}
