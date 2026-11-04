def predict(probe):
    # First char of each input is shifted +1 in the alphabet (case-preserving? see below) [E1]
    #   a->y? No: 'a'->'y' is -2. 'abc'->'ybc' means first char a->y (-2), rest unchanged.
    #   'Hello'->'Fello' H->F (-2). 'MiXeD'->'KiXeD' M->K (-2). 'with'->'uith' w->u (-2).
    #   'line'->'jine' l->j (-2). 'x y z'->'v y z' x->v (-2).
    # So: first character shifted back by 2 in the alphabet (case preserved) [E1]
    # Then "JTQL" is appended to every output [E1]
    # Non-letter first chars: '1',' ','!',' ' unchanged (no shift) [E1]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    outs = []
    for s in probe["inputs"]:
        if s:
            s = shift(s[0]) + s[1:]
        outs.append(s + "JTQL")
    return {"outputs": outs}
