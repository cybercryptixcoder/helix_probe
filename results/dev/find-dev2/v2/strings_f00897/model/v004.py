def predict(probe):
    # First char: letters a-v and A-V shift +2 [E1,E2,E3,E4]
    #   (u->w, v->x, t->v, s->u, a->c all +2; w->{ is +4)
    # First char: w,x,y,z and W,X,Y,Z shift +4 [E1,E2,E4]
    # First char: non-letters (space, digit, symbol) shift +4 [E1,E2]
    # All positions after index 0: shift +4 [E1,E2]
    def shift(s):
        out = []
        for i, ch in enumerate(s):
            if i == 0 and (('a' <= ch <= 'v') or ('A' <= ch <= 'V')):
                out.append(chr(ord(ch) + 2))
            else:
                out.append(chr(ord(ch) + 4))
        return ''.join(out)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
