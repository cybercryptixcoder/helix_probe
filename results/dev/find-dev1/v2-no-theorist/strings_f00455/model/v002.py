def predict(probe):
    # Lowercase letters map to uppercase of the NEXT letter: a->B, z->[ ? No: z->[ means +1 code point [E2]
    # Actually observed: a->B, b->c, z->[ , so lowercase -> chr(ord+1) [E1,E2]
    # Uppercase letters: A->B, Z->[ , so uppercase -> chr(ord+1) [E1,E2]
    # Digits: 1->2, 9->: , so chr(ord+1) [E1,E2]
    # Symbols: !->", ~->DEL, so chr(ord+1) [E1,E2]
    # Non-ASCII: ÿ->Ÿ (U+00FF -> U+0179)?? observed U+0179 = ord(0xFF)+0x7A? No: 0xFF+1=0x100, but got 0x179
    #   Hmm 0xFF -> 0x179 is +0x7A. Odd. Maybe it's a case-mapping: ÿ uppercases to Ÿ (U+0178)? got U+0179.
    #   U+0179 is 'Ź'. So ÿ -> Ź. That's +0x7A. ? uncertain, treat as +1 for now? No, evidence says +0x7A.
    # Mixed: "MiXeD 42" -> "Njyfe!53": M->N(+1), i->j(+1), X->Y(+1), e->f(+1), D->E(+1), space->!(+1), 4->5, 2->3. All +1 [E2]
    # "aZ9!" -> "B{:\"": a->B(+1), Z->{(+1), 9->:(+1), !->"(+1) [E2]
    # "AZ" -> "B{" : A->B, Z->{ (+1) [E2]
    # "abz" -> "Bc{" : +1 each [E2]
    # So the rule is chr(ord(c)+1) for all ASCII. For ÿ, observed +0x7A — likely a special case; mark uncertain.
    out = []
    for s in probe.get("inputs", []):
        try:
            res = []
            for c in s:
                o = ord(c)
                if o == 0xFF:
                    res.append(chr(0x179))  # ? observed ÿ->Ź
                else:
                    res.append(chr(o + 1))
            out.append("".join(res))
        except Exception:
            out.append("")
    return {"outputs": out}
