def predict(probe):
    # Mechanism: for each character, shift its Unicode code point by +1,
    # EXCEPT letters are case-mapped to the opposite case before shifting.
    # Evidence:
    #  - 'abc123' -> 'Bcd234': a->B (+1 and upper), b->c, c->d, digits +1.
    #  - 'ABC' -> 'Bcd': A->B, B->c, C->d (uppercase letters become lowercase after shift).
    #  - 'xyz' -> 'Yz{': x->Y, y->z, z->{ (shift past 'z').
    #  - 'Zebra' -> '[fcsb': Z->[ (shift past 'Z'), e->f, etc.
    #  - 'a b' -> 'B!c': space (0x20) -> '!' (0x21).
    #  - 'a-b' -> 'B.c', 'a.b' -> 'B/c', 'a_b' -> 'B`c': symbols shift +1.
    #  - '9!?' -> ':"@': '9'->':', '!'->'"', '?'->'@'.
    #  - 'az' -> 'B{': a->B (upper), z->{.
    #  - 'AZ' -> 'B{': A->B, Z->[? Wait E4 says 'AZ'->'B{'.
    #    Hmm: A->B, Z->? E4 'AZ' -> 'B{'. So Z->{ means +1 but '{' is 0x7b, Z is 0x5a.
    #    That's not +1. Let's recheck: 'Zebra'->'[fcsb': Z->'[' (0x5b), +1.
    #    But 'AZ'->'B{': A->B (+1), Z->'{'? That contradicts.
    #    Wait, 'AZ' output is "B{" — maybe A->B and Z->{? Z+1 = '['. '{' is 'z'+1.
    #    So maybe uppercase letters are lowercased then shifted? A->a->b? No, A->B.
    #    Let's reconsider: maybe letters toggle case THEN shift.
    #    'abc'->'Bcd': a->A->B? or a->B directly.
    #    'ABC'->'Bcd': A->a->b? No, output B. A->B.
    #    Hmm 'AZ'->'B{': A->B, Z->{ means Z->z->{ (lowercase then shift).
    #    'ABC'->'Bcd': A->B, B->c, C->d. B->b->c? yes! C->c->d? yes!
    #    So uppercase to lowercase then +1: A->a->b? But output is B not b.
    #    Wait 'Bcd': B, c, d. A->B (uppercase B). B->c (lowercase c). C->d.
    #    So A->B: uppercase stays uppercase? No...
    #    Let's look at 'Zz'->'[{': Z->'[', z->'{'. So Z+1='[', z+1='{'. Simple +1!
    #    Then 'AZ'->'B{' must be A->B (+1) and Z->{ ... but Z+1='['.
    #    Contradiction. Unless 'AZ' is actually A->B and Z->{? Let me re-read E4.
    #    E4: "az","AZ","09","aZ","Zz","Aa","zA","a9","9a","!~"
    #    -> "B{","B{","1:","B{","[{","Bb","[b","B:",":b","\"\u007f"
    #    So az->B{, AZ->B{, aZ->B{, Zz->[{, Aa->Bb, zA->[b.
    #    'aZ'->'B{' : a->B, Z->{. So Z->{.
    #    'Zz'->'[{': Z->'[', z->'{'. So Z->'[' here!
    #    Contradiction: Z->{ in aZ, Z->[ in Zz.
    #    Unless... it's not per-character independent. Maybe case toggling?
    #    Let's think: maybe the rule is: toggle case, then shift +1? 
    #    a->A->B? A+1=B yes. z->Z->[ yes! (Z+1='['). 
    #    'az'->B{: a->A->B, z->Z->[? But output is '{' not '['.
    #    Hmm no.
    #    Try: shift +1, then toggle case if letter?
    #    a+1=b, toggle->B. z+1={, not letter, stays {. az->B{. ✓
    #    A+1=B, toggle->b? But AZ->B{. A->B ✓ (output B, not b). Hmm toggle would give b.
    #    Maybe: if lowercase, +1 then uppercase; if uppercase, +1 then lowercase?
    #    a->b->B ✓. z->{->{ ✓. A->B->b ✗ (output B).
    #    Hmm.
    #    Let's tabulate single chars from evidence:
    #    a->B, b->c, c->d, d->e (from abc->Bcd, banana->Cbobob: b->c,a->B,n->o,a->B,n->o,a->B)
    #    Wait banana->Cbobob: b->C? No: b->C, a->b, n->o, a->b, n->o, a->b.
    #    Hmm that's different! 'banana'->'Cbobob': b->C, a->b, n->o.
    #    But 'abc'->'Bcd': a->B, b->c, c->d.
    #    So 'a'->B in abc but 'a'->b in banana? Inconsistent per-char!
    #    Let's recheck banana: E3 'banana'->'Cbobob'. b->C, a->b, n->o, a->b, n->o, a->b.
    #    And 'abc'->'Bcd': a->B, b->c, c->d.
    #    So position matters? First char special?
    #    In 'abc': pos0 a->B, pos1 b->c, pos2 c->d.
    #    In 'banana': pos0 b->C, pos1 a->b, pos2 n->o, pos3 a->b, pos4 n->o, pos5 a->b.
    #    So pos0: a->B, b->C: +1 and uppercase. Other positions: a->b, b->c: +1 lowercase.
    #    Check 'ABC'->'Bcd': pos0 A->B (upper), pos1 B->c (lower), pos2 C->d (lower). ✓
    #    Check 'xyz'->'Yz{': pos0 x->Y (upper), pos1 y->z, pos2 z->{. ✓
    #    Check 'Zebra'->'[fcsb': pos0 Z->[ (upper +1 = [), pos1 e->f, etc. ✓
    #    Check 'Hello World function lazy'->'Ifmmp!xpsme!gvodujpo!mb{z':
    #      H->I (upper), e->f, l->m, l->m, o->p, space->!, W->x (lower!), o->p...
    #      Wait W->x: W+1=X, lowercase->x. ✓ pos after space? It's pos6.
    #      So rule: pos0 uppercase+1, all other positions lowercase+1 (for letters)?
    #      But 'World' W is not pos0 of string, it's after space. W->x (lowercase).
    #      And 'function' f->g (lowercase, f+1=g). ✓
    #    Check 'Example123'->'Fybnqmf234': E->F (upper), x->y, a->b, m->n, p->q, l->m, e->f, 1->2,2->3,3->4. ✓
    #    Check 'test case'->'Uftu!dbtf': t->U (upper), e->f,s->t,t->u, space->!, c->d,b->c,a->b,s->t,e->f. ✓
    #    Check 'level'->'Mfwfm': l->M (upper), e->f,v->w,e->f,l->m. ✓
    #    Check 'aMiXeD'->'Bnjyfe': a->B (upper), M->n (lower), i->j, X->y, e->f, D->e. ✓
    #    Check 'Zz'->'[{': Z->[ (upper+1), z->{ (lower+1). ✓
    #    Check 'AZ'->'B{': A->B (upper+1), Z->{ (lower+1: Z->z? No, Z+1='['... hmm).
    #      Wait Z lowercased is z, z+1={. Yes! So for non-first letters: lowercase the char then +1.
    #      Z->z->{ ✓.
    #    Check 'aZ'->'B{': a->B (upper+1), Z->z->{ ✓.
    #    Check 'Aa'->'Bb': A->B (upper+1), a->b (lower+1) ✓.
    #    Check 'zA'->'[b': z->[ (upper+1: z->Z->[), A->a->b (lower+1) ✓.
    #    Check 'a9'->'B:': a->B, 9->: ✓.
    #    Check '9a'->':b': 9->:, a->b (lower+1) ✓.
    #    Check '!~'->'"\x7f': !->", ~->\x7f ✓.
    #    Check '0123'->'1234': 0->1,1->2,2->3,3->4 ✓ (digits +1, case doesn't apply).
    #    Check '9!?'->':"@': 9->:, !->", ?->@ ✓.
    #    Check 'a-b'->'B.c': a->B, -->., b->c ✓.
    #    Check 'a.b'->'B/c': .->/ ✓.
    #    Check 'a_b'->'B`c': _->` ✓.
    #    Check 'a b'->'B!c': space->! ✓.
    #    Check 'a1b'->'B2c': 1->2 ✓.
    #    Check 'ABC'->'Bcd': A->B, B->b->c, C->c->d ✓.
    #    Check 'bananaUPPER'->'Cbobobvqqfs': b->C, a->b,n->o,a->b,n->o,a->b, U->v (u+1), P->q, P->q, E->f, R->s ✓.
    #    Check 'racecar Example racecar'->'Sbdfdbs!fybnqmf!sbdfdbs':
    #      r->S, a->b,c->d,e->f,c->d,a->b,r->s, space->!, E->f (e+1), x->y... ✓
    #    Check 'world42'->'Xpsme53': w->X, o->p,r->s,l->m,d->e,4->5,2->3 ✓.
    #    Check 'Example '->'Fybnqmf!': trailing space->! ✓.
    #    Check 'banana a data '->'Cbobob!b!ebub!': ✓.
    #    Check 'function Hello World'->'Gvodujpo!ifmmp!xpsme': f->G, u->v,n->o,c->d,t->u,i->j,o->p,n->o, space->!, H->i (h+1), e->f... ✓.
    #    Check ' Zebralower'->'!{fcsbmpxfs': space->!, Z->{ (z+1), e->f,b->c,r->s,a->b,l->m,o->p,w->x,e->f,r->s ✓.
    #    Check 'Hello World function lazy'->'Ifmmp!xpsme!gvodujpo!mb{z': ✓.
    #    Check 'level'->'Mfwfm' ✓.
    #
    # Final rule:
    #   For each character c at position i:
    #     if c is a letter:
    #       if i == 0: result = chr(ord(c.upper()) + 1)   # uppercase then +1
    #       else:      result = chr(ord(c.lower()) + 1)   # lowercase then +1
    #     else:
    #       result = chr(ord(c) + 1)
    #   (No wrapping; just +1 in code point.)
    #
    # Edge: what about non-letters at position 0? Evidence '0123'->'1234': 0->1 (+1). '9!?'->':"@': 9->: (+1). '!~'->'"\x7f': !->" (+1). So non-letters always +1.
    # Edge: empty string -> empty string (no evidence, but natural).

    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        if not isinstance(s, str):
            s = str(s)
        out_chars = []
        for i, c in enumerate(s):
            if c.isalpha():
                if i == 0:
                    out_chars.append(chr(ord(c.upper()) + 1))
                else:
                    out_chars.append(chr(ord(c.lower()) + 1))
            else:
                out_chars.append(chr(ord(c) + 1))
        outputs.append("".join(out_chars))
    return {"outputs": outputs}
