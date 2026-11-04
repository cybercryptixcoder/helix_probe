def predict(probe):
    # Hypothesis: f(x) = Caesar shift +1 on each character, then append "W".
    # Evidence E1:
    #  "abc123" -> "fgh678W": a->f is +5? No: a->f = +5, b->g=+5, c->h=+5, 1->6=+5, 2->7=+5, 3->8=+5. So shift +5.
    #  "level" -> "qj{jqW": l->q=+5, e->j=+5, v->{=+5, e->j=+5, l->q=+5. Yes +5.
    #  " Zebralower" -> "%_jgwfqt|jwW": space->% = +5 (space=32, %=37), Z->_(90->95), e->j, b->g, r->w, a->f, l->q, o->t, w->|, e->j, r->w. Yes +5.
    #  "Hello World function lazy" -> "Mjqqt%\twqi%kzshynts%qf~W": H->M(+5), e->j, l->q, l->q, o->t, space->%, W->\, o->t, r->w, l->q, d->i, space->%, f->k, u->z, n->s, c->h, t->y, i->n, o->t, n->s, space->%, l->q, a->f, z->~, y->}? Wait y->} is +5 (121->126). Observed "qf~W" = q,f,~ then W. So "lazy" -> "qf~}"? But observed ends "qf~W". Hmm, z->~ (+5), y->} (+5). But observed is "qf~W" — that's q,f,~,W. So "lazy" -> "qf~" + W? That's only 3 chars + W. Wait "lazy" is 4 chars: l,a,z,y -> q,f,~,} then W. But observed "qf~W" has no }. Let me recount.
    #  Actually "Hello World function lazy" length: H e l l o (5) space (6) W o r l d (11) space (12) f u n c t i o n (20) space (21) l a z y (25). Output "Mjqqt%\twqi%kzshynts%qf~W": M j q q t % \ t w q i % k z s h y n t s % q f ~ W. That's 25 chars. So l a z y -> q f ~ W? That's only 4: q,f,~,W. But y->W is +5? y=121, W=87. No. Hmm.
    #  Wait let me recount output: "Mjqqt%\twqi%kzshynts%qf~W"
    #  M(1)j(2)q(3)q(4)t(5)%(6)\(7)t(8)w(9)q(10)i(11)%(12)k(13)z(14)s(15)h(16)y(17)n(18)t(19)s(20)%(21)q(22)f(23)~(24)W(25)
    #  So position 22=q (l+5), 23=f (a+5), 24=~ (z+5), 25=W. But y+5 = } (125). W=87. So y->W is not +5.
    #  Hmm, but wait — maybe the last char is the appended "W" and y maps to }? But then output would be 26 chars. It's 25. So "lazy" (4 chars) -> "qf~W" (4 chars)? That means y->W. y=121, W=87, diff = -34. Odd.
    #  Let me recheck "bananaUPPER" -> "gfsfsfZUUJW": b->g(+5), a->f, n->s, a->f, n->s, a->f, U->Z(+5), P->U, P->U, E->J, then W appended. That's 10 chars + W = 11. Observed "gfsfsfZUUJW" = g f s f s f Z U U J W = 11. Good, so W appended.
    #  "Zebra" -> "_jgwfW": Z->_(+5), e->j, b->g, r->w, a->f, W appended. Good.
    #  So the "lazy" case: l->q, a->f, z->~, y->? and then W. But output has only one char after ~ before W... wait "qf~W": q,f,~,W. So y maps to nothing? Or y->W and no append?
    #  Hmm. Let me reconsider: maybe W is not always appended; maybe it's part of the shift for some char. But all others clearly append W.
    #  Actually wait: maybe "lazy" -> "qf~}" and then W, giving "qf~}W" (5 chars). But observed is "qf~W" (4). Let me recount the full output string char by char from the raw: "Mjqqt%\\twqi%kzshynts%qf\u007f~W". Ah! \u007f is DEL (127). So the string is M j q q t % \ t w q i % k z s h y n t s % q f \x7f ~ W. That's 26 chars!
    #  Let me recount: "Mjqqt%\twqi%kzshynts%qf\u007f~W"
    #  M j q q t % \ t w q i % k z s h y n t s % q f \x7f ~ W = 26 chars.
    #  So l a z y -> q f \x7f ~ ? l+5=q, a+5=f, z+5=~ (126), y+5=} (125). Hmm but we have \x7f (127) and ~ (126). 
    #  Wait z=122, +5=127=\x7f. y=121, +5=126=~. Yes! z->\x7f, y->~. So "lazy" -> "qf\x7f~" then W. 
    #  Great, consistent: shift +5, append "W".
    #  Check "abc123": a->f,b->g,c->h,1->6,2->7,3->8, +W = "fgh678W". Yes.
    #  Check "level": l->q,e->j,v->{,e->j,l->q,+W = "qj{jqW". Yes.
    #  Check " Zebralower": space->%,Z->_,e->j,b->g,r->w,a->f,l->q,o->t,w->|,e->j,r->w,+W = "%_jgwfqt|jwW". Yes.
    #  So: shift each char by +5 (mod 256? or just codepoint +5), then append "W".
    #  Need to determine mod behavior. For chars near 255, does it wrap? Unknown. Assume codepoint+5 without wrap for now, or mod 256? Mark with ?.
    def shift(c):
        return chr((ord(c) + 5) % 256)
    return {"outputs": ["".join(shift(c) for c in s) + "W" for s in probe["inputs"]]}
