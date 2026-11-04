def predict(probe):
    # Observations:
    # - First character: shift +2 if it's in 'a'-'v' or 'A'-'V', else shift +4 [E1, E2, E3]
    #   Evidence: a,b,l,t,f,H,E -> +2; Z, space, w -> +4
    # - All other characters: shift +4 [E1, E2, E3]
    # - "abc123" -> "cfg567": a->c(+2), b->f(+4), c->g(+4), 1->5(+4), 2->6(+4), 3->7(+4)
    # - "level" -> "nizip": l->n(+2), e->i(+4), v->z(+4), e->i(+4), l->p(+4)
    # - " Zebralower" -> "$^ifveps{iv": space->$(+4), Z->^(+4), rest +4
    # - "Hello World function lazy" -> "Jipps$[svph$jyrgxmsr$pe~}": H->J(+2), rest +4
    # - "Zebra" -> "^ifve": Z->^(+4), rest +4
    # - "world42" -> "{svph86": w->{(+4), rest +4  [E3: key fix]
    # - "aMiXeD" -> "cQm\\iH": a->c(+2), M->Q(+4), i->m(+4), X->\\(+4), e->i(+4), D->H(+4)
    def transform(s):
        out = []
        for i, c in enumerate(s):
            if i == 0 and (('a' <= c <= 'v') or ('A' <= c <= 'V')):
                shift = 2
            else:
                shift = 4
            out.append(chr(ord(c) + shift))
        return ''.join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
