def predict(probe):
    # Position-0 shift is +2 for a contiguous codepoint band, else +4.
    # E11: P->R,Q->S,R->T,S->U,T->V,U->W,V->X,W->[ (+4),X->\ (+4),Y->] (+4)
    #   So uppercase +2 ends at W(87); X,Y,Z are +4.
    # E7: u->w,v->x (+2), w->{ (+4). So lowercase +2 ends at v(118); w..z +4.
    # E10: [,\,],^ +4; ;,<,=,>,? +4; O->Q +2.
    # E1-E6: a..v +2, A..W +2, @(64) +2, _(95),`(96) +2.
    # So +2 set: [64,87] ∪ [95,118]. Everything else +4. pos>0 always +4 [E9].
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0 and (64 <= o <= 87 or 95 <= o <= 118):
            return chr(o + 2)
        return chr(o + 4)
    out = []
    for s in probe["inputs"]:
        out.append("".join(shift(c, i) for i, c in enumerate(s)))
    return {"outputs": out}
