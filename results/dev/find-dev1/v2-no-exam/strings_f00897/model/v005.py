def predict(probe):
    # Mechanism: for each character, shift its Unicode code point by +2
    # (i.e. add 2 to ord(c)), then convert back with chr().
    # Evidence:
    #  'a'(97)->'c'(99), 'A'(65)->'C'(67), '1'(49)->'5'(51) [E1]
    #  ' '(32)->'$'(36)? Wait: 32+2=34='"' not '$'. Check: '$' is 36.
    #  Hmm, space -> '$' is +4? Let's recheck E1: " " -> "$".
    #  ord(' ')=32, ord('$')=36, so +4. But 'a'->'c' is +2.
    #  Re-examine: maybe it's not a simple shift.
    #
    # Let's tabulate from evidence:
    # a->c (+2), A->C (+2), 1->5 (+4), ' '->$ (+4), !->% (+4)
    # ab->cf: a->c(+2), b->f(+4)? b(98)->f(102) is +4.
    # AB->CF: A->C(+2), B->F(+4).
    # 12->56: 1->5(+4), 2->6(+4).
    # "a b"->"c$f": a->c(+2), space->$ (+4), b->f(+4).
    #
    # So first character gets +2, subsequent characters get +4? Check E6:
    # aa->ce: a->c(+2), a->e(+4). Yes!
    # ba->de: b->d(+2), a->e(+4). Yes!
    # zzz->~~~: z->~(+2), z->~(+4), z->~(+4). z(122)+2=124='|', not '~'.
    # Wait z->~ : ord('z')=122, ord('~')=126, so +4. Hmm.
    # E2: z->~ (+4). But a->c (+2). Contradiction?
    #
    # Let's recheck E2: "z"->"~". z=122, ~=126, +4.
    # E1: "a"->"c". a=97, c=99, +2.
    # Hmm, so it's not uniform.
    #
    # E3: n->p (+2), N->P (+2), m->o (+2), M->O (+2), l->n(+2), L->N(+2)
    #     0->4 (+4), 9->= (+4), @->B (+2), a~->c\x82: a->c(+2), ~->\x82(+4)
    # E4: w->{ (+5)? w=119, {=123, +4. x->| (+4). W->[ (+5)? W=87, [=91, +4.
    #     X->\ (+4). Y->] (+4).
    #     wy->{}: w->{ (+4), y->} (+4)? y=121, }=125, +4.
    #     xz->|~: x->| (+4), z->~ (+4).
    #     WY->[]: W->[ (+4), Y->] (+4).
    #     XZ->\^: X->\ (+4), Z->^ (+4).
    #     y z->}$~: y->} (+4), space->$ (+4), z->~ (+4).
    #
    # So E4 all +4. E1 a->c is +2. E3 n->p is +2.
    # E5: 0a->4e: 0->4(+4), a->e(+4). !a->%e: !->%(+4), a->e(+4).
    #     space a -> $e: space->$(+4), a->e(+4).
    #     @a->Be: @->B(+2), a->e(+4).
    #     9a->=e: 9->=(+4), a->e(+4).
    #     {a->\x7fe: {->\x7f(+4), a->e(+4).
    #     ~a->\x82e: ~->\x82(+4), a->e(+4).
    #     \x80a->\x84e: \x80->\x84(+4), a->e(+4).
    #     ya->}e: y->}(+4), a->e(+4).
    #     na->pe: n->p(+2), a->e(+4).
    #
    # So single-char inputs: a->c(+2), A->C(+2), n->p(+2), N->P(+2)...
    # but z->~(+4), 0->4(+4), 9->=(+4), w->{(+4), x->|(+4)...
    #
    # Wait, maybe it's not position-based but character-region based?
    # Let's check: a,A,n,N,m,M,l,L,@ -> +2
    # z,0,9,w,x,W,X,Y,~,} -> +4
    # 1,space,! -> +4
    #
    # Hmm, what distinguishes a from z? Both lowercase letters.
    # a->c, z->~. Let's check: maybe it's based on the character's value mod something?
    # a=97, 97 mod ? =? c=99. z=122->126.
    # 97->99 (+2), 122->126 (+4).
    # 65->67 (+2), 87->91 (+4).
    # 110->112(+2), 119->123(+4).
    # 109->111(+2).
    # 108->110(+2).
    #
    # Hmm, maybe it depends on the character's position in alphabet?
    # a is 1st letter, z is 26th. n is 14th, m is 13th, l is 12th.
    # w is 23rd, x is 24th.
    # Letters 1-14 (a-n): +2. Letters 23-26 (w-z): +4.
    # What about 15-22 (o-v)? Unknown.
    #
    # But digits: 0->4(+4), 1->5(+4), 2->6(+4), 9->=(+4). All +4.
    # Space, !, @: space+4, !+4, @+2. @ is 64. 
    #
    # Wait, maybe it's simpler: the shift is +2 for the first character of the
    # string if that character is in some set, else +4? No, E6 aa->ce: first a +2, second a +4.
    # So position matters: first char +2, rest +4? But z->~ is single char +4.
    # And a->c single char +2.
    #
    # Let's reconsider: maybe it's +2 if the character is in [a-n] or [A-N] or @,
    # and +4 otherwise? Check E1 "a b"->"c$f": a->c(+2), space->$(+4), b->f(+4).
    # b is in a-n, so should be +2, but it's +4. So position matters for b.
    #
    # Hmm. Let's look at E6: aa->ce, ba->de, ca->ee, ... ja->le.
    # First char: a->c(+2), b->d(+2), c->e(+2), d->f(+2), e->g(+2), f->h(+2),
    # g->i(+2), h->j(+2), i->k(+2), j->l(+2). All +2.
    # Second char: always a->e (+4).
    #
    # E5: all second chars a->e (+4). First chars: 0->4(+4), !->%(+4), space->$(+4),
    # @->B(+2), 9->=(+4), {->\x7f(+4), ~->\x82(+4), \x80->\x84(+4), y->}(+4), n->p(+2).
    #
    # So first char: a-n, A-N, @ get +2; others get +4.
    # Second char (and beyond): always +4.
    #
    # Check E4: wy->{}: w->{(+4) first char w is not a-n, so +4. y->}(+4) second char +4. Good.
    # xz->|~: x->|(+4), z->~(+4). Good.
    # WY->[]: W->[(+4), Y->](+4). Good.
    # XZ->\^: X->\(+4), Z->^(+4). Good.
    # y z->}$~: y->}(+4), space->$(+4), z->~(+4). Good.
    #
    # E2: z->~(+4) first char z not in a-n. Good.
    # Z->^(+4). Good.
    # y->}(+4). Good.
    # ~->\x82(+4). Good.
    # }->\x81(+4). Good.
    # ba->de: b->d(+2), a->e(+4). Good.
    # aa->ce: a->c(+2), a->e(+4). Good.
    # aA->cE: a->c(+2), A->E(+4). Good.
    # A a->C$e: A->C(+2), space->$(+4), a->e(+4). Good.
    # zzz->~~~: z->~(+4), z->~(+4), z->~(+4). Good.
    #
    # E3: n->p(+2) n in a-n. Good.
    # N->P(+2). Good.
    # m->o(+2), M->O(+2), l->n(+2), L->N(+2). Good.
    # 0->4(+4), 9->=(+4). Good.
    # @->B(+2) @ is first char and gets +2. Good.
    # a~->c\x82: a->c(+2), ~->\x82(+4). Good.
    #
    # E1: a->c(+2), A->C(+2), 1->5(+4), space->$(+4), !->%(+4).
    # ab->cf: a->c(+2), b->f(+4). Good.
    # AB->CF: A->C(+2), B->F(+4). Good.
    # 12->56: 1->5(+4), 2->6(+4). Good.
    # a b->c$f: a->c(+2), space->$(+4), b->f(+4). Good.
    # Hello, World!->Jipps0$[svph%:
    #   H->J(+2), e->i(+4), l->p(+4), l->p(+4), o->s(+4), ,->0(+4),
    #   space->$(+4), W->[(+4), o->s(+4), r->v(+4), l->p(+4), d->h(+4), !->%(+4).
    #   Check: H=72, J=74 (+2). e=101, i=105 (+4). l=108, p=112 (+4). o=111, s=115 (+4).
    #   ,=44, 0=48 (+4). space=32,$=36(+4). W=87,[=91(+4). r=114,v=118(+4). d=100,h=104(+4).
    #   !=33, %=37(+4). All match!
    #
    # So rule: for each character at index i in the string:
    #   if i == 0 and character is in [a-n] or [A-N] or '@': shift +2
    #   else shift +4
    #
    # Wait, is '@' really +2? E3 @->B: @=64, B=66, +2. Yes.
    # What about other chars in that range? @ is 64. A=65. 
    # Maybe the rule is: first char, if ord(c) in [64, 110] (i.e. @ through n), +2?
    # Let's check: a=97 in [64,110] -> +2. n=110 in range -> +2. 
    # o=111 not in range -> +4? Unknown but plausible.
    # A=65 in range -> +2. N=78 in range -> +2.
    # What about digits? 0=48 not in [64,110] -> +4. Good.
    # 1=49 -> +4. Good.
    # space=32 -> +4. Good.
    # !=33 -> +4. Good.
    # {=123 not in range -> +4. Good.
    # ~=126 -> +4. Good.
    # \x80=128 -> +4. Good.
    # y=121 -> +4. Good.
    # w=119 -> +4. Good.
    # x=120 -> +4. Good.
    # z=122 -> +4. Good.
    # Z=90 in [64,110]? 90 is in range, but Z->^ is +4. Contradiction!
    # Z=90, ^=94, +4. So Z is in [64,110] but gets +4.
    #
    # Hmm. So range [64,110] is wrong. Let's reconsider.
    # +2 chars seen: a,b,c,d,e,f,g,h,i,j (from E6 first chars), l,m,n, A,B,C (from E1), N,P? no N->P is +2, L->N +2, M->O +2, @->B +2.
    # +4 chars seen: z,Z,y,~,},0,9,w,x,W,X,Y,space,!,1,2,{, \x80.
    #
    # So +2 set includes: a-n, A-N, @.
    # +4 set includes: o-z? (we have w,x,y,z), O-Z (W,X,Y,Z), 0-9, space, !, {, ~, \x80.
    #
    # What about o-v and O-V? Unknown. But likely the rule is:
    # +2 if first char is in [a-n] or [A-N] or '@'
    # else +4.
    #
    # Actually, maybe simpler: +2 if ord(c) in [64, 110] AND c is not uppercase beyond N?
    # N=78, O=79. Z=90. So [64,78] for uppercase? But @=64, A=65...N=78.
    # Lowercase a=97...n=110. So [97,110] for lowercase.
    # What about chars between 79 and 96? [O-Z, [, \, ], ^, _, `]. Unknown.
    # And 64 is @.
    #
    # Maybe the rule is: +2 if c in "@" + "A-N" + "a-n", else +4.
    # That fits all evidence.
    #
    # Let's also check: is it possible the rule is based on the character's
    # position in some ordering? Like +2 if c is in first half of alphabet?
    # a-n is 14 letters, o-z is 12. A-N is 14, O-Z is 12. @ is one char.
    # Hmm, 14+14+1 = 29 chars. Odd.
    #
    # Alternatively: +2 if ord(c) <= 110 and ord(c) >= 64 and not (79<=ord(c)<=96)?
    # That's @, A-N, a-n. Same as above.
    #
    # I'll go with: first character gets +2 if it's in "@A-Na-n", else +4.
    # All subsequent characters get +4.
    #
    # Wait, let me double check E6: ja->le. j=106, l=108 (+2). a->e(+4). Good.
    # ia->ke: i=105, k=107 (+2). Good.
    #
    # And E5: na->pe: n=110, p=112 (+2). Good.
    #
    # What about single char '@'? E3 @->B (+2). Good.
    #
    # One more check: E2 "A a"->"C$e": A->C(+2), space->$(+4), a->e(+4). Good.
    #
    # I'm fairly confident. Let me also consider: maybe the +2 set is
    # exactly characters whose ord is in [64,110] minus [79,96]? 
    # That's @ (64), A-N (65-78), a-n (97-110). Yes.
    #
    # Actually simpler: +2 if c in "@" or "A"<=c<="N" or "a"<=c<="n".
    #
    # Let me write the code.

    def shift_char(c, is_first):
        o = ord(c)
        if is_first and (c == '@' or ('A' <= c <= 'N') or ('a' <= c <= 'n')):
            return chr(o + 2)
        return chr(o + 4)

    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        if not isinstance(s, str):
            s = str(s)
        out = []
        for i, c in enumerate(s):
            out.append(shift_char(c, i == 0))
        outputs.append("".join(out))
    return {"outputs": outputs}
