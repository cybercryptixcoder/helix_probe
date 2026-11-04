def predict(probe):
    # Observations:
    # - ASCII: every char -> chr(ord+1): a->B, A->B, 1->2, !->", ~->DEL, space->! [E1,E2]
    # - ÿ (U+00FF) -> Ź (U+0179): that's uppercase(ÿ) then +1? uppercase(ÿ)=Ÿ(U+0178), +1=Ź(U+0179) [E2,E3]
    # - þ (U+00FE) -> ß (U+00DF): uppercase(þ)=Þ(U+00DE), +1=ß(U+00DF) [E3]
    # - é (U+00E9) -> Ê (U+00CA): uppercase(é)=É(U+00C9), +1=Ê(U+00CA) [E3]
    # - ß (U+00DF) -> "Tt": uppercase(ß)="SS", then +1 each -> "Tt" [E3]
    # - So rule: uppercase the char, then add 1 to each resulting code point. For ASCII letters uppercase
    #   is identity (already upper) -> +1. For lowercase ASCII, uppercase makes it upper then +1, which
    #   equals ord+1 only for... wait: 'a'->'A'->'B' = ord('a')+1. Yes coincidentally same for a-z.
    #   Actually 'a'(0x61)->'A'(0x41)+1='B'(0x42)=0x62? No 0x42 != 0x62. But observed a->B (0x42). 
    #   Hmm a->B is 0x42. ord('a')+1=0x62='b'. But observed "B". So it IS uppercase-then-+1! [E1]
    #   Wait E1: "hello"->"Ifmmp". h->I? uppercase(h)=H(0x48)+1=I(0x49). Yes! e->f: E+1=F. l->m: L+1=M. o->p: O+1=P.
    #   So "hello"->"IFMMP"? But observed "Ifmmp". Hmm. h->I, e->f, l->m, l->m, o->p = "Ifmmp". 
    #   e->f: uppercase(e)=E(0x45)+1=F(0x46)='F' not 'f'. But observed 'f'. Contradiction!
    #   So lowercase ASCII -> lowercase+1 (a->b would be 'b' but observed 'B' for 'a'...). 
    #   E1: "a"->"B". E2: "abz"->"Bc{". a->B, b->c, z->{. So a->B but b->c. Not uniform!
    #   a(0x61)->B(0x42): uppercase then +1. b(0x62)->c(0x63): +1. z(0x7A)->{(0x7B): +1.
    #   Hmm inconsistent. Unless: uppercase(a)=A, +1=B. uppercase(b)=B, +1=C not c. 
    #   Wait "abz"->"Bc{": a->B, b->c, z->{. b->c is +1. a->B is uppercase+1.
    #   Maybe rule: if uppercase(c) != c (i.e. lowercase), then... no.
    #   Let me reconsider: maybe it's uppercase(c) then +1, but for b: uppercase(b)=B(0x42)+1=C(0x43). Observed 'c'(0x63). No.
    #   Alternative: the rule is chr(ord(c)+1) for ASCII, EXCEPT a->B? But E1 "hello"->"Ifmmp": h->I not i.
    #   h(0x68)+1=0x69='i'. Observed 'I'(0x49). So h->I is uppercase+1.
    #   e->f: e(0x65)+1=0x66='f'. Observed 'f'. So e->f is +1.
    #   l->m: l+1=m. observed m. +1.
    #   o->p: +1.
    #   So "hello"->"Ifmmp": h->I (upper+1), e->f(+1), l->m(+1), l->m, o->p.
    #   Why h special? h is... hmm. Maybe first char of word? "Hello"->"Ifmmp": H->I (upper+1), e->f,l->m,l->m,o->p. Same.
    #   "a b"->"B!c": a->B(upper+1), space->!(+1), b->c(+1).
    #   "MiXeD 42"->"Njyfe!53": M->N(+1), i->j(+1), X->Y(+1), e->f(+1), D->E(+1), space->!, 4->5,2->3.
    #   So i->j is +1 (i+1=j). But in "hello" h->I is upper+1. 
    #   Difference: h vs i? h(0x68), i(0x69). h+1=i but observed I. 
    #   Hmm wait maybe I misread. "hello"->"Ifmmp". Let me index: I f m m p. h->I, e->f, l->m, l->m, o->p.
    #   e->f is +1 (e+1=f). l->m +1. o->p +1. h->I: h+1=i, but got I. 
    #   Unless it's: uppercase(c)+1 for ALL letters, and for e: E+1=F not f. So no.
    #   Let me try: maybe the rule is chr(ord(c)+1) but with case preserved differently...
    #   Actually maybe: if c is lowercase, output uppercase(c)+1? a->A+1=B. b->B+1=C. But observed b->c. No.
    #   I'm confusing myself. Let me carefully use E2 "abz"->"Bc{": a->B, b->c, z->{.
    #   a(0x61): B(0x42). b(0x62): c(0x63). z(0x7A): {(0x7B).
    #   b->c and z->{ are +1. a->B is not +1 (that'd be b).
    #   So a is special? Or maybe first char? In "abz" a is first. In "hello" h is first -> I (upper+1). 
    #   In "Hello" H first -> I (+1, since H+1=I). In "MiXeD" M first -> N (+1). 
    #   In "a b" a first -> B (upper+1). In "aZ9!" a first -> B (upper+1). 
    #   In "aÿ" a first -> B. In "ÿa" ÿ first -> Ź, a->b? observed "Źb". a->b is +1 here (not first).
    #   So hypothesis: FIRST character gets uppercase-then-+1; rest get +1? 
    #   Check "hello": h first -> upper(h)+1 = H+1 = I. ✓. e->f(+1)✓, l->m✓, l->m✓, o->p✓. "Ifmmp" ✓
    #   "Hello": H first -> upper(H)+1 = I ✓. "Ifmmp" ✓
    #   "a b": a first -> B ✓, space->!✓, b->c✓. "B!c" ✓
    #   "abz": a first -> B ✓, b->c✓, z->{✓. "Bc{" ✓
    #   "AZ": A first -> upper(A)+1=B ✓, Z->{(+1)✓. "B{" ✓
    #   "aZ9!": a first->B✓, Z->{✓, 9->:✓, !->"✓. "B{:\"" ✓
    #   "MiXeD 42": M first->upper(M)+1=N✓, i->j✓,X->Y✓,e->f✓,D->E✓,space->!✓,4->5✓,2->3✓. "Njyfe!53" ✓
    #   "123": 1 first->upper(1)+1? upper('1')='1', +1='2' ✓, 2->3✓, 3->4✓. "234" ✓
    #   "  ": space first->upper(space)+1='!'✓, space->!✓. "!!" ✓
    #   "z": z first->upper(z)+1=Z+1=[ ✓. "[" ✓
    #   "Z": Z first->upper(Z)+1=[ ✓
    #   "9": 9 first->upper(9)+1=: ✓
    #   "~": ~ first->upper(~)+1=DEL ✓
    #   "ÿ": ÿ first->upper(ÿ)+1=Ÿ+1=Ź ✓
    #   "þ": þ first->upper(þ)+1=Þ+1=ß ✓
    #   "é": é first->upper(é)+1=É+1=Ê ✓
    #   "ß": ß first->upper(ß)+1="SS"+1="Tt" ✓ (uppercase expands to 2 chars, each +1)
    #   "aÿ": a first->B✓, ÿ->? not first, so +1? ÿ+1=0x100=Ā. Observed "B\u0100" = B + Ā ✓!
    #   "ÿa": ÿ first->Ź✓, a->b(+1)✓. "Źb" ✓
    #   "Ā"(U+0100): first->upper(Ā)+1. upper(Ā)=Ā, +1=ā(U+0101) ✓
    #   "€": first->upper(€)+1=€+1=₭(U+20AD) ✓
    #   "Ω": first->upper(Ω)+1=Ω+1=Ϊ(U+03AA) ✓
    #   "中": first->upper(中)+1=中+1=丮(U+4E2E) ✓
    #   All consistent! Rule: for the FIRST character, apply str.upper() then add 1 to each code point of the result.
    #   For all OTHER characters, add 1 to each code point (no uppercasing).
    #   Wait but does uppercase apply only to first char, or is it "uppercase then +1" for first char only?
    #   Check "hello" e->f: e+1=f ✓ (no uppercase). Good.
    #   But wait, what about "MiXeD": i->j is +1 ✓ (no upper). Good.
    #   Hmm but is it really "first char" or "first char of each word"? "a b"->"B!c": b->c (+1, not upper+1). So only very first char.
    #   Let me double check "hello" h->I: upper(h)=H, +1=I ✓. If it were just +1, h+1=i. Observed I. ✓ first-char rule.
    #   Great. So: first char: upper then +1 per code point. Rest: +1 per code point.
    out = []
    for s in probe.get("inputs", []):
        try:
            if not s:
                out.append("")
                continue
            res = []
            first = s[0].upper()
            for c in first:
                res.append(chr(ord(c) + 1))
            for c in s[1:]:
                res.append(chr(ord(c) + 1))
            out.append("".join(res))
        except Exception:
            out.append("")
    return {"outputs": out}
