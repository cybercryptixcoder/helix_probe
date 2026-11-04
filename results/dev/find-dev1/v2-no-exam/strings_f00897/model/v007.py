def predict(probe):
    # Mechanism: each character's code point is shifted by +2 or +4.
    # The shift depends on the character's code point AND its position.
    #
    # Position 0: a "special" set of characters gets +2; everything else +4.
    # Position >=1: everything gets +4.
    #
    # Special +2 set at position 0 (from evidence):
    #  - lowercase a-v: +2 [E1,E6,E7]; w-z: +4 [E2,E4]
    #  - uppercase A-V: +2 [E3,E7]; W-Z: +4 [E4,E7]
    #  - '@': +2 [E3,E5]
    #  - '?' and '>': +2 [E8,E9,E11,E12]  ('?'->A, '>'->Z)
    #  - '=' '<' ';' ':' '9' '8' '7' '6' ... : +4 [E8,E10,E11,E12]
    #    E12: '='->Y(+4), '<'->@(+4), ';'->?(+4), ':'->>(+4)
    #    E10: '7'->;(+4), '6'->:(+4), ... '0'->4(+4)
    #  So the +2 set in punctuation begins at '>' (0x3E) and includes '?' (0x3F) and '@' (0x40).
    #  '=' (0x3D) is +4. So boundary: c >= '>' and c <= 'v' (with gaps) get +2.
    #
    # Let's define the +2 set at position 0 as a union of ranges:
    #   '>' (0x3E), '?' (0x3F), '@' (0x40)   -> 0x3E..0x40
    #   'A'..'V' (0x41..0x56)
    #   'a'..'v' (0x61..0x76)
    # Everything else at position 0: +4.
    # Position >=1: +4 always.
    #
    # Check '=' (0x3D) is +4 [E12: '='->Y]. Good, just below 0x3E.
    # Check '>' (0x3E) is +2 [E8: '>'->Z, E12: '>'->Z]. Good.
    # Check '?' (0x3F) is +2 [E8: '?'->A, E12: '?'->A]. Good.
    # Check '@' (0x40) is +2 [E3,E5,E12: '@'->B]. Good.
    # Check 'V' (0x56) +2 [E7: 'V'->X], 'W' (0x57) +4 [E4]. Good.
    # Check 'v' (0x76) +2 [E7: 'v'->x], 'w' (0x77) +4 [E4]. Good.

    def shift_char(c, is_first):
        o = ord(c)
        if is_first and (0x3E <= o <= 0x40 or 0x41 <= o <= 0x56 or 0x61 <= o <= 0x76):
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
