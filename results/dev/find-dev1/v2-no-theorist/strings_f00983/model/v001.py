def predict(probe):
    # Per-character Caesar shift: each char's code point is increased by 4 [E1]
    #   h->l? no: h(104)->p(112) is +8; e(101)->m(109) +8; l->t +8; o->w +8
    #   So shift is +8 for lowercase letters [E1: hello->pmttw]
    # Uppercase also +8: H->P, E->M, L->T, O->W [E1: Hello->Pmttw, HELLO->PMTTW]
    # Digits +6? '1'(49)->'9'(57) +8; '2'(50)->':'(58) +8; '3'(51)->';'(59) +8 [E1: 123->9:;]
    # So it's a uniform +8 on every code point [E1: !(33)->)(41) +8, @(64)->H(72) +8, #(35)->+(43) +8]
    # Space (32)->'('(40) +8 [E1: hello world->pmttw(pwztl]
    # Empty string -> empty [E1]
    # Confirmed: The quick brown fox -> \pm(y}qks(jzw\x7fv(nw\x80 (all +8) [E1]
    def shift(s):
        return ''.join(chr(ord(c) + 8) for c in s)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
