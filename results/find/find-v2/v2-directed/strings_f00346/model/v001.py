def predict(probe):
    # Letters shift +1 in alphabet, preserving case [E1]
    # 'h'->'j', 'e'->'f'... wait: hello->jello. h->j, e->f, l->l, l->l, o->o? No.
    # hello -> jello: h->j (+2), e->e (0), l->l, l->l, o->o. Hmm.
    # Actually "hello"->"jello": only first letter changes? h->j. rest same.
    # "Hello"->"Jello": H->J. "HELLO"->"JELLO": H->J only? E->E,L->L,L->L,O->O. Yes only first char.
    # "two words"->"vwowords": t->v(+2), w->w, o->o, space removed, w->w,o->o,r->r,d->d,s->s
    #   Wait "two words" -> "vwowords". t->v (+2), w->w, o->o, then space gone, w,o,r,d,s same.
    # "two  words"->"vwowords": same, double space collapsed/removed.
    # "123"->"123": digits unchanged.
    # "A1!"->"C1!": A->C (+2), 1, ! unchanged.
    # " hello"->"jello": leading space removed, then hello->jello (h->j +2).
    # "hello "->"jello": trailing space removed.
    # "hello!"->"jello!": ! unchanged.
    # So: remove all spaces. Then first letter shifts +2 in alphabet (case preserved). Rest unchanged.
    # Check "two words": remove spaces -> "twowords". First letter t->v (+2). -> "vwowords". Yes!
    # "hello"->"hello", h->j -> "jello". Yes.
    # "A1!"->"A1!", A->C -> "C1!". Yes.
    # So rule: strip spaces, shift first character +2 if it's a letter.
    s = probe["inputs"]
    out = []
    for x in s:
        y = x.replace(" ", "")
        if y and y[0].isalpha():
            c = y[0]
            if c.islower():
                y = chr((ord(c) - ord('a') + 2) % 26 + ord('a')) + y[1:]
            else:
                y = chr((ord(c) - ord('A') + 2) % 26 + ord('A')) + y[1:]
        out.append(y)
    return {"outputs": out}
