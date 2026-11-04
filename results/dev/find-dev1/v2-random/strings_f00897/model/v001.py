def predict(probe):
    # Observations:
    # - "abc123" -> "cfg567": letters shifted +2 (a->c,b->d,c->e), digits shifted +4 (1->5,2->6,3->7)
    # - "level" -> "nizip": each letter shifted +4 (l->n,e->i,v->z,e->i,l->p)
    # - " Zebralower" -> "$^ifveps{iv": space->$, Z->^, e->i, b->f, r->v, a->e, l->p, o->s, w->{, e->i, r->v
    #   Wait: Z->^ is +4 in ASCII (Z=90, ^=94). e->i +4, b->f +4, r->v +4, a->e +4, l->p +4, o->s +4, w->{ +4, e->i +4, r->v +4. Space(32)->$(36) +4. So +4 shift on all chars!
    # - "Hello World function lazy" -> "Jipps$[svph$jyrgxmsr$pe~}": H->J +2? H=72,J=74 +2. e->i +4? e=101,i=105 +4. Hmm mixed.
    #   Let's check: H->J (+2), e->i(+4), l->p(+4), l->p(+4), o->s(+4), space->$(+4), W->[(+4? W=87,[=91 +4), o->s+4, r->v+4, l->p+4, d->h+4, space->$+4, f->j+4, u->y+4, n->r+4, c->g+4, t->x+4, i->m+4, o->s+4, n->r+4, space->$+4, l->p+4, a->e+4, z->~+4, y->}+4.
    #   So only first char H->J is +2, rest +4? Or maybe H is uppercase and uppercase shifts +2?
    # - "bananaUPPER" -> "derereYTTIV": b->d+2, a->e+4, n->r+4, a->e+4, n->r+4, a->e+4, U->Y+4, P->T+4, P->T+4, E->I+4, R->V+4.
    #   First char b->d is +2, rest +4. Interesting.
    # - "Zebra" -> "^ifve": Z->^+4, e->i+4, b->f+4, r->v+4, a->e+4. All +4.
    # - "Example123" -> "G|eqtpi567": E->G+2, x->|+4? x=120,|=124 +4. a->e+4, m->q+4, p->t+4, l->p+4, e->i+4, digits 1->5,2->6,3->7 +4.
    #   First char E->G +2, rest +4.
    # - "test case" -> "viwx$gewi": t->v+2, e->i+4, s->w+4, t->x+4, space->$+4, c->g+4, a->e+4, s->w+4, e->i+4.
    #   First char t->v +2, rest +4.
    # - "banana data banana " -> "derere$hexe$ferere$": b->d+2, a->e+4, n->r+4, a->e+4, n->r+4, a->e+4, space->$+4, d->h+4, a->e+4, t->x+4, a->e+4, space->$+4, b->f+4, a->e+4, n->r+4, a->e+4, n->r+4, a->e+4, space->$+4.
    #   First char b->d +2, rest +4.
    # - "lazy" -> "ne~}": l->n+2, a->e+4, z->~+4, y->}+4. First char +2, rest +4.
    # - "banana" -> "derere": b->d+2, rest +4.
    # - "level" -> "nizip": l->n+2, e->i+4, v->z+4, e->i+4, l->p+4. First char +2, rest +4.
    # So rule: first character shifted +2, all subsequent characters shifted +4 (in ASCII/Unicode codepoint).
    # Check "abc123": a->c+2, b->f+4, c->g+4, 1->5+4, 2->6+4, 3->7+4. Yes!
    # Check " Zebralower": space->$+4? First char space(32)->$(36) is +4, not +2. Hmm.
    #   Wait first char is space. 32+2=34='"', but observed '$'=36. So +4.
    #   Maybe rule is: first char +2 only if it's a letter? Or maybe +2 applies to first letter, and non-letters +4?
    #   Let's recheck "Hello World function lazy": H->J +2 (letter). Good.
    #   " Zebralower": first char space -> $ +4. So non-letter first char gets +4.
    #   "Example123": E->G +2 (letter).
    #   "test case": t->v +2 (letter).
    #   "banana...": b->d +2 (letter).
    #   "lazy": l->n +2 (letter).
    #   "banana": b->d +2 (letter).
    #   "level": l->n +2 (letter).
    #   "abc123": a->c +2 (letter).
    #   "Zebra": Z->^ +4?? Z is a letter! Z=90, ^=94, +4. But observed "^ifve". Hmm, that contradicts.
    #   Wait, maybe uppercase letters shift +2 and lowercase +2? Z->^ is +4 though.
    #   Let me recheck: Z=90, ^=94. +4. But H=72->J=74 +2. Both uppercase. Inconsistent!
    #   Hmm. Let me recheck "Zebra" -> "^ifve". Z(90)->^(94) +4. e(101)->i(105)+4. b(98)->f(102)+4. r(114)->v(118)+4. a(97)->e(101)+4. All +4.
    #   But "banana" -> "derere": b(98)->d(100)+2. So b->d +2 in one case, b->f +4 in "Zebra"? No, in Zebra b is second char, +4. In banana b is first char, +2.
    #   So first char +2, rest +4. But Zebra first char Z->^ is +4, not +2.
    #   Unless... maybe the shift depends on position differently. Let me reconsider.
    #   Maybe it's: shift = 2 + 2*position? Position 0: +2, position 1: +4, position 2: +6...? No, "level": l->n+2(pos0), e->i+4(pos1), v->z+4(pos2), e->i+4(pos3), l->p+4(pos4). So pos2 is +4 not +6.
    #   Maybe: first char +2, all others +4, EXCEPT uppercase first char? Z->^ +4. H->J +2. Both uppercase. Contradiction.
    #   Wait, maybe I misread. "Zebra" -> "^ifve". Let me recompute Z. Z is 90. ^ is 94. Difference 4. H is 72, J is 74, difference 2.
    #   Hmm, what if the rule is: shift by 2 if the character is a lowercase letter at position 0? b->d, l->n, t->v, a->c, E? E is uppercase ->G +2. H->J +2. So uppercase first also +2 sometimes.
    #   Z->^ +4 is the odd one. Maybe Z wraps? Z+2 = '\' (92). But observed ^ (94). Hmm.
    #   What if it's ROT-like with wraparound? Z+2 wraps to B? No, observed ^.
    #   Let me reconsider: maybe the shift is +2 for the first character, but for uppercase letters it's... no.
    #   Actually wait: maybe the rule is: shift +2 for first char, +4 for rest, but Z is special because Z+2='\\' which... no.
    #   Let me recheck the string: "Zebra" -> "^ifve". Z(90) ^(94). Yes +4.
    #   Hmm, could it be that the first character shift is +2 only if result stays a letter, else +4? Z+2 = '\' not a letter, so +4? But space+2='"' not letter, observed +4. That fits! First char: if char+2 is a letter, use +2; else +4.
    #   Check: H+2=J letter -> +2. b+2=d letter -> +2. l+2=n -> +2. t+2=v -> +2. a+2=c -> +2. E+2=G -> +2. Z+2='\' not letter -> +4. space+2='"' not letter -> +4. 
    #   That's a plausible rule! But it's a bit odd. Alternatively: first char +2 if it's a letter (a-z, A-Z), else +4. Z is a letter though, so that fails.
    #   Hmm, but maybe simpler: the shift is +2 for first char, but Z->^ is +4... 
    #   Let me check if maybe it's not position-based but something else. What if the whole string is shifted by +4, but the first character is shifted by +2 only when... 
    #   Actually, let me reconsider "Hello World function lazy": H->J+2, e->i+4, l->p+4... wait e->i is +4? e=101, i=105, +4. Yes.
    #   So first char +2, rest +4, with Z exception.
    #   Let me check "Example123": E->G+2, x->|+4 (x=120,|=124). Yes.
    #   OK so the "first char +2 if result is letter else +4" rule works for all data. But it's weird.
    #   Alternative: maybe the shift is +2 for the first character, and +4 for the rest, but the first character is shifted +2 in the alphabet with wraparound for letters only, and non-letters +4. Z+2 wraps to B? No, observed ^.
    #   Hmm, what if it's: shift = 2 for position 0, 4 for others, but Z is at end of alphabet and 90+2=92='\', which is not what we see.
    #   Let me just go with: first char +2 if it's a letter AND char+2 is still a letter (i.e., not Z or z), else +4. Actually z+2 = | (124), not letter. Let's check if there's a z first char case... "lazy" first char l. No z first char.
    #   Actually, simpler hypothesis: first character +2, all others +4, but with the caveat that if first char +2 would leave the letter range, use +4. Hmm.
    #   Wait, maybe the rule is different: maybe it's +2 for the first character only if it's lowercase or specific uppercase? H->J+2 (uppercase), E->G+2 (uppercase), Z->^+4 (uppercase). So not case-based.
    #   Let me think about Z differently. What if the shift is +2 for first char, but the alphabet is considered circular for letters? Z+2 -> B. But observed ^. So no.
    #   What if the shift is actually +4 for everything, and the first char appears +2 because... no, b->d is clearly +2.
    #   Hmm, let me recheck "bananaUPPER" -> "derereYTTIV": b->d+2, a->e+4, n->r+4, a->e+4, n->r+4, a->e+4, U->Y+4, P->T+4, P->T+4, E->I+4, R->V+4. Yes first +2 rest +4.
    #   OK. I'll go with: position 0: +2 if (char is letter and char+2 is letter) else +4; positions >0: +4.
    #   Actually, let me reconsider: maybe it's +2 for first char always, but Z is special because... hmm. Actually maybe the rule is +2 for first char, but the shift is applied to the character code and Z=90, +2=92='\'. But observed ^=94. So that's +4.
    #   What if the first character shift is +2 for lowercase and +2 for uppercase except Z? That's ad hoc.
    #   Let me look for another pattern. What if the shift is based on the character itself: shift = 2 + (position>0)*2, but for Z it's different... 
    #   Actually, maybe I should reconsider: what if the rule is +4 for all characters, but the first character is +2 only when the string starts with a letter that isn't Z? Hmm.
    #   Let me check "abc123": a->c+2. a+2=c letter. Good.
    #   I'll implement: for i,ch: shift = 2 if i==0 and ch.isalpha() and chr(ord(ch)+2).isalpha() else 4. Wait but Z+2='\' not alpha, so +4. Good. But what about z? z+2='|' not alpha, so +4. No data on z first.
    #   Actually, hold on. Let me reconsider whether it's really position-based. What if the rule is: shift +2 for the first character, +4 for the rest, but the first character is shifted +2 in a circular alphabet for letters (a-z, A-Z separately)? Z+2 -> B. But observed ^. So no.
    #   What if it's: the first character is shifted +2, but if it's 'Z' it's shifted +4? That's a special case.
    #   Hmm, let me reconsider the whole thing. Maybe the shift is +2 for the first character and +4 for the rest, but the first character is shifted +2 only if it's a lowercase letter? b,l,t,a are lowercase -> +2. H,E are uppercase -> +2. So no.
    #   Wait, H->J is +2, E->G is +2, Z->^ is +4. All uppercase. So Z is the exception among uppercase.
    #   Maybe the rule is: first char +2, but if char+2 is not a letter, +4. That handles Z and space. Let's go with that.
    #   Actually, let me reconsider: maybe the rule is simpler: shift = 2 for first char, 4 for rest, but the shift is applied modulo something? No.
    #   Let me just go with: first char: +2 if result is alphanumeric? Z+2='\' not alnum -> +4. space+2='"' not alnum -> +4. H+2=J alnum -> +2. b+2=d alnum -> +2. That works too. But digits? "abc123" first char a. No digit-first case.
    #   I'll use: first char +2 if chr(ord(c)+2).isalnum() else +4. Hmm, but that's arbitrary. Let me think if there's a cleaner rule.
    #   Actually, maybe the rule is: shift +2 for the first character, +4 for the rest, but the shift is +4 for the first character if it's 'Z' or a space or... 
    #   Let me look at it from a different angle. What if the function is: shift each character by 2 + 2*min(i,1)? That gives +2 for i=0, +4 for i>=1. But Z breaks it.
    #   What if the function is: shift by 2 for the first character, 4 for the rest, but the first character is shifted by 2 only if it's not 'Z'? 
    #   I think the cleanest hypothesis that fits all data: first character shifted +2 if it's a letter other than Z (and maybe z), else +4; all other characters +4. But that's ugly.
    #   Let me reconsider: maybe it's +2 for the first character, and +4 for the rest, but the first character is shifted +2 in the ASCII table, and Z+2='\', but the observed is '^'. Wait, could I have misread the output? "^ifve" - ^ is 94. Z is 90. 94-90=4. Yes.
    #   Hmm, what if the rule is: shift +2 for the first character, but the shift is +4 for the first character if it's uppercase? H->J is +2 though. So no.
    #   What if the rule is: shift +2 for the first character, but the shift is +4 for the first character if it's 'Z'? That's a special case but maybe the box does that.
    #   Actually, wait. Let me reconsider "Zebra". What if the first character is shifted +4 because... hmm. What if the rule is: shift +2 for the first character, +4 for the rest, but the first character is shifted +2 only if it's a lowercase letter? b,l,t,a are lowercase -> +2. H,E are uppercase -> +2 though. So no.
    #   Let me check: is there any uppercase first char other than H, E, Z? "Hello" H, "Example" E, "Zebra" Z. H->J+2, E->G+2, Z->^+4. So Z is the only uppercase that's +4.
    #   Maybe the rule is: shift +2 for the first character, but if the character is 'Z' (or 'z'), shift +4? That's a special case but plausible if the box does something like "shift +2, but wrap around for letters"? Z+2 wraps to B, not ^. So no.
    #   I'll go with: first char +2 if chr(ord(c)+2).isalpha() else +4. This handles Z (not alpha) and space (not alpha). For lowercase z, z+2='|' not alpha -> +4. No data but plausible.
    #   Actually, let me reconsider: maybe the rule is +2 for the first character, and +4 for the rest, but the first character is shifted +2 only if it's a letter AND not 'Z'? That's the same as above for letters.
    #   Hmm, but what about 'z'? z+2='|' not letter. So +4. But maybe the box does +2 for z too? Unknown.
    #   Let me just implement: shift = 2 if i==0 and c.isalpha() and chr(ord(c)+2).isalpha() else 4. Wait, but for 'Z', c.isalpha() is True, chr(90+2)='\' not alpha, so +4. Good.
    #   Actually, I realize there might be a simpler rule: shift +2 for the first character, +4 for the rest, but the first character is shifted +2 only if it's a letter that isn't 'Z' (case-sensitive). Hmm.
    #   Let me think about whether the box might be doing something like: for each character, shift by 2 if it's the first character and it's a letter, else shift by 4. But Z is a letter and gets +4. So that fails.
    #   What if the rule is: shift by 2 if the character is the first character AND the character is in 'a-yA-Y' (excluding Z and z)? That's ad hoc.
    #   I'll go with the "result is alpha" rule. It's the most natural: first char +2 if result stays a letter, else +4.
    #   Wait, but what about digits? "abc123" first char a. No digit-first case. If first char is '1', 1+2='3' which is alnum but not alpha. Would it be +2 or +4? Unknown. I'll guess +4 for non-alpha first char (since space got +4).
    #   Actually, let me reconsider: maybe the rule is simply: first character +2, all others +4, but the first character is shifted +2 only if it's a letter (a-z, A-Z) AND the result is also a letter. For Z, result is not a letter, so +4. For space, not a letter, so +4. This is my rule.
    #   Let me also consider: maybe the shift is +2 for the first character, +4 for the rest, but the first character is shifted +2 only if it's a lowercase letter? No, H and E are uppercase and +2.
    #   OK, I'll implement: for i, c: if i==0 and c.isalpha() and chr(ord(c)+2).isalpha(): shift=2 else shift=4. Then new char = chr(ord(c)+shift).
    #   Wait, but what about 'z'? z+2='|' not alpha, so +4. But maybe the box does +2 for z? Unknown. I'll go with +4.
    #   Actually, let me reconsider the whole thing. Maybe the rule is: shift +2 for the first character, +4 for the rest, but the first character is shifted +2 only if it's not 'Z' and not 'z'? That's the same as "result is alpha" for letters.
    #   Hmm, but what if the first character is a digit? 1+2=3, which is a digit. Would it be +2? Unknown. I'll guess +4 for non-alpha first char (since space got +4).
    #   Let me just go with: first char: +2 if c.isalpha() and chr(ord(c)+2).isalpha() else +4. Others: +4.
    #   Actually, I want to double-check "Hello World function lazy" first char H->J. H=72, J=74, +2. chr(72+2)=J is alpha. Good.
    #   "Example123" E->G. E=69, G=71, +2. chr(69+2)=G alpha. Good.
    #   "Zebra" Z->^. Z=90, chr(92)='\' not alpha, so +4 -> ^. Good.
    #   " Zebralower" space->$. space not alpha, +4 -> $. Good.
    #   "abc123" a->c. a=97, chr(99)=c alpha, +2. Good.
    #   "level" l->n. l=108, chr(110)=n alpha, +2. Good.
    #   "banana" b->d. b=98, chr(100)=d alpha, +2. Good.
    #   "lazy" l->n. +2. Good.
    #   "test case" t->v. t=116, chr(118)=v alpha, +2. Good.
    #   "banana data banana " b->d. +2. Good.
    #   "bananaUPPER" b->d. +2. Good.
    #   All fit!
    #   So the rule: for each character at position i:
    #     if i == 0 and c.isalpha() and chr(ord(c)+2).isalpha(): shift = 2
    #     else: shift = 4
    #   new_c = chr(ord(c) + shift)
    #   This is a Caesar-like cipher with position-dependent shift.
    #   Let me write the code.
    def transform(s):
        out = []
        for i, c in enumerate(s):
            if i == 0 and c.isalpha() and chr(ord(c)+2).isalpha():
                shift = 2
            else:
                shift = 4
            out.append(chr(ord(c) + shift))
        return ''.join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
