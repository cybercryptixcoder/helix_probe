def predict(probe):
    # Position-0 shift is +2 for codepoint band [64,87] and [95,118]; else +4. pos>0 always +4.
    # E12: ?(63)->A(+4), @(64)->B(+2), A->C(+2), Z(90)->^(+4), [(91)->_(+4), `(96)->b(+2), a->c(+2), v(118)->x(+2), w(119)->{(+4), {(123)->\x7f(+4).
    # E11: P..W +2, X,Y,Z +4. E7: u,v +2, w..z +4. E10: [..^ +4, ;..? +4, O->Q +2.
    # E1-E6: a..v +2, A..W +2, @ +2, _ +2, ` +2.
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0 and (64 <= o <= 87 or 95 <= o <= 118):
            return chr(o + 2)
        return chr(o + 4)
    return {"outputs": ["".join(shift(c, i) for i, c in enumerate(s)) for s in probe["inputs"]]}
