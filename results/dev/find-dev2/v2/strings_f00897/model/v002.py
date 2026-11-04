def predict(probe):
    # Each char's ASCII code is shifted by +2 if it is the first char of a multi-char string, else +4 [E1, E2]
    # Single-char strings shift by +4 (treated as non-first) [E2: a->c? no, a->c is +2... wait]
    # E2: "a"->"c" (+2), "z"->"~" (+2), "1"->"5" (+4), "!"->"%" (+4)
    # So single chars: letters shift +2, digits/symbols shift +4? Check: a=97->c=99 +2. z=122->~=126 +4? 
    # z=122, ~=126, that's +4. But a->c is +2. Contradiction!
    # Hmm: a->c +2, z->~ +4. Both single letters. 
    # Wait: maybe shift is +2 for first char, but wraps? a+2=c, z+2=| (124). But observed ~ (126).
    # Actually z=122, +4=126=~. a=97,+2=99=c. So a is +2, z is +4?
    # Reconsider: maybe it's +2 for index 0, +4 for index>0, but single char... 
    # "a"->"c": +2. "z"->"~": +4. "1"->"5": +4. "!": +4.
    # So letters a->+2 but z->+4? Unless z wraps: z+2 = | (124), not ~.
    # Maybe the rule: shift +2 for first char, but if result exceeds some bound, add more?
    # Or: shift by 2, but letters near end wrap differently.
    # Actually: maybe it's +2 for index 0, +4 for index>0, and single char gets +2 normally.
    # a->c (+2) ok. z->? +2 = | (124). But observed ~ (126) = +4.
    # Hmm. What if the shift is +2 for index 0, +4 for index>0, but z is special?
    # Or: maybe the rule is +2 for first char, +4 for rest, and for single char it's +2 UNLESS... 
    # Let me reconsider: maybe it's +2 for index 0, +4 for index>0, and "z"->"~" because z+2=| but | is... no.
    # Alternative: shift = 2 + 2*(index>0), but for single char, shift = 2 + 2*(index>0) still gives +2.
    # But z->~ is +4. And a->c is +2. Both single chars, different shifts.
    # Difference: a is early alphabet, z is late. Maybe wrap-around?
    # If shift +2: a->c, z->| (124). Observed ~ (126). 
    # What if shift is +2 but capped at some max? No.
    # What if the rule is: +2 for index 0, +4 for index>0, and single char gets +2, BUT z+2 wraps past 'z' region?
    # Actually maybe the shift is +2 for first char, +4 for others, and for single char it's +2, but z->~ means +4.
    # Let me check "x y": x->| (+4), space->$ (+4), y->} (+4). All +4! Even index 0!
    # Wait "x y" -> "|$}": x=120->|=124 +4, space=32->$=36 +4, y=121->}=125 +4.
    # So "x y" all +4, including first char x! But "hello" first char h->j is +2.
    # Difference: "x y" has a space? Or x is late alphabet?
    # Hmm "x y" first char x->| is +4. "hello" first char h->j is +2.
    # Maybe first char shift depends on the char? h->+2, x->+4?
    # Or maybe: shift +2 for first char if it's a letter a-h? No...
    # Let me reconsider E1: "x"->"|" (+4). "hello" h->j (+2). "world" w->{ (+2). 
    # w=119, {=123, +4! Wait w->{ is +4, not +2!
    # Let me recheck: w=119, {=123. That's +4. But I said +2 earlier. Let me recompute.
    # h=104, j=106: +2. e=101,i=105:+4. l=108,p=112:+4. o=111,s=115:+4.
    # w=119, {=123: +4! o=111,s=115:+4. r=114,v=118:+4. l=108,p=112:+4. d=100,h=104:+4.
    # So "world" is ALL +4! w->{ is +4.
    # "hello": h->j +2, rest +4.
    # "Hello": H->J +2, rest +4.
    # "HELLO": H->J +2, rest +4.
    # "two words": t->v +2, rest +4.
    # "a b": a->c +2, rest +4.
    # "  spaced  ": space->$ +2? space=32,$=36 +4. Hmm first char space->$ is +4!
    # Wait "  spaced  " -> "$$wtegih$$": first space->$ +4, second space->$ +4, s->w +4...
    # So first char space is +4, not +2!
    # "test123": t->v +2, rest +4.
    # "abc-def": a->c +2, rest +4.
    # "x": x->| +4.
    # "a"->"c" +2. "z"->"~" +4. "1"->"5" +4. "!"->"%" +4.
    # "ab"->"cf": a->c +2, b->f +4.
    # "abc"->"cfg": a->c +2, b->f +4, c->g +4.
    # "x y"->"|$}": x->| +4, space->$ +4, y->} +4.
    # "12"->"56": 1->5 +4, 2->6 +4.
    # "hi"->"jm": h->j +2, i->m +4.
    # "Hi"->"Jm": H->J +2, i->m +4.
    # So when is first char +2 vs +4?
    # +2 cases: h(hello), H(Hello), H(HELLO), t(two words), a(a b), t(test123), a(abc-def), a(a), a(ab), a(abc), h(hi), H(Hi)
    # +4 cases: space(  spaced), x(x), z(z), 1(1), !(!), x(x y)
    # +2 first chars: h,H,t,a. +4 first chars: space,x,z,1,!.
    # Maybe: letters a-h (or a-t?) get +2, others +4? 
    # a,h,t get +2. x,z get +4. So maybe a-t get +2, u-z get +4?
    # Check: t->v +2 (t is in a-t). x->| +4 (x in u-z). z->~ +4. 
    # h->j +2. a->c +2. All consistent with a-t +2, u-z +4!
    # Non-letters (space, digit, symbol) as first char: +4.
    # What about uppercase? H->J +2. So A-T +2, U-Z +4?
    # Let me verify: is there any first char in u-z uppercase? No data. Assume A-T +2, U-Z +4.
    # Actually simpler: maybe first char shift is +2 if ord < some threshold, +4 otherwise?
    # a=97, t=116: +2. u=117: +4? x=120:+4, z=122:+4. 
    # Threshold: ord <= 116 (t) -> +2, else +4? But uppercase H=72 -> +2.
    # Hmm uppercase H=72, T=84. If threshold is 116 for lowercase... 
    # Maybe rule: first char +2 if it's a letter in first ~20 of alphabet, else +4.
    # Or: +2 if ord(ch) in [97..116] or [65..84], else +4.
    # Actually maybe simpler: +2 if the char is a letter a-t/A-T, else +4.
    # Let me just encode: first char (index 0) of multi-char string: +2 if 'a'<=c<='t' or 'A'<=c<='T', else +4.
    # Single char: same rule? "a"->+2 (a in a-t), "z"->+4 (z not), "1"->+4, "!"->+4, "x"->+4. Yes!
    # So single char follows same rule as first char. 
    # And "x y": x->+4 (x not in a-t). Yes!
    # So the rule is uniform: index 0 uses "letter a-t/A-T ? +2 : +4", index>0 always +4.
    # Wait but "  spaced  " first char space->$ +4. Space not letter, +4. Yes.
    # Let me double check "world": w->{ +4. w not in a-t. Yes!
    # "hello": h->j +2. h in a-t. Yes!
    # Great, this fits everything.
    def shift(s):
        out = []
        for i, ch in enumerate(s):
            if i == 0 and (('a' <= ch <= 't') or ('A' <= ch <= 'T')):
                out.append(chr(ord(ch) + 2))
            else:
                out.append(chr(ord(ch) + 4))
        return ''.join(out)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
