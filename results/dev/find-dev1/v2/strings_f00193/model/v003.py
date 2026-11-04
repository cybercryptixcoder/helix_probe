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
    # Rule: for non-ASCII first char, shift by -2 ONLY if the result is a "letter-like" char;
    #   otherwise leave unchanged. Evidence:
    #     - é->ç, É->Ç, ñ->ï, ß->Ý, ø->ö, Ω->Χ, 日->散 : shifted [E5]
    #     - µ(U+00B5)->³(U+00B3) : shifted (µ is a letter, ³ is superscript) [E6]
    #     - ª(U+00AA)->¨(U+00A8) : shifted (ª is a letter) [E6]
    #     - ²(U+00B2)->² : UNCHANGED (² is not a letter) [E6]
    #     - NBSP(U+00A0)->NBSP : UNCHANGED [E6]
    #     - ¡(U+00A1)->¡ : UNCHANGED [E6]
    #     - –(U+2013), —(U+2014) : UNCHANGED [E6]
    #     - €(U+20AC) : UNCHANGED [E5]
    #     - DEL(U+007F) : UNCHANGED [E6]
    #   So: shift -2 iff first char is a Unicode letter (per str.isalpha-like check),
    #   OR more precisely: shift iff char is alphabetic. µ and ª are alphabetic; ², NBSP, ¡, –, —, € are not.
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
        # Non-ASCII: shift codepoint by -2 only for alphabetic chars
        if o > 127:
            # Leave emoji and other astral / symbol chars unchanged
            if 0xD800 <= o <= 0xDFFF or o > 0xFFFF:
                return s
            if c.isalpha():
                return chr(o - 2) + s[1:]
            return s
        return s

    outputs = []
    for s in probe.get("inputs", []):
        outputs.append(shift(s) + "JTQL")
    return {"outputs": outputs}
