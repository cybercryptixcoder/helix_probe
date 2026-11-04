def predict(probe):
    # Deduplicate characters keeping first occurrence, case-sensitively [E1, E2]
    # Append 'h' only if the result does not already end with 'h' [E2: "h"->"h", "hh"->"h", "Hh"->"Hh"]
    # Case-sensitive: 'a' and 'A' distinct [E2: "aA"->"aAh", "abcABC"->"abcABCh"]
    # Space is a normal character, deduplicated too [E1, E2: "a b a b"->"a bh"]
    # 'h' in input is kept as first occurrence; trailing 'h' suppresses append [E2: "Hello"->"Heloh"]
    def transform(s):
        seen = set()
        out = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
        r = ''.join(out)
        if not r.endswith('h'):
            r += 'h'
        return r

    return {"outputs": [transform(x) for x in probe["inputs"]]}
