def predict(probe):
    # Rule: shift each char forward by 1, BUT only if it's lowercase a-z [E1,E2]
    #   'a'->'b', ..., 'z'->'{'  (lowercase shifts)
    #   Uppercase A-Z unchanged [E1: "Hello"->"Ifmmp" wait...]
    # Re-examine E1: "Hello World function lazy" -> "Ifmmp!xpsme!gvodujpo!mb{z"
    #   'H'->'I' (upper shifts!), 'e'->'f', 'l'->'m', 'o'->'p' ... so upper DOES shift
    #   'W'->'x'? No: "World"->"xpsme" means 'W'->'x' (lowercase!). So case flips?
    # Actually: H->I (upper->upper +1), e->f, l->m, o->p => "Hello"->"Ifmmp" all +1
    # "World"->"xpsme": W->x (+1 but becomes lower), o->p, r->s, l->m, d->e
    #   W(87)->x(120)? No. W->x is +33. Hmm.
    # Wait "Hello World" -> "Ifmmp!xpsme": H->I, e->f, l->m, l->m, o->p, space->!, W->x, o->p, r->s, l->m, d->e
    #   W->x: ord('W')=87, ord('x')=120, diff 33. But o->p is +1. Inconsistent!
    # Recheck: maybe "World"->"xpsme" means W->x. Let me recount: x p s m e = 5 chars, World = 5.
    #   W->x, o->p, r->s, l->m, d->e. W->x is +33? That's weird.
    # OR the shift is +1 but W->X->... no.
    # Hmm, actually maybe it's: lowercase->lowercase+1, uppercase->lowercase+1? 
    #   H(72)->i(105)? No, output is I(73). So H->I is +1.
    # Let me just trust: all chars +1 EXCEPT... E2 shows "test case"->"Uftu!dbtf"
    #   t->U? t(116)->U(85)? No. "test"->"Uftu": t->U, e->f, s->t, t->u
    #   t->U is -31. But e->f is +1, s->t is +1, t->u is +1.
    # So FIRST char of each word gets special treatment? "test"->"Uftu": first t->U (uppercase!)
    # "case"->"dbtf": c->d (+1, stays lower). Hmm inconsistent.
    # "banana"->"Cbobob": b->C (upper!), a->b, n->o, a->b, n->o, a->b
    # "level"->"Mfwfm": l->M (upper!), e->f, v->w, e->f, l->m
    # "lazy"->"Mb{z": l->M (upper!), a->b, z->{, y->z
    # "Example123"->"Fybnqmf234": E->F (+1 upper), x->y, a->b, m->n, p->q, l->m, e->f, 1->2,2->3,3->4
    # So: FIRST character of the string is uppercased (if letter), rest shift +1!
    # "abc123"->"Bcd234": a->B (upper!), b->c, c->d, 1->2,2->3,3->4 ✓
    # "level"->"Mfwfm": l->M ✓
    # " Zebralower"->"!{fcsbmpxfs": space->!, Z->{? Z(90)->{(123) +33. Hmm.
    #   Wait first char is space -> '!'. Then Z->{? That breaks "first char upper" rule.
    #   Actually maybe: first char shifts +1, AND if it becomes lowercase letter, uppercase it?
    #   space->! (not letter). Z->{ : Z+1=[ not {. So Z->{ is +33.
    #   Hmm. Let me reconsider " Zebralower"->"!{fcsbmpxfs"
    #   space->!, Z->{, e->f, b->c, r->s, a->b, l->m, o->p, w->x, e->f, r->s
    #   Z->{: Z(90), {(123). diff 33. But e->f is +1. 
    #   Unless Z->{ is actually... no.
    #   Wait maybe it's case-flip then +1? Z->z->{? Z->z is lowercase, +1 = {. Yes!
    #   Check "Hello": H->I. H->h->i? No, output is I not i.
    # Hmm. Let me check "Zebra"->"[fcsb": Z->[, e->f, b->c, r->s, a->b
    #   Z->[ : Z(90)->[(91) +1! OK so Z->[ is +1.
    # So in " Zebralower", Z->{ is NOT +1. Contradiction with "Zebra"->"[fcsb".
    #   Unless first char of string: space->!, then... Z is 2nd char. Z->{?
    #   Wait maybe I misread. "!{fcsbmpxfs" vs " Zebralower"
    #   space->!, Z->{, e->f, b->c, r->s, a->b, l->m, o->p, w->x, e->f, r->s
    #   That's 11 in, 11 out. Z->{ stands. But "Zebra"->"[fcsb" has Z->[.
    #   Difference: in " Zebralower" Z is not first char; in "Zebra" Z is first char.
    #   First char: Z->[ (+1). Non-first: Z->{? 
    #   Hmm but "banana"->"Cbobob": b(first)->C, a->b, n->o... a->b is +1.
    #   Let me hypothesize: FIRST char gets uppercased after +1? 
    #     b+1=c, uppercase=C ✓. Z+1=[, not letter, stays [ ✓ (Zebra->[fcsb)
    #     space+1=!, not letter, stays ! ✓. Then Z (2nd char) -> should be +1 = [. But observed {.
    #   I'm confused. Let me just go with: first char: +1 then uppercase if letter; rest: +1.
    #   For " Zebralower": space->!, Z->[ expected but got {. 
    #   Maybe the rule is different. Given uncertainty, implement: first char +1 and uppercase-if-letter, rest +1. Mark Z->{ as ?.
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append("")
            continue
        r = []
        c0 = s[0]
        n0 = chr(ord(c0) + 1)
        if 'a' <= n0 <= 'z':
            n0 = n0.upper()
        r.append(n0)
        for c in s[1:]:
            r.append(chr(ord(c) + 1))
        out.append("".join(r))
    return {"outputs": out}
