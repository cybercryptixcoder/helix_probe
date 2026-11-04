def predict(probe):
    # Observations from E1:
    # - lowercase letters map via a Caesar-like shift: h->j, e->i, l->p, o->s (shift +2)
    #   hello -> jipps, world -> {svph (w->{, o->s, r->v, l->p, d->h) yes +2
    # - uppercase letters also shift +2: H->J, E->I, L->P, O->S (HELLO -> JIPPS)
    # - digits shift +2: test123 -> viwx567 (t->v,e->i,s->w,t->v, 1->5? wait)
    #   test123: t->v(+2), e->i(+2), s->w(+2), t->v(+2), 1->5(+4?), 2->6(+4?), 3->7(+4?)
    #   Hmm digits: 1->5,2->6,3->7 is +4. Let's check abc-def: a->c,b->f? no.
    #   abc-def -> cfg1hij: a->c(+2), b->f(+4?), c->g(+4?), - ->1, d->h(+4), e->i(+4), f->j(+4)
    #   Wait let me recheck: "abc-def" -> "cfg1hij"
    #   a->c (+2), b->f (+4), c->g (+4), '-'->'1', d->h (+4), e->i (+4), f->j (+4)
    #   Hmm inconsistent. Let me reconsider.
    #   Actually maybe it's shift by position index? 
    #   hello: h+2=j, e+4=i, l+4=p, l+4=p, o+4=s -> jipps. Yes! positions 0,1,2,3,4 shift +2,+4,+4,+4,+4? 
    #   Wait h->j is +2, e->i is +4, l->p is +4, l->p +4, o->s +4. 
    #   Hmm first char +2, rest +4? Check world: w+2={, o+4=s, r+4=v, l+4=p, d+4=h -> {svph. Yes!
    #   Check Hello: H+2=J, e+4=i, l+4=p, l+4=p, o+4=s -> Jipps. Yes!
    #   Check HELLO: H+2=J, E+4=I, L+4=P, L+4=P, O+4=S -> JIPPS. Yes!
    #   Check "two words": t+2=v, w+4={, o+4=s, space+4=$, w+4={, o+4=s, r+4=v, d+4=h, s+4=w -> v{s${svhw. Yes!
    #   Check "a b": a+2=c, space+4=$, b+4=f -> c$f. Yes!
    #   Check "  spaced  ": space+2=$, space+4=$, s+4=w, p+4=t, a+4=e, c+4=g, e+4=i, d+4=h, space+4=$, space+4=$ -> $$wtegih$$. Yes!
    #   Check test123: t+2=v, e+4=i, s+4=w, t+4=x, 1+4=5, 2+4=6, 3+4=7 -> viwx567. Yes!
    #   Check abc-def: a+2=c, b+4=f, c+4=g, -+4=1, d+4=h, e+4=i, f+4=j -> cfg1hij. Yes!
    #   Check x: x+2=z? but observed "|". x is 120, +2=122='z'. But observed '|' (124). Hmm.
    #   Wait x->| is +4? x=120, |=124, +4. But first char should be +2. 
    #   Hmm. Let me reconsider: maybe single char gets +4? Or maybe x+2=z but z... no.
    #   Actually maybe shift is +2 for first, +4 for rest, but x is special? x+2=z, z+2=|? No.
    #   Let me reconsider: maybe it's +2 for position 0, +4 for others. x at pos 0 -> +2 = z. But observed |.
    #   Unless... the shift wraps or x is at boundary. x=120, +2=122 z. Not |.
    #   Hmm, maybe the first char shift is +2 but for x specifically... Let me check: is it possible the rule is +2 for first char, but x->| means +4. 
    #   Wait, maybe I misread. "x" -> "|". x is 120, | is 124. That's +4.
    #   Could the rule be: shift +2 if position 0 AND ... hmm. Or maybe shift depends on something else.
    #   Let me reconsider all: maybe it's +2 for first char only when length>1? For single char "x", maybe +4?
    #   Actually maybe the rule is: each char shifted by 2 + 2*(index>0)? For index 0: +2. For index>0: +4. x at index 0 -> +2 = z. But observed |.
    #   Alternatively maybe the shift is +2 for first, +4 for rest, but there's wrapping in some range. x+2=z, but maybe z is excluded and wraps? No.
    #   Let me reconsider: maybe it's not +2/+4 by position. Let me check "a b": a->c (+2), space->$ (+4), b->f (+4). Yes pos-based.
    #   For "x": x->| is +4. So maybe single character gets +4? Or maybe the first char rule is +2 only if there's a next char?
    #   Hmm, or maybe the rule is: shift +2 for index 0, +4 for index>=1, but for a single char it's treated as index>=1? Unlikely.
    #   Alternatively: maybe the shift is +2 for the first character, but "x" -> "|" suggests +4. Could there be an off-by-one: shift = 2 + 2*min(index,1)? For index 0: +2, index>=1: +4. x index 0 -> +2 = z. Still not |.
    #   Wait, maybe I should reconsider: is it possible the shift is +2 for index 0, +4 for others, and x->| because... x=120, +2=122='z'. But maybe the observed is actually 'z'? No, it says "|".
    #   Let me reconsider: maybe the rule is different. What if it's +2 for first char, +4 for rest, but the alphabet for shifting is different? 
    #   Actually, let me reconsider "x". Maybe the rule is: shift by 2 + 2*(index) capped? No.
    #   Hmm, what if the shift is +2 for index 0, +4 for index 1, +6 for index 2...? Let's check hello: h+2=j, e+4=i, l+6=r? but observed p. No.
    #   What if shift is +2 for index 0, +4 for all others, and x->| is an anomaly? Or maybe single char treated as index 1?
    #   Let me just go with: shift = 2 if index==0 else 4, but for length 1 use 4? That's ad hoc.
    #   Actually wait: maybe the rule is shift = 2 + 2*(index>0), and for "x" the result should be "z" but observed "|". 
    #   Let me reconsider: x is 120. | is 124. Difference 4. If index 0 shift is +2, we'd get 122='z'. 
    #   Unless the shift for index 0 is +2 but there's an additional rule... 
    #   Hmm, what if the rule is: shift by 2 for first char, but if the char is 'x' or beyond... no.
    #   Let me reconsider: maybe the shift is +2 for index 0, +4 for index>0, but the "first char" is determined differently. 
    #   Actually, maybe I'm wrong about "x". Let me reconsider: could the rule be +4 for ALL chars except... no, hello shows h+2=j.
    #   OK here's another thought: maybe the shift is +2 for index 0, +4 for index>0, and for single-char strings the index 0 char gets +4 because... hmm.
    #   Or maybe the rule is: shift = 2 + 2*(index>0), but there's a special case where if the string has length 1, shift is +4.
    #   Let me just test: for "x" (len 1), output "|" = x+4. So maybe len 1 -> +4.
    #   I'll go with: shift = 2 if (index==0 and len>1) else 4. Let me verify all:
    #   hello len 5: h+2=j, e+4=i, l+4=p, l+4=p, o+4=s. Yes.
    #   x len 1: x+4=|. Yes.
    #   All others len>1, index 0 +2, rest +4. Yes.
    #   This is a guess but fits all data.
    # Shift applies to ASCII codes directly (spaces, digits, symbols all shift).
    def shift(s):
        out = []
        n = len(s)
        for i, ch in enumerate(s):
            if i == 0 and n > 1:
                out.append(chr(ord(ch) + 2))
            else:
                out.append(chr(ord(ch) + 4))
        return ''.join(out)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
