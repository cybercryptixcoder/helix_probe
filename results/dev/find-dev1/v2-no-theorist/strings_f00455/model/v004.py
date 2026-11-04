def predict(probe):
    # Rule: for each character, add 1 to its code point. EXCEPT the first character
    # of the string, which is first uppercased (str.upper, may expand to multiple chars),
    # then each resulting code point is +1. [E1-E4]
    # Evidence:
    #  - "hello"->"Ifmmp": h first -> upper(h)=H +1=I; e->f,l->m,l->m,o->p (+1) [E1]
    #  - "a"->"B", "A"->"B": first char upper+1 [E1]
    #  - "abz"->"Bc{": a first->B; b->c, z->{ (+1) [E2]
    #  - "a b"->"B!c": only very first char gets upper+1; b->c is +1 [E1,E4]
    #  - "a b c"->"B!c!d": per-word NOT applied; only first char [E4]
    #  - ß first -> upper(ß)="SS" +1 each = "Tt" [E3]; ß not first -> +1 = à [E4]
    #  - "ß a"->"Tt!b": ß first expands to Tt, then space->!, a->b (+1) [E4]
    #  - " A"->"!b": space first -> upper(space)=space +1='!'; A->B? observed 'b'!
    #    Wait: " A"->"!b". space first->'!', A->'b'? A+1='B' not 'b'. Hmm.
    #    Actually 'A'(0x41)+1=0x42='B'. Observed 'b'(0x62). So A->b is +0x21?
    #    Re-examine: maybe non-first chars get lowercased then +1? A->a+1=b. 
    #    Check "MiXeD 42"->"Njyfe!53": M first->N; i->j, X->Y? X lower=x+1=y not Y. Observed Y.
    #    Hmm X->Y is +1 (X+1=Y). So X not lowercased. But A->b in " A"?
    #    Let me recheck E4 " A"->"!b": chars: space, A. space first->'!'. A->'b'.
    #    A(0x41)->b(0x62). That's not +1. 
    #    Wait maybe I misread. "!b": '!' then 'b'. A->b?
    #    Compare E2 "AZ"->"B{": A first->B, Z->{ (+1). So Z->{ is +1.
    #    In " A", A is second char. If +1, A->B. But observed b.
    #    Hmm. Unless... the first char being space: upper(space)=space, +1='!'. Then A->? 
    #    Maybe rule is: uppercase first char, then +1 ALL; but also... no.
    #    Let me reconsider "  a"->"!!b": space,space,a. first space->'!', second space->'!', a->'b'. a+1=b ✓.
    #    " A"->"!b": space->'!', A->'b'. A+1=B≠b. 
    #    Difference: A is uppercase. a->b works (+1). A->b doesn't.
    #    Maybe non-first uppercase letters get lowercased then +1? A->a->b ✓. 
    #    But "MiXeD"->"Njyfe": X->Y. X lower=x+1=y≠Y. Contradiction.
    #    Wait "MiXeD 42"->"Njyfe!53": M->N,i->j,X->Y,e->f,D->E. 
    #    X->Y: X(0x58)+1=Y(0x59) ✓ +1. D->E: D+1=E ✓.
    #    So in MiXeD uppercase non-first -> +1. But in " A", A->b.
    #    What's different? In " A", the first char is a SPACE. 
    #    Maybe: the uppercasing applies to the first ALPHABETIC char? No, "a b"->"B!c" b->c.
    #    Hmm. Or maybe the rule is: uppercase the whole string first, then +1? 
    #    "hello" upper="HELLO" +1="IFMMP"≠"Ifmmp". No.
    #    Let me reconsider. Maybe it's: for first char upper+1; for others +1; BUT there's something about " A".
    #    Actually wait: maybe the transformation is: uppercase(c) for first char, then +1; for others, +1. 
    #    " A": space first: upper(space)=' ', +1='!'. A second: +1='B'. Expected "!B". Observed "!b".
    #    So A->b. That's A lowercased then +1. 
    #    Could it be: the FIRST char determines case? Like if first char is lowercase/space, whole string lowercased then +1? 
    #    "hello"->"Ifmmp": h first. If whole lowercased: hello, +1=ifmmp≠Ifmmp. No.
    #    Hmm "Ifmmp": I is uppercase. So first char upper+1, rest +1.
    #    " A"->"!b": first space->'!'. A->b. 
    #    Maybe: after the first char, uppercase letters are lowercased then +1, lowercase +1? 
    #    Check "MiXeD": X->Y (not lowercased). Contradiction.
    #    Unless "MiXeD" X->Y is actually... let me recount "Njyfe!53": N,j,y,f,e,!,5,3.
    #    M->N, i->j, X->y, e->f, D->e. X->y! Not Y. Let me check: "Njyfe" = N,j,y,f,e. 
    #    X(0x58)->y(0x79)? That's not +1. Hmm. X lower=x, +1=y. So X->y is lowercase+1!
    #    D->e: D lower=d+1=e ✓. So uppercase non-first -> lowercase then +1!
    #    Recheck "AZ"->"B{": A first->B. Z->{? Z lower=z+1={ ✓! 
    #    "aZ9!"->"B{:\"": a first->B, Z->{, 9->:, !->". Z->{ = z+1 ✓.
    #    "Hello"->"Ifmmp": H first->I, e->f,l->m,l->m,o->p. lowercase +1 ✓.
    #    "MiXeD 42": M first->N, i->j, X->y, e->f, D->e, space->!, 4->5,2->3 = "Njyfe!53" ✓!!
    #    So rule: first char: upper then +1. Other chars: LOWER then +1!
    #    Check "hello": h first->I, e->f,l->m,l->m,o->p = "Ifmmp" ✓ (lowercase already).
    #    "a b"->"B!c": a first->B, space->!, b->c ✓.
    #    "abz"->"Bc{": a->B, b->c, z->{ ✓.
    #    "123"->"234": 1 first->upper(1)+1=2, 2->3,3->4 ✓.
    #    "  "->"!!": space first->!, space->! ✓.
    #    "z"->"[": z first->upper(z)=Z+1=[ ✓.
    #    "Z"->"[": Z first->Z+1=[ ✓.
    #    "~"->DEL: ~ first->~+1 ✓.
    #    ÿ first->Ÿ+1=Ź ✓. ÿ non-first: lower(ÿ)=ÿ+1=Ā ✓ ("aÿ"->"BĀ").
    #    þ first->Þ+1=ß ✓.
    #    é first->É+1=Ê ✓.
    #    ß first->upper(ß)="SS"+1="Tt" ✓.
    #    ß non-first: lower(ß)=ß+1=à ✓ ("a ß"->"B!à").
    #    "ß a"->"Tt!b": ß first->Tt, space->!, a->b ✓.
    #    "x ß y"->"Y!à!z": x first->X+1=Y, space->!, ß->à, space->!, y->z ✓.
    #    "ßß"->"Ttà": ß first->Tt, ß non-first->à ✓.
    #    "aß"->"Bà": a first->B, ß->à ✓.
    #    " A"->"!b": space first->!, A->lower(A)=a+1=b ✓!
    #    "  a"->"!!b": space->!, space->!, a->b ✓.
    #    "Ω Ω"->"Ϊ!ϊ": Ω first->upper(Ω)=Ω+1=Ϊ, space->!, Ω non-first->lower(Ω)=ω+1=ϊ ✓!
    #    "a Ω"->"B!ϊ": a->B, space->!, Ω->ω+1=ϊ ✓.
    #    "Ā" first->Ā+1=ā ✓. "€"->€+1=₭ ✓. "中"->中+1=丮 ✓.
    #    All consistent! Rule: first char: upper() then +1 per codepoint. Other chars: lower() then +1 per codepoint.
    out = []
    for s in probe.get("inputs", []):
        try:
            if not s:
                out.append("")
                continue
            res = []
            for c in s[0].upper():
                res.append(chr(ord(c) + 1))
            for c in s[1:]:
                for d in c.lower():
                    res.append(chr(ord(d) + 1))
            out.append("".join(res))
        except Exception:
            out.append("")
    return {"outputs": out}
