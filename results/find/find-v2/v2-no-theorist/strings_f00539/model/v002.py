def predict(probe):
    # Rule: deduplicate ALL characters (keep first occurrence), regardless of case/type [E2]
    #   "112233" -> "123", "!!!???" -> "!?", "ZzZz" -> "Zz", "a1a1b2b2" -> "a1b2"
    #   "Hello HELLO" -> "Helo ELO" (H,e,l,o kept; second l,o,space,H,E,L,L,O deduped)
    #   "lL1lL1" -> "lL1" (l,L,1 kept; rest deduped)
    # Rule: append 'h' at end [E1, E2]
    # Rule: case-sensitive dedup (a vs A distinct) [E2: "aAbBcC" -> "aAbBcC"]
    def transform(s):
        seen = set()
        out = []
        for ch in s:
            if ch in seen:
                continue
            seen.add(ch)
            out.append(ch)
        return ''.join(out) + 'h'
    return {"outputs": [transform(x) for x in probe["inputs"]]}
