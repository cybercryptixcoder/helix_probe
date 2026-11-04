def predict(probe):
    # Observations from E1:
    # - Lowercase letters shift by +1 in the alphabet: h->i, e->f, l->m, o->p [E1]
    # - Uppercase letters shift by +1: H->I, E->F, L->M, O->P [E1]
    # - Vowels (a,e,i,o,u) become 'Y' regardless of case? Check: a->Y, e->Y, o->Y [E1]
    #   Wait: "hello" -> "ifYmmp": h->i, e->Y, l->m, l->m, o->Y. So e->Y, o->Y.
    #   "cat" -> "dYbu": c->d, a->Y, t->u. So a->Y.
    #   "dog" -> "eYph": d->e, o->Y, g->h. o->Y.
    #   "test" -> "ufYtu": t->u, e->Y, s->t, t->u. e->Y.
    #   "a" -> "Yb": a->Y, then extra 'b'? Hmm "a"->"Yb" is 2 chars.
    #   "ab" -> "bYc": a->b? no. Let's re-examine.
    #
    # Re-examine carefully:
    # hello -> ifYmmp (6 chars from 5)
    # world -> xpYsme (6 chars from 5)
    # cat -> dYbu (4 chars from 3)
    # dog -> eYph (4 chars from 3)
    # test -> ufYtu (5 chars from 4)
    # a -> Yb (2 chars from 1)
    # ab -> bYc (3 chars from 2)
    # abc -> bYcd (4 chars from 3)
    # Hello -> IfYmmp (6 chars from 5)
    # HELLO -> IFYMMP (6 chars from 5)
    #
    # Pattern: each input char maps to 1 char, but there's an extra char inserted.
    # hello: h->i, e->f, l->m, l->m, o->p would be "ifmmp". Observed "ifYmmp".
    #   So position 1 (0-indexed) 'e'->'Y' instead of 'f'. Vowel e->Y.
    # world: w->x, o->p, r->s, l->m, d->e = "xpsme". Observed "xpYsme".
    #   Position 1 'o'->'Y'. Vowel o->Y.
    # cat: c->d, a->b, t->u = "dbu". Observed "dYbu". Position 1 'a'->'Y'.
    # dog: d->e, o->p, g->h = "eph". Observed "eYph". Position 1 'o'->'Y'.
    # test: t->u, e->f, s->t, t->u = "uftu". Observed "ufYtu". Position 1 'e'->'Y'.
    # a: a->b = "b". Observed "Yb". Hmm, position 0 'a'->'Y'? Then 'b' appended?
    #   Actually "a" -> "Yb": maybe a->Y, then shift a->b appended? Or: vowel at pos0 -> Y, then...
    # ab: a->b, b->c = "bc". Observed "bYc". Position 1 'b'->'Y'? b is not vowel.
    #   Hmm. "ab" -> "bYc". If a->b, b->Y, c? That's 3 chars.
    #   Maybe: a->b, insert Y, b->c? "bYc". Yes! Insert Y after position 0.
    # abc: a->b, b->c, c->d = "bcd". Observed "bYcd". Insert Y after position 0: "bYcd". Yes!
    # a: a->b = "b". Insert Y after position 0: "bY"? But observed "Yb".
    #   Hmm. "a"->"Yb". Maybe for length 1, Y comes first?
    #   Or: a->Y (vowel), then... "Yb"? 
    #   Let's reconsider: maybe rule is: shift each char +1, but vowels become Y, AND insert Y at position 1 (after first char).
    #   hello: i f m m p -> insert Y at pos1: i Y f m m p = "iYfmmp". But observed "ifYmmp".
    #   So insert at pos 2? i f Y m m p = "ifYmmp". Yes!
    #   world: x p s m e -> insert Y at pos2: x p Y s m e = "xpYsme". Yes!
    #   cat: d b u -> insert Y at pos2: d b Y u = "dbYu". But observed "dYbu".
    #   Hmm, "dYbu" has Y at pos1.
    #   Wait, maybe vowels become Y in place, no insertion.
    #   cat: c->d, a->Y, t->u = "dYu". Observed "dYbu" (4 chars). Extra 'b'.
    #   Hmm.
    #
    # Let me recount. "cat" -> "dYbu". d,Y,b,u = 4 chars.
    #   c->d, a->Y, t->u gives "dYu" (3). Where's 'b'?
    #   Maybe a->Y and also insert b? 
    #   Or: c->d, a->b, t->u = "dbu", then insert Y at pos1: "dYbu". Yes!
    #   So: shift +1, then insert Y at position 1.
    #   hello: i f m m p, insert Y at pos1: "ifYmmp"? i,Y,f,m,m,p = "iYfmmp". No, observed "ifYmmp".
    #   Hmm inconsistent.
    #
    # Let me try: shift +1, vowels become Y, then insert Y at position 1.
    #   hello: h->i, e->Y, l->m, l->m, o->Y = "iYm mY" = "iYmmY". Insert Y at pos1: "iYYmmY". No.
    #
    # Try: shift +1, insert Y at position 1, then vowels become Y.
    #   hello: i f m m p -> insert Y pos1: i Y f m m p -> vowels: i,Y,f,m,m,p (no vowels) = "iYfmmp". Observed "ifYmmp". No.
    #
    # Try: shift +1, insert Y at position 2.
    #   hello: ifmmp -> ifYmmp. Yes!
    #   world: xpsme -> xpYsme. Yes!
    #   cat: dbu -> dbYu. Observed "dYbu". No.
    #   Hmm.
    #
    # Wait, maybe I misread. "cat" -> "dYbu". Let me check: c+1=d, a+1=b, t+1=u. "dbu". Insert Y at pos1: "dYbu". Yes!
    #   hello: "ifmmp", insert Y at pos1: "iYfmmp". But observed "ifYmmp".
    #   Difference: hello has Y at pos2, cat has Y at pos1.
    #   Length of hello=5, cat=3. Maybe insert position depends on length?
    #   world=5 -> Y at pos2. test=4 -> "ufYtu", Y at pos2. dog=3 -> "eYph", Y at pos1. cat=3 -> pos1.
    #   ab=2 -> "bYc", Y at pos1. abc=3 -> "bYcd", Y at pos1. a=1 -> "Yb", Y at pos0.
    #   hello=5 -> pos2. world=5 -> pos2. test=4 -> pos2. cat=3 -> pos1. dog=3 -> pos1. abc=3 -> pos1. ab=2 -> pos1. a=1 -> pos0.
    #   So insert position = floor(length/2)? 
    #   len1: 0. len2: 1. len3: 1. len4: 2. len5: 2. Yes! floor(len/2).
    #   Check: hello len5, floor(5/2)=2. "ifmmp" insert Y at 2: "ifYmmp". Yes!
    #   world len5: "xpsme" insert Y at 2: "xpYsme". Yes!
    #   test len4: "uftu" insert Y at 2: "ufYtu". Yes!
    #   cat len3: "dbu" insert Y at 1: "dYbu". Yes!
    #   dog len3: "eph" insert Y at 1: "eYph". Yes!
    #   abc len3: "bcd" insert Y at 1: "bYcd". Yes!
    #   ab len2: "bc" insert Y at 1: "bYc". Yes!
    #   a len1: "b" insert Y at 0: "Yb". Yes!
    #
    # Now case: Hello -> IfYmmp. H->I, e->f, l->m, l->m, o->p = "Ifmmp", insert Y at 2: "IfYmmp". Yes!
    #   HELLO -> IFYMMP. H->I, E->F, L->M, L->M, O->P = "IFMMP", insert Y at 2: "IFYMMP". Yes!
    #   So case preserved, shift +1 in alphabet, wrap? Need to test z->? and Z->?
    #   Also non-letters? Need to test.
    #
    # Rule: for each char, shift +1 in alphabet (preserving case), then insert 'Y' at index floor(len/2).
    #   Wrap-around: z->a? Z->A? Unknown, guess wrap.
    #   Non-letters: unknown, guess unchanged.
    
    import math
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c
    
    results = []
    for s in probe.get("inputs", []):
        shifted = ''.join(shift(c) for c in s)
        pos = len(s) // 2
        out = shifted[:pos] + 'Y' + shifted[pos:]
        results.append(out)
    return {"outputs": results}
