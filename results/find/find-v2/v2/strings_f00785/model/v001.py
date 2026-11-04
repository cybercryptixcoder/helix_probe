def predict(probe):
    # First letter: shifted up by 1 (a->b, H->I, Z->A, space->space?) [E1]
    # Last letter: appended 'y' [E1]
    # Second letter: shifted up by 1 (b->c, e->m? no...) [E1]
    # Let's look: "abc123"->"bbc123y": a->b, b->b? Actually first char a->b, second b->b?
    # "level"->"mevely": l->m, e->e? v->v? e->e? l->l? +y
    # "Zebra"->"Aebray": Z->A, e->e, b->b, r->r, a->a, +y
    # "Hello World..."->"Iello World...": H->I, rest same, +y
    # "bananaUPPER"->"cananaUPPER": b->c, rest same, +y
    # " Zebralower"->" Zebralowery": space->space, rest same, +y
    # So: first character shifted up by 1 (alphabet, wrap Z->A, space stays), rest unchanged, append 'y'
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+1)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+1)%26+ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        if s == "":
            out.append("y")
        else:
            out.append(shift(s[0]) + s[1:] + "y")
    return {"outputs": out}
