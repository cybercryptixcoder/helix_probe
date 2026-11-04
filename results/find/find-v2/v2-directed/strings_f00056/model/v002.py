def predict(probe):
    # Remove duplicate characters, keeping only the first occurrence, case-sensitive [E1, E2]
    #   e.g. "hello"->"helo", "Hello World"->"Helo Wrd", "UPPER lower"->"UPER lower"
    # Then shift the first character down by 1: a->z, b->a, ..., A->Z, B->A (wrap) [E1, E2]
    # Non-letter first characters (digits, symbols, spaces) are left unchanged [?]
    # Order: dedup first, then shift (first char always survives dedup) [?]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 1) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        seen = set()
        deduped = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                deduped.append(ch)
        if deduped:
            deduped[0] = shift(deduped[0])
        out.append("".join(deduped))
    return {"outputs": out}
