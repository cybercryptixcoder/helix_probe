def predict(probe):
    # Every character's Unicode codepoint is shifted by +2, uniformly [E1,E2,E3,E4]:
    #   'a'->'c', 'A'->'C', '1'->'3'? no: '1'->'5'? check E1: '1'->'5' is +4...
    # Wait: E1 '1'->'5' (+4), but E4 '0'->'4' (+4), '9'->'=' (0x39->0x3D, +4).
    # E4 'a'->'c' (+2), 'z'->'~' (0x7A->0x7E, +4)? 0x7A+2=0x7C='|', but observed '~'.
    # Hmm. Let's recheck: E4 z->~ : 0x7A->0x7E is +4. y->} : 0x79->0x7D is +4.
    # a->c (+2), b->d (+2). A->C (+2), Z->^ (0x5A->0x5E, +4).
    # E2: z->~ (+4), Z->^ (+4), 9->= (+4), y->} (+4), Y->] (+4), 8->< (+4).
    # E1: a->c(+2), A->C(+2), 1->5(+4), !->% (+4), space->$ (+4).
    # So lowercase a..? and uppercase A..? shift +2, but near end shift +4?
    # E2 'a b'->'c$f': a->c(+2), space->$(+4), b->f(+4)?? b->f is +4.
    # E1 'ab'->'cf': a->c(+2), b->f(+4). 'a1'->'c5': a+2, 1+4. 'a!'->'c%'.
    # E4 'b'->'d' (+2). So b->d in E4 but b->f in E1? Contradiction unless position matters.
    # E1 'ab'->'cf' : a->c, b->f. E4 'b'->'d'. So shift depends on position in string!
    # Position 0: +2, position 1+: +4? Check E1 'ab': pos0 a->c(+2), pos1 b->f(+4). Yes.
    # E1 'AB'->'CF': A->C(+2), B->F(+4). Yes.
    # E2 'Hello, World!': H->J(+2), e->i(+4), l->p(+4), l->p, o->s, ,->0(+4), space->$, W->[? 
    #   W(0x57)->[ (0x5B) +4. o->s(+4), r->v(+4), l->p, d->h, !->%. Yes all +4 after pos0.
    # E2 'abcXYZ019!': a->c(+2), b->f(+4), c->g(+4), X->\(+4), Y->], Z->^, 0->4,1->5,9->=,!->%.
    # So: first character +2, all subsequent characters +4. Uniform codepoint shift.
    # E3 single chars: all +2 (they're position 0). '{'->0x7F (+2). Yes.
    # E3 '\u007f'->'\u0083' (+4)? 0x7F->0x83 is +4. But it's a single char at pos0!
    # Hmm 0x7F+2=0x81, observed 0x83. So +4. Contradiction with pos0 +2.
    # Wait E3 inputs are single chars each, so pos0. '{'->0x7F is +2. 0x7F->0x83 is +4.
    # Maybe: shift +2 for codepoints < 0x7F, +4 for >= 0x7F? Check '~' 0x7E->0x82(+4) in E4.
    # But E3 '~'->'\u0082' (+4). And E2 z->~ : 0x7A->0x7E +4. Hmm z is <0x7F but +4.
    # Let's reconsider: maybe it's +2 for a-z,A-Z start... no.
    # Recheck E4: a->c(+2), b->d(+2), y->}(+4), z->~(+4), A->C(+2), Z->^(+4),
    #   0->4(+4), 9->=(+4), !->%(+4), ~->0x82(+4).
    # So a,b,A shift +2; y,z,Z,0,9,!,~ shift +4.
    # E1: a->c(+2), A->C(+2), 1->5(+4), !->%(+4), space->$(+4).
    # E2: y->}(+4), Y->](+4), 8-><(+4).
    # So which chars get +2? a,b,A in E4. In E1 'ab'->'cf': a+2,b+4. So b differs by position.
    # E4 b->d (+2) but E1 b (pos1)->f (+4). So position matters for b.
    # E4 a->c, b->d both +2 (pos0). E1 a->c(pos0 +2), b->f(pos1 +4).
    # So: pos0 +2, pos>0 +4? But E4 y,z,Z,0,9,!,~ are all pos0 and get +4.
    # So pos0: +2 for a,b,A; +4 for y,z,Z,0,9,!,~.
    # E1 pos0: a+2,A+2,1+4,!+4,space+4. E2 pos0: z+4,Z+4,9+4,y+4,Y+4,8+4.
    # E3 pos0: {+2,}+2, :+2, ~+4, @+2, _+2, `+2, 0x7F+4, 0x80+4, 0x81+4.
    # Pattern for pos0: +2 for a,b,A,{,},:,@,_,` ; +4 for y,z,Z,0,9,!,space,~,0x7F+.
    # Hmm a,b,A +2 but y,z,Z +4. Maybe +2 if codepoint in some set, else +4.
    # a=0x61,b=0x62,A=0x41,{=0x7B,}=0x7D,:=0x3A,@=0x40,_=0x5F,`=0x60 -> +2
    # y=0x79,z=0x7A,Z=0x5A,0=0x30,9=0x39,!=0x21,space=0x20,~=0x7E -> +4
    # Maybe +2 if codepoint mod something? 0x61,0x62,0x41,0x7B,0x7D,0x3A,0x40,0x5F,0x60
    # vs 0x79,0x7A,0x5A,0x30,0x39,0x21,0x20,0x7E.
    # 0x61=97,0x62=98,0x41=65,0x7B=123,0x7D=125,0x3A=58,0x40=64,0x5F=95,0x60=96
    # 0x79=121,0x7A=122,0x5A=90,0x30=48,0x39=57,0x21=33,0x20=32,0x7E=126
    # +2 set: 97,98,65,123,125,58,64,95,96. +4 set:121,122,90,48,57,33,32,126.
    # Hmm 97,98 (+2) but 121,122 (+4). 65(+2) but 90(+4). Maybe mod 3? 97%3=1,98%3=2,65%3=2...
    # 121%3=1,122%3=2. Same mod, different shift. Not mod.
    # Maybe it's a Caesar on letters only for +2 region and +4 elsewhere? No.
    # Let's just check: is it +2 for chars where (ord-?) ... 
    # Actually maybe the rule: shift +2 if char is in "aAbB{}:@_`" ... too ad hoc.
    # Alternative: maybe the shift is +2 for pos0 AND char in a certain class, else +4.
    # Let me look at pos>0 all +4 (E1 ab->cf, AB->CF, E2 long strings all +4 after first).
    # E2 'Hello, World!': H+2 then rest +4. Confirmed.
    # So pos0 special. pos0 shift: +2 or +4 depending on char.
    # +2 chars seen: a,b,A,{,},:,@,_,`
    # +4 chars seen: y,z,Z,0,9,!,space,~,0x7F,0x80,0x81,1,8,Y
    # Notice +2 set: a,b,A,{ ,},:,@,_,` -- these are... hmm.
    # Maybe +2 if ord < 0x63 and >=0x41? a=97,b=98,A=65. But {=123,}=125,:=58,@=64,_=95,`=96.
    # Not a range. 
    # Maybe +2 if the char is a letter in first half? a,b,A yes; y,z,Z no. 
    # {,},:,@,_,` are punctuation though.
    # Perhaps: +2 if ord%? Let's try ord%5: 97%5=2,98%5=3,65%5=0,123%5=3,125%5=0,58%5=3,64%5=4,95%5=0,96%5=1
    # 121%5=1,122%5=2,90%5=0,48%5=3,57%5=2,33%5=3,32%5=2,126%5=1. No.
    # I'll go with: pos0 uses +2 for a specific set, else +4; pos>0 always +4.
    # Best guess set for +2: {a,b,A,{,},:,@,_,`}. Mark as ?.
    # Actually simpler: maybe +2 for chars in "abA{}:@_`" and +4 otherwise at pos0.
    # Let me just encode observed +2 set and default +4.
    plus2 = set("abA{}:@_`")
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0 and ch in plus2:
            return chr(o + 2)
        return chr(o + 4)
    out = []
    for s in probe["inputs"]:
        out.append("".join(shift(c, i) for i, c in enumerate(s)))
    return {"outputs": out}
