def predict(probe):
    # First char of any string: +2 if it's a letter a-t or A-T, else +4 [E1, E2]
    # Wait — E3 shows u->w (+2), U->W (+2), t->v (+2), T->V (+2), s->u (+2), S->U (+2)
    # So u and U get +2 too! And s,S get +2. So the +2 range extends past t.
    # E2: z->~ (+4), x->| (+4). E1: w->{ (+4). So w,x,z get +4.
    # So +2 for a-v? u->+2, v? unknown, w->+4. Boundary between v and w?
    # Letters a-u get +2 (u confirmed +2), w,x,z get +4. v untested.
    # Non-letters (space, digit, symbol) get +4 [E1, E2].
    # All positions after index 0: +4 [E1, E2].
    def shift(s):
        out = []
        for i, ch in enumerate(s):
            if i == 0 and (('a' <= ch <= 'u') or ('A' <= ch <= 'U')):
                out.append(chr(ord(ch) + 2))
            else:
                out.append(chr(ord(ch) + 4))
        return ''.join(out)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
