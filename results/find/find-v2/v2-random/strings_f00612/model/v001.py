def predict(probe):
    # Caesar shift +1 on letters (a->b, z->a, A->B, Z->A) [E1]
    # Non-letters unchanged (digits, spaces, punctuation) [E1]
    # "abc123" -> "bcdY234": wait, 'a'->'b','b'->'c','c'->'d', then '1'->'Y'? 
    # Actually "abc123"->"bcdY234": a->b,b->c,c->d, 1->Y, 2->2, 3->3, 4->4
    # Hmm: "abc123" has 6 chars -> output "bcdY234" 6 chars. positions: a->b,b->c,c->d,1->Y,2->2,3->3... but input is abc123 (a,b,c,1,2,3) output b,c,d,Y,2,3,4? No: bcdY234 = b,c,d,Y,2,3,4 is 7 chars.
    # Let me recount: "abc123" = a b c 1 2 3 (6). "bcdY234" = b c d Y 2 3 4 (7). Length differs!
    # "level"->"mfYwfm": l->m,e->f,v->Y,e->w,l->f,m->m? level=5, mfYwfm=6. length+1.
    # " Zebralower"->"![fcsYbmpxfs": 11 -> 12. +1
    # "Hello World function lazy"->"Ifmmp!Xpsme!Ygvodujpo!mb{z": 25 -> 26. +1
    # "bananaUPPER"->"cboboYbVQQFS": 11 -> 12. +1
    # "Zebra"->"[fYcsb": 5 -> 6. +1
    # So output length = input length + 1. There's an inserted char.
    # Pattern: shift each letter +1, and insert 'Y' somewhere.
    # "abc123"->"bcdY234": b c d [Y] 2 3 4? but 1->2,2->3,3->4? digits shifted +1 too!
    # Wait digits: 1->2,2->3,3->4. And Y inserted after 3rd char.
    # "level"->"mfYwfm": l->m,e->f,[Y],v->w,e->f,l->m. Y inserted after 2nd char.
    # " Zebralower"->"![fcsYbmpxfs": space->!,Z->[,e->f,b->c,r->s,[Y],l->m,o->p,w->x,e->f,r->s. Y after 6th char.
    # "Hello World function lazy"->"Ifmmp!Xpsme!Ygvodujpo!mb{z": H->I,e->f,l->m,l->m,o->p,space->!,W->X,p->q,s->t,m->m,e->f,space->!,[Y],f->g,u->v,n->o,c->d,t->u,i->j,o->p,n->o,space->!,l->m,a->b,z->{,y->z. Y after 12th char.
    # "bananaUPPER"->"cboboYbVQQFS": b->c,a->b,n->o,a->b,n->o,a->b,[Y],U->V,P->Q,P->Q,E->F,R->S. Y after 6th char.
    # "Zebra"->"[fYcsb": Z->[,e->f,[Y],b->c,r->s,a->b. Y after 2nd char.
    # Insert position: abc123(3), level(2), Zebralower(6), Hello...(12), bananaUPPER(6), Zebra(2)
    # Hmm. Insert Y at position = ? Let's see: maybe after first vowel? 
    # abc123: no vowel, inserted after 3. level: after 'e'(pos2). Zebralower: after 'r'? Z-e-b-r-a... after 6th char which is 'r'? Z(1)e(2)b(3)r(4)a(5)l(6)... wait 6th is 'l'. Hmm.
    # Let me index: " Zebralower": [space,Z,e,b,r,a,l,o,w,e,r]. Insert after 6th char = after 'a'? positions: 1=space,2=Z,3=e,4=b,5=r,6=a. So after 'a'.
    # Hello World function lazy: H(1)e(2)l(3)l(4)o(5)space(6)W(7)o(8)r(9)l(10)d(11)space(12)f(13)... insert after 12th = after space. Hmm.
    # bananaUPPER: b(1)a(2)n(3)a(4)n(5)a(6)U(7)... insert after 6th = after 'a'.
    # Zebra: Z(1)e(2)b(3)... insert after 2nd = after 'e'.
    # abc123: a(1)b(2)c(3)1(4)... insert after 3rd = after 'c'.
    # level: l(1)e(2)v(3)... insert after 2nd = after 'e'.
    # So insert after... last vowel? abc123 no vowel -> after 3? level last vowel 'e' at pos2. Zebralower last vowel 'e' at pos10? but inserted at 6. Hmm no.
    # Maybe insert after position = number of... Let's think differently.
    # Actually maybe it's: shift +1, then insert 'Y' after the first occurrence of something.
    # abc123: after 'c' (3rd). level: after 'e'(2nd). Zebralower: after 'a'(6th). Hello: after space(12th). bananaUPPER: after 'a'(6th). Zebra: after 'e'(2nd).
    # Hmm 'Y' inserted... maybe after the character that when shifted... 
    # Let me look: maybe insert Y at a fixed fraction? Or after first vowel from... 
    # abc123: first vowel none. level: 'e' pos2. Zebralower: 'e' pos3? but inserted at 6.
    # Maybe after last char that is a letter before a digit/space/uppercase?
    # abc123: c before 1 (digit). level: e before v? no.
    # Let's try: insert after position = length of first "word"? 
    # abc123: whole thing one token, len 6, insert at 3? no.
    # Hmm. Maybe the Y is inserted after the first character that is >= some value?
    # Actually maybe simpler: the shift is +1, and 'Y' replaces... no, length grows.
    # Let me reconsider: maybe it's not insert, maybe one char is doubled or transformed.
    # "Zebra"->"[fYcsb": Z->[, e->f, b->c, r->s, a->b gives "[fcsb" (5). Output "[fYcsb" (6). So Y inserted between f and c, i.e., after 'e' (2nd char).
    # What's special about position 2 in Zebra? 'e' is a vowel.
    # level: insert after 'e' (2nd char, vowel).
    # abc123: insert after 'c' (3rd, consonant). Hmm no vowel before? a is vowel at pos1! So why not after a?
    # Wait abc123: a is vowel at pos 1. But inserted after pos3. Contradiction.
    # Unless... maybe insert after the LAST vowel? abc123: vowels a only at pos1 -> after pos1? but it's pos3.
    # Hmm. Let me recheck abc123 output: "bcdY234". b c d Y 2 3 4. So a->b, b->c, c->d, then Y, then 1->2,2->3,3->4. Yes insert after 3rd char 'c'.
    # Maybe insert after the character whose shifted value... 'c'->'d', and 'Y'... 
    # Or maybe: insert 'Y' after the first character that is >= 'c'? abc: c is first >=c? a,b no, c yes pos3. level: l>=c pos1? but inserted pos2. No.
    # Maybe after first char that is a consonant? abc: a vowel, b consonant pos2... but inserted pos3.
    # Hmm let me try: insert after the character at position = (something like count).
    # Positions: 3,2,6,12,6,2 for inputs of length 6,5,11,25,11,5.
    # Ratios: 3/6=.5, 2/5=.4, 6/11=.55, 12/25=.48, 6/11=.55, 2/5=.4.
    # Hmm ~half. Maybe insert at middle? floor(len/2)? 
    # len6->3 yes. len5->2 yes (floor 2.5=2). len11->5? but we got 6. Hmm floor(11/2)=5, but got 6. ceil(11/2)=6 yes! len25->ceil=13? got 12. floor=12 yes. len11->6 (ceil), len5->2(floor), len6->3.
    # Inconsistent. Let me recompute Zebralower length: " Zebralower" = space+Zebralower = 1+10=11. Insert after 6th. ceil(11/2)=6. ok.
    # Hello World function lazy: count: "Hello World function lazy". H-e-l-l-o(5) space(6) W-o-r-l-d(11) space(12) f-u-n-c-t-i-o-n(20) space(21) l-a-z-y(25). len25. insert after 12. floor(25/2)=12. 
    # So len6->3, len5->2, len11->6, len25->12, len11->6, len5->2.
    # len5->2, len6->3, len11->6, len25->12. 
    # floor((len+1)/2)? len5->3 no. 
    # round(len/2)? len5->2 (round 2.5=2 in banker's? or 3). len11->6 (round 5.5=6). len25->12 (round 12.5=12 banker's). len6->3, len5->2.
    # Banker's rounding: round(2.5)=2, round(5.5)=6, round(12.5)=12, round(3)=3, round(2.5)=2. YES! All match!
    # So insert 'Y' at position round(len/2) (banker's rounding), i.e., after that many chars.
    # Actually let's verify: len6 round(3)=3 insert after 3. len5 round(2.5)=2. len11 round(5.5)=6. len25 round(12.5)=12. 
    # Great.
    # Now the shift: letters +1 (z->a? test: 'z' in lazy -> '{'? output mb{z, so z->{. That's +1 in ASCII, not wrapping! a->b... z->{. So it's ASCII +1 for letters, not Caesar wrap.
    # Check: 'Z'->'[' (Zebra). Yes ASCII+1. 'A'? bananaUPPER: U->V,P->Q,P->Q,E->F,R->S yes +1.
    # Digits: 1->2,2->3,3->4 yes +1. 
    # Space->'!' (space is 32, ! is 33) +1. Yes!
    # So EVERY character is shifted +1 in ASCII, and 'Y' inserted at position round(len/2).
    # Check "Hello World function lazy": space->! yes. 
    # So: shift every char +1 (ord+1), then insert 'Y' after round(len/2) chars.
    # Wait but does insertion happen before or after shift? 'Y' is literal Y (not shifted). If we shift first then insert Y, Y stays Y. Good.
    # Verify "abc123": shift -> "bcd234", insert Y after 3 -> "bcdY234". ✓
    # "level": shift->"mfXfm"? l->m,e->f,v->w,e->f,l->m = "mfwfm", insert Y after 2 -> "mfYwfm". ✓
    # "Zebra": shift->"[fcsb", insert after 2 -> "[fYcsb". ✓
    import math
    def transform(s):
        shifted = ''.join(chr(ord(c)+1) for c in s)
        n = len(s)
        # banker's rounding of n/2
        pos = round(n/2)
        return shifted[:pos] + 'Y' + shifted[pos:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
