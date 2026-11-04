def predict(probe):
    # Rule: shift the FIRST character back by 2 in Unicode code point order [E1, E3, E5]
    #   - ASCII letters: a->y, b->z, c->a (wraps within a-z / A-Z) [E1, E3]
    #   - Non-ASCII letters: é->ç, É->Ç, ñ->ï, ß->Ý, ø->ö (plain codepoint -2) [E5]
    #   - Greek Ω->Χ (codepoint -2) [E5]
    #   - CJK 日->散 (codepoint -2) [E5]
    #   - Emoji / symbols: unchanged (surrogate pair first unit -2 would corrupt; observed unchanged) [E5]
    #   - Digits, spaces, punctuation, control chars: unchanged [E1, E4]
    # Rule: append "JTQL" to the whole string [E1-E4]
    # Rule: empty string -> "JTQL" (?) [inferred]
    def shift(s):
        if not s:
            return s
        c = s[0]
        o = ord(c)
        # ASCII letters wrap within their case range
        if 'a' <= c <= 'z':
            return chr((o - ord('a') - 2) % 26 + ord('a')) + s[1:]
        if 'A' <= c <= 'Z':
            return chr((o - ord('A') - 2) % 26 + ord('A')) + s[1:]
        # Non-ASCII: shift codepoint by -2, but only for letters/scripts where it makes sense.
        # Emoji (surrogates / high planes) and symbols left unchanged.
        if o > 127:
            # Leave emoji and other astral / symbol chars unchanged
            if 0xD800 <= o <= 0xDFFF or o > 0xFFFF:
                return s
            # Leave common symbol/punctuation blocks unchanged (e.g. € U+20AC)
            if 0x2000 <= o <= 0x2BFF:
                return s
            return chr(o - 2) + s[1:]
        return s

    outputs = []
    for s in probe.get("inputs", []):
        outputs.append(shift(s) + "JTQL")
    return {"outputs": outputs}
