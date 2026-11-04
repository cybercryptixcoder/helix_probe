def predict(probe):
    # Every character's codepoint is shifted by +2 or +4 depending on the character's value [E1-E8].
    # Position does NOT matter: 'b' at pos0 is +2 (E5 'b'->'d'), 'b' at pos1 is +4 (E1 'ab'->'cf')...
    #   wait, that contradicts. Let's recheck.
    # E8 'kK'->'mO': k->m (+2), K->O (+4). 'aa'->'ce': a->c (+2), a->e (+4).
    #   So position DOES matter: pos0 +2, pos>0 +4 for these chars.
    # E5: a..j at pos0 all +2. E6: k..t at pos0 all +2. E7: u,v +2; w,x +4; y,z +4.
    #   K..N at pos0 +2 (E7). 
    # E4: y,z,Z,0,9,!,~ at pos0 +4; a,b,A at pos0 +2.
    # E3: {,},:,~,0x7f,0x80,0x81 at pos0 +4; @,_,` at pos0 +2.
    # So pos0: +2 for a..v (97..118), A..N (65..78), @(64), _(95), `(96).
    #   +4 for w..z (119..122), O..Z (79..90), 0..9, space, !, ~, {, }, :, 0x7f+.
    # Check: A=65..N=78 +2, O=79..Z=90 +4. a=97..v=118 +2, w=119..z=122 +4.
    #   @=64 +2, _=95 +2, `=96 +2. So [64,78] +2, [79,90] +4, [91,96]? unknown, [97,118] +2, [119,122] +4.
    #   :(58)+4, 0-9(48-57)+4, space(32)+4, !(33)+4.
    #   {=123 +4, }=125 +4, ~=126 +4.
    # So pos0 +2 region: [64,78] ∪ [95,118]? But _=95,`=96 +2, and a..v=97..118 +2. So [95,118] +2.
    #   And [64,78] +2. What about [79,94]? O..Z=79..90 +4, [=91, \=92, ]=93, ^=94 unknown.
    #   What about [59,63]? :(58)+4, so maybe [59,63] unknown.
    #   Best guess: pos0 +2 if 64<=o<=78 or 95<=o<=118, else +4. pos>0 always +4.
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0 and (64 <= o <= 78 or 95 <= o <= 118):
            return chr(o + 2)
        return chr(o + 4)
    out = []
    for s in probe["inputs"]:
        out.append("".join(shift(c, i) for i, c in enumerate(s)))
    return {"outputs": out}
