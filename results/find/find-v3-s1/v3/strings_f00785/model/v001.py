def predict(probe):
    # Observations [E1]: first char shifted +1 (a->b, t->u, d->e, M->N), last char shifted +1 (e->y? no)
    # Actually: "apple"->"bppley": a->b, p->p, p->p, l->l, e->e, then append 'y'? 
    # "test case "->"uest case y": t->u, rest same, trailing space->y
    # "test caseMiXeD"->"uest caseMiXeDy": t->u, append y
    # "data a Python "->"eata a Python y": d->e, trailing space->y
    # "Mississippi Hello World data"->"Nississippi Hello World datay": M->N, append y
    # Rule: first char +1 (if letter), last char: if space -> 'y', else append 'y'
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-97+1)%26+97)
        if 'A' <= c <= 'Z':
            return chr((ord(c)-65+1)%26+65)
        return c
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        first = shift(s[0])
        rest = s[1:]
        if rest.endswith(' '):
            rest = rest[:-1] + 'y'
        else:
            rest = rest + 'y'
        out.append(first + rest)
    return {"outputs": out}
