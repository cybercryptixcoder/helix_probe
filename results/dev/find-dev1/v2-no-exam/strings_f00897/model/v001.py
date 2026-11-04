def predict(probe):
    # Each character is shifted by +2 in ASCII [E1: a->c, A->C, 1->5, space->$, !->%]
    # 'ab'->'cf', 'AB'->'CF', '12'->'56', 'a b'->'c$f' all consistent with +2 per char
    # 'Hello, World!' -> 'Jipps0$[svph%' : H->J(+2), e->g(+2), l->n(+2), l->n(+2), o->q(+2),
    #   ,->0(+2), space->$(+2), W->Y? but observed '[' ... let's check: W(87)->[ (91) is +4?
    # Wait: 'Hello, World!' chars: H e l l o , _ W o r l d !
    #   H->J +2, e->g +2, l->n +2, l->n +2, o->q +2, ,->0 +2, space->$ +2,
    #   W->[ : W=87, [=91 => +4. Hmm inconsistent.
    # Recheck observed: "Jipps0$[svph%" length 12. Input "Hello, World!" length 13.
    # So one char dropped. Let's align: H->J, e->i? no.
    # Actually maybe it's +2 but 'l'->'p'? Let's map: J i p p s 0 $ [ s v p h %
    # H->J(+2), e->i(+4)? no e->i is +4.
    # Try: each char +2: H->J, e->g, l->n, l->n, o->q, ,->0, space->$, W->Y, o->q, r->t, l->n, d->f, !->%
    # = "Jgnnq0$Yqtnf%" not matching.
    # Observed "Jipps0$[svph%": J i p p s 0 $ [ s v p h %
    # H->J +2, e->i +4, l->p +4, l->p +4, o->s +4, ,->0 +2, space->$ +2, W->[ +4, o->s +4, r->v +4, l->p +4, d->h +4, !->% +2
    # Pattern: letters shift +4, non-letters shift +2? Check 'a'->'c' +2 (letter!). Contradiction.
    # Hmm 'a'->'c' is +2. But 'e'->'i' is +4.
    # Maybe it's +2 for lowercase a, but +4 for others? Unlikely.
    # Alternative: maybe it's not ASCII shift. 'a'->'c', 'A'->'C', '1'->'5', ' '->'$', '!'->'%'
    # 1->5 is +4, not +2! '1'=49, '5'=53, +4. space=32, $=36, +4. !=33, %=37, +4.
    # a=97, c=99, +2. A=65, C=67, +2.
    # So digits/spaces/punct shift +4, letters shift +2? Check 'ab'->'cf': a->c +2, b->f +4? b=98,f=102,+4. Inconsistent within word.
    # Hmm 'ab'->'cf': a->c(+2), b->f(+4). 'AB'->'CF': A->C(+2), B->F(+4).
    # '12'->'56': 1->5(+4), 2->6(+4). 'a b'->'c$f': a->c(+2), space->$(+4), b->f(+4).
    # So first char +2, subsequent chars +4? 'Hello, World!': H->J(+2), then e->i(+4), l->p(+4), l->p(+4), o->s(+4), ,->0(+4), space->$(+4), W->[(+4), o->s(+4), r->v(+4), l->p(+4), d->h(+4), !->% (+4)
    # That gives 13 chars: "Jipps0$[svph%" - wait that's J i p p s 0 $ [ s v p h % = 13 chars!
    # Let me recount observed: "Jipps0$[svph%" -> J,i,p,p,s,0,$,[,s,v,p,h,% = 13. Yes!
    # So rule: first character +2, all subsequent characters +4 (ASCII).
    # Check 'a'->'c' +2 (single char, first). 'A'->'C' +2. '1'->'5' +4? single char should be +2!
    # 1->5 is +4. Contradiction with "first char +2".
    # Hmm. '1' single char -> '5' +4. 'a' single -> 'c' +2. 'A' single -> 'C' +2. ' ' -> '$' +4. '!' -> '%' +4.
    # So single letters +2, single non-letters +4.
    # 'ab': a->c +2 (letter), b->f +4? b is letter but +4. Hmm.
    # Maybe: shift depends on position AND type? a is pos0 letter +2, b pos1 letter +4.
    # '1' pos0 digit +4. So pos0: letter +2, non-letter +4. pos>=1: +4 always.
    # Check 'AB': A pos0 letter +2 ->C, B pos1 +4 ->F. Yes.
    # '12': 1 pos0 digit +4 ->5, 2 pos1 +4 ->6. Yes.
    # 'a b': a pos0 letter +2->c, space pos1 +4->$, b pos2 +4->f. Yes.
    # 'Hello, World!': H pos0 letter +2->J, rest +4. e->i,l->p,l->p,o->s,,->0,space->$,W->[,o->s,r->v,l->p,d->h,!->%. Yes!
    # Rule: char at index 0: if letter, +2; else +4. All other indices: +4.
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, ch in enumerate(s):
            if i == 0 and ch.isalpha():
                r.append(chr(ord(ch) + 2))
            else:
                r.append(chr(ord(ch) + 4))
        out.append("".join(r))
    return {"outputs": out}
