def predict(probe):
    # Mechanism: every character's code point is shifted by +2 or +4.
    # The shift depends on the character's code point AND its position.
    #
    # Position >= 1: everything gets +4 [E1,E2,E6].
    # Position 0: a contiguous code-point range [0x3E, 0x76] gets +2;
    #   everything else gets +4.
    #
    # Evidence for the range boundaries at position 0:
    #  - '=' (0x3D) is +4 [E8,E11,E12: '='->Y]
    #  - '>' (0x3E) is +2 [E8,E9,E11,E12: '>'->Z]
    #  - '?' (0x3F) is +2 [E8,E9,E11,E12: '?'->A]
    #  - '@' (0x40) is +2 [E3,E5,E12,E14: '@'->B]
    #  - 'A'..'V' +2 [E3,E7], 'W'..'Z' +4 [E4,E7,E14: 'Z'->^]
    #  - '[' '\' ']' '^' '_' '`' are +2 [E13,E14: '['->_, ']'->y, '^'->z, '_'->a, '`'->b]
    #  - 'a'..'v' +2 [E1,E6,E7], 'w'..'~' +4 [E2,E4,E13: '{'->\x7f]
    #  So the +2 set at position 0 is exactly 0x3E..0x76 (contiguous).
    #  Note 'Z' (0x5A) is inside the range but observed +4 [E14: 'Z'->^].
    #  Hmm — 'Z' contradicts contiguity. Re-examine: 'Z'->'^' is +4.
    #  So the range is NOT fully contiguous: 'Z' (0x5A) is +4.
    #  Check 'W','X','Y','Z' all +4 [E4,E7,E14]. So uppercase W-Z are +4.
    #  Everything else in 0x3E..0x76 is +2.

    def shift_char(c, is_first):
        o = ord(c)
        if is_first and 0x3E <= o <= 0x76 and not (0x57 <= o <= 0x5A):
            return chr(o + 2)
        return chr(o + 4)

    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        if not isinstance(s, str):
            s = str(s)
        out = []
        for i, c in enumerate(s):
            out.append(shift_char(c, i == 0))
        outputs.append("".join(out))
    return {"outputs": outputs}
