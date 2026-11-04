def predict(probe):
    # Every character's codepoint is shifted by +2, uniformly, regardless of position [E1,E2,E3,E4,E5].
    #   'a'->'c', 'b'->'d', ... 'j'->'l' [E5]
    #   'y'->'}', 'z'->'~', 'A'->'C', 'Z'->'^', '0'->'4', '9'->'=', '!'->'%', '~'->'\u0082' [E4]
    #   '{'->'\u007f', '}'->'\u0081', ':'->'>', '@'->'B', '_'->'a', '`'->'b' [E3]
    #   '\u007f'->'\u0083'? No: E3 shows '\u007f'->'\u0083' which is +4... 
    #   Wait: E3 '\u007f'->'\u0083' is +4, '\u0080'->'\u0084' is +4, '\u0081'->'\u0085' is +4.
    #   But '{' (0x7B)->'\u007f' (0x7F) is +4! And '}' (0x7D)->'\u0081' is +4.
    #   Recheck E3: '{'->'\u007f' : 0x7B->0x7F = +4. '}'->'\u0081' = +4. ':'->'>' = +4. '~'->'\u0082' = +4.
    #   '@'->'B' = +2! '_'->'a' = +2! '`'->'b' = +2!
    #   Hmm. E4: a->c(+2), b->d(+2), y->}(+4), z->~(+4), A->C(+2), Z->^(+4), 0->4(+4), 9->=(+4), !->%(+4), ~->\u0082(+4).
    #   E5: a..j all +2 (c,d,e,f,g,h,i,j,k,l).
    #   E1: a->c(+2), A->C(+2), 1->5(+4), !->%(+4), space->$(+4), ab->cf (a+2,b+4), AB->CF (A+2,B+4), a1->c5, a!->c%.
    #   E2: z->~(+4), Z->^(+4), 9->=(+4), y->}(+4), Y->](+4), 8-><(+4), 'a b'->'c$f' (a+2, space+4, b+4).
    #   'Hello, World!'->'Jipps0$[svph%': H+2, e+4, l+4, l+4, o+4, ,+4, space+4, W+4, o+4, r+4, l+4, d+4, !+4.
    #   'abcXYZ019!'->'cfg\]^45=%': a+2, b+4, c+4, X+4, Y+4, Z+4, 0+4, 1+4, 9+4, !+4.
    #   So position matters: pos0 sometimes +2, pos>0 always +4.
    #   But E5: a..j are all single chars (pos0) and ALL +2. So c,d,e,f,g,h,i,j at pos0 are +2.
    #   E4: y,z,Z,0,9,!,~ at pos0 are +4. a,b,A at pos0 +2.
    #   E3: {,},:,~,0x7f,0x80,0x81 at pos0 +4; @,_,` at pos0 +2.
    #   So pos0: +2 for a-j (and presumably k..?), A, @, _, ` ; +4 for y,z,Z,0,9,!,~,{,},:,0x7f+.
    #   Need boundary. E5 shows a..j +2. E4 shows y,z +4. What about k..x? Unknown.
    #   E1 'ab'->'cf': pos0 a+2, pos1 b+4. E2 'a b': a+2, space+4, b+4.
    #   So pos>0 always +4. pos0: +2 for some chars, +4 for others.
    #   Guess: pos0 +2 for chars in a certain range. a(97)..j(106) +2, y(121),z(122) +4.
    #   A(65)+2, Z(90)+4. @(64)+2, _(95)+2, `(96)+2, {(123)+4, }(125)+4, :(58)+4.
    #   Hmm :(58)+4 but @(64)+2. 0(48)+4, 9(57)+4, !(33)+4, space(32)+4.
    #   Maybe +2 if ord in [64,106]? @=64 +2, _=95 +2, `=96 +2, a-j=97-106 +2. A=65 +2.
    #   But :(58)+4, 0-9(48-57)+4, space,!(32,33)+4. And {(123)+4,}(125)+4,~(126)+4, y,z(121,122)+4.
    #   So range [64,106] gives +2 at pos0? Check Z=90 is in [64,106] but Z->^ is +4! Contradiction.
    #   Z=90 in range but +4. Hmm. Y=89->] +4 (E2). So uppercase Y,Z +4 but A +2.
    #   Maybe +2 for [64,106] except uppercase letters after some point? A=65+2, Y=89+4, Z=90+4.
    #   Ugh. Let me reconsider: maybe it's not position but something else.
    #   E1 'ab'->'cf': could be a+2, b+4. But E5 'b'->'d' is +2. So b at pos1 is +4, at pos0 is +2. Position matters.
    #   OK so pos0 rule: +2 for {A, @, _, `, a..j}, +4 otherwise (observed). 
    #   Best guess: pos0 +2 for ord in [64,106] minus... no, Z=90 breaks it.
    #   Let me try: +2 for ord in [64,106] AND not uppercase? A=65 is uppercase and +2. 
    #   Alternative: +2 for ord in [64,106] where... A(65)+2, Y(89)+4, Z(90)+4. 
    #   Maybe +2 for [64,106] except [89,90]? Too ad hoc.
    #   Let me just guess: pos0 +2 for ord in [64,106], else +4; pos>0 always +4.
    #   But Z=90 in [64,106] contradicts. So exclude uppercase Y,Z? 
    #   Actually maybe the rule is +2 for ord in [64,106] AND ord not in uppercase letters above some point.
    #   I'll guess +2 for ord in [64,106] except [89,90], mark with ?.
    #   Actually simpler guess: +2 if 64<=ord<=106 and not (89<=ord<=90). Hmm.
    #   Let me just use: pos0 +2 if 64<=ord<=106 and ord not in (89,90), else +4.
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0 and 64 <= o <= 106 and o not in (89, 90):
            return chr(o + 2)
        return chr(o + 4)
    out = []
    for s in probe["inputs"]:
        out.append("".join(shift(c, i) for i, c in enumerate(s)))
    return {"outputs": out}
