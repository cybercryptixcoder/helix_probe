def predict(probe):
    # Mechanism: each character's code point is shifted by +2 or +4.
    # Position >= 1: everything gets +4 [E1,E2,E6,E17].
    # Position 0: two contiguous code-point ranges get +2:
    #   [0x3E, 0x56]  ('>'..'V')  and  [0x5B, 0x76]  ('['..'v').
    #   Everything else gets +4.
    # Boundaries:
    #  '=' (0x3D) +4 [E8,E11,E12,E15,E16,E17]; '>' (0x3E) +2 [E8,E9,E11,E12,E15,E16,E17]
    #  '?' (0x3F) +2 [E8,E9,E11,E12,E15,E16,E17]; '@' (0x40) +2 [E3,E5,E12,E14,E15,E16]
    #  'A'..'V' (0x41..0x56) +2 [E3,E7,E15,E16]; 'W'..'Z' (0x57..0x5A) +4 [E4,E7,E14,E15,E16]
    #  '['..'`' (0x5B..0x60) +2 [E13,E14]; 'a'..'v' (0x61..0x76) +2 [E1,E6,E7,E16,E17]
    #  'w'..'~' (0x77..0x7E) +4 [E2,E4,E13,E16,E17]

    def shift_char(c, is_first):
        o = ord(c)
        if is_first and ((0x3E <= o <= 0x56) or (0x5B <= o <= 0x76)):
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
