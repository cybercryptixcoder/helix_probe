def predict(probe):
    # Model: each character is shifted by +3 in ASCII (Caesar cipher), then 'W' appended.
    # Evidence E1:
    #   "abc123" -> "fgh678W": a->f(+5?) wait check: a(97)->f(102) is +5? No: a->f is +5.
    #   Actually a->f = +5, b->g = +5, c->h = +5, 1->6 = +5, 2->7 = +5, 3->8 = +5. So +5.
    #   "level" -> "qj{jqW": l->q(+5), e->j(+5), v->{(+5), e->j, l->q. Yes +5.
    #   " Zebralower" -> "%_jgwfqt|jwW": space->%(+5), Z->_(+5), e->j, b->g, r->w, a->f, l->q, o->t, w->|, e->j, r->w. Yes +5.
    #   "Hello World function lazy" -> "Mjqqt%\twqi%kzshynts%qf~W": H->M(+5), e->j, l->q, l->q, o->t, space->%, W->\, o->t, r->w, l->q, d->i, space->%, f->k, u->z, n->s, c->h, t->y, i->n, o->t, n->s, space->%, l->q, a->f, z->~, y->}. Yes +5.
    #   "bananaUPPER" -> "gfsfsfZUUJW": b->g(+5), a->f, n->s, a->f, n->s, a->f, U->Z(+5), P->U, P->U, E->J. Yes +5.
    #   "Zebra" -> "_jgwfW": Z->_(+5), e->j, b->g, r->w, a->f. Yes +5.
    # So: shift each char +5 in ASCII, then append 'W'.
    def enc(s):
        return ''.join(chr(ord(c) + 5) for c in s) + 'W'
    return {"outputs": [enc(x) for x in probe["inputs"]]}
