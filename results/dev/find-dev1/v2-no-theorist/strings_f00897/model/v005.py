def predict(probe):
    # Position-0 shift is +2 for a contiguous codepoint band, else +4 [E4,E5,E6,E7,E10].
    # Band boundaries from E10: '['(91)->'_'(+4), '\\'(92)->'`'(+4), ']'(93)->'y'(+4), '^'(94)->'z'(+4)
    #   so 91-94 are +4. ';'(59)->'?'(+4), '<'(60)->'@'(+4), '='(61)->'Y'(+4), '>'(62)->'Z'(+4), '?'(63)->'A'(+4)
    #   so 59-63 are +4. 'O'(79)->'Q'(+2) confirms O..Z is +2? wait O->Q is +2.
    # Recheck: E7 K..N -> +2 (M,N,O,P). E10 O->Q is +2. So uppercase K..Z all +2? 
    #   E4 Z->^ (+4)? E4 'Z'->'^' means Z(90)->^(94) +4. Contradiction with O->Q +2.
    #   Hmm E10 O->Q: O(79)+2=Q(81). E4 Z->^: Z(90)+4=^(94). So uppercase band is not all +2.
    # Let's tabulate pos0 uppercase: A..N +2 (E1,E7), O +2 (E10), Z +4 (E4). P..Y unknown.
    # Lowercase pos0: a..v +2 (E5,E6,E7), w..z +4 (E7). So a..v +2, w..z +4.
    # Digits 0..9 +4 (E4). Space,!,~ +4 (E4). {,},: +4 (E3). @,_,` +2 (E3).
    # Symbols: 59-63 +4 (E10), 91-94 +4 (E10).
    # Best guess: +2 band is [64,78]∪[79?]... O=79 is +2 but Z=90 is +4. 
    #   Maybe uppercase +2 is A..O (65..79)? Then P..Z +4. Check E7 K..N +2 ok, O +2 ok, Z +4 ok.
    # Lowercase +2 a..v (97..118), w..z +4. @(64),_(95),`(96) +2.
    # So +2 set: [64,79] ∪ [95,118]. Everything else +4. pos>0 always +4 [E9].
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0 and (64 <= o <= 79 or 95 <= o <= 118):
            return chr(o + 2)
        return chr(o + 4)
    out = []
    for s in probe["inputs"]:
        out.append("".join(shift(c, i) for i, c in enumerate(s)))
    return {"outputs": out}
