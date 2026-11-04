def predict(probe):
    # Caesar shift +1 on letters (preserving case) [E1, E2]
    # Digits shifted +1 too (0->1, 9->: ) [E2: "0123456789"->"12345Y6789:"]
    # Wait: digits show "12345Y6789:" - the 5 became Y, not 6. So digits are NOT simply +1.
    # Let's re-examine: "0123456789" -> "12345Y6789:"
    #   0->1, 1->2, 2->3, 3->4, 4->5, 5->Y, 6->6, 7->7, 8->8, 9->:
    # Hmm. Only position 5 (the char '5') became 'Y'. And '9'->':' is +1 in ASCII.
    # Actually look: '0'->'1'(+1), '1'->'2'(+1), '2'->'3', '3'->'4', '4'->'5', then '5'->'Y'?? 
    # And '6'->'6', '7'->'7', '8'->'8', '9'->':'.
    # That's inconsistent. Let's check "aA0 zZ!" -> "bB1Y!{[\""
    #   a->b, A->B, 0->1, space->Y, z->{, Z->[, !->"
    # So space->Y, !->". These are +1 in ASCII: ' '=32->33='!', but we got 'Y'. No.
    # '!'=33 -> '"'=34: +1 ASCII. space=32 -> 'Y'=89? No.
    # Hmm space->Y. And in "Hello World" -> "IfmmpY!Xpsme": space->Y.
    # So space maps to 'Y'. And '5' maps to 'Y' too? In "0123456789": position 5 is '5'->'Y'.
    # Wait maybe it's not per-character position. Let me recount "0123456789"->"12345Y6789:".
    # chars: 0,1,2,3,4,5,6,7,8,9 -> 1,2,3,4,5,Y,6,7,8,9,:
    # That's 10 in, 11 out! Extra char. So '5' -> 'Y6'? No... 
    # Actually output "12345Y6789:" has 11 chars. Input 10. So one char expanded.
    # Hmm, maybe '5' -> 'Y' and something. Let's count: 1,2,3,4,5,Y,6,7,8,9,: = 11.
    # So input '5' produced 'Y6'? Or '5'->'Y' and '6'->'6'... but then where's extra?
    # 0->1,1->2,2->3,3->4,4->5,5->Y,6->6,7->7,8->8,9->:  that's 10 outputs: 1,2,3,4,5,Y,6,7,8,9,: = 11. 
    # I miscounted: 1,2,3,4,5,Y,6,7,8,9,: is 11 chars. So one input char gave two.
    # Likely '5' -> 'Y' is wrong. Maybe '5'->'Y'? Let's think differently.
    # What if it's Caesar +1 on letters, and space->'Y'? No, space->'Y' weird.
    # Reconsider: maybe the shift is +1 for letters, and for non-letters something else.
    # "aA0 zZ!" -> "bB1Y!{[\"": a->b(+1), A->B(+1), 0->1(+1), space->Y, z->{(+1), Z->[(+1), !->"(+1)
    # So space->Y is the odd one. Space is 32. Y is 89. 
    # In "Hello World": H->I,e->f,l->m,l->m,o->p, space->Y, W->X,o->p,r->s,l->m,d->e
    # "IfmmpY!Xpsme" = I,f,m,m,p,Y,!,X,p,s,m,e. Wait that's space->Y then W->!? 
    # "Hello World" -> "IfmmpY!Xpsme": H->I,e->f,l->m,l->m,o->p,space->Y,W->!,o->p,r->s,l->m,d->e
    # So W->! ? That's not +1. Hmm. W=87, !=33. 
    # Wait maybe space->Y and W->! ... no.
    # Let me recount "IfmmpY!Xpsme": I f m m p Y ! X p s m e = 12 chars. "Hello World" = 11 chars.
    # So one expansion again. H->I,e->f,l->m,l->m,o->p,space->Y, then W->!? 
    # Actually maybe space->'Y!'? No.
    # Alternative: maybe it's not Caesar. Let's look at "abcxyz"->"bcdYyz{": a->b,b->c,c->d,x->Y,y->y,z->{
    # x->Y! x=120, Y=89. y->y (unchanged), z->{ (+1). Weird.
    # "ABCXYZ"->"BCDYYZ[": A->B,B->C,C->D,X->Y,Y->Y,Z->[
    # So X->Y, Y->Y, Z->[. X->Y is +1, Y->Y is 0, Z->[ is +1.
    # Hmm Y stays Y. Interesting: Y is special.
    # "level"->"mfYwfm": l->m,e->f,v->Y,e->f,l->m. So v->Y! v=118, Y=89.
    # "bananaUPPER"->"cboboYbVQQFS": b->c,a->b,n->o,a->b,n->o,a->b,U->Y? 
    #   b,a,n,a,n,a,U,P,P,E,R -> c,b,o,b,o,b,Y,V,Q,Q,F,S
    #   U->Y, P->V, P->Q, E->F, R->S. Hmm U->Y? P->V then P->Q inconsistent!
    # Wait "cboboYbVQQFS": c,b,o,b,o,Y,b,V,Q,Q,F,S = 12 chars, input 11. Expansion again.
    # So b->c,a->b,n->o,a->b,n->o,a->b, then U->Y? and P->V,P->Q,E->F,R->S
    # Hmm P->V and P->Q differ. So position matters, not just char.
    # Let me reconsider: maybe there's a fixed string inserted, like "Y" appears.
    # Notice 'Y' appears in many outputs: "bcdYyz{", "mfYwfm", "cboboYbVQQFS", "IfmmpY!Xpsme", "bB1Y!{[\"", "12345Y6789:"
    # Y appears at a specific position? In "abcxyz"(6)->"bcdYyz{"(7): Y at index 3.
    # "level"(5)->"mfYwfm"(6): Y at index 2.
    # "bananaUPPER"(11)->"cboboYbVQQFS"(12): Y at index 5.
    # "Hello World"(11)->"IfmmpY!Xpsme"(12): Y at index 5.
    # "aA0 zZ!"(7)->"bB1Y!{[\""(8): Y at index 3.
    # "0123456789"(10)->"12345Y6789:"(11): Y at index 5.
    # Hmm positions: 3,2,5,5,3,5. Not fixed.
    # Length of input: 6->3, 5->2, 11->5, 11->5, 7->3, 10->5.
    # 6->3 (half), 5->2 (floor half), 11->5 (floor half), 7->3 (floor half), 10->5 (half).
    # So Y inserted at index floor(len/2)! 
    # Check: len 6 -> index 3. len 5 -> 2. len 11 -> 5. len 7 -> 3. len 10 -> 5. YES!
    # So the box inserts 'Y' at the middle (floor(len/2)) of the input, then applies Caesar +1 to letters?
    # Let's verify: "abcxyz" insert Y at 3: "abcYxyz", then Caesar+1 letters: "bcdYyz{"? 
    #   a->b,b->c,c->d,Y->Y(not letter? Y is letter, +1=Z). Hmm Y->Y not Z.
    #   Actually if Y is inserted after shift, then shift "abcxyz"->"bcdyz{" then insert Y at 3: "bcdYyz{". YES!
    # Check "level": shift -> "mfWfm"? l->m,e->f,v->w,e->f,l->m = "mfwfm". Insert Y at 2: "mfYwfm". YES!
    # Check "Hello World": shift -> "Ifmmp!Xpsme" (space->! is +1 ASCII? space=32, !=33 yes +1).
    #   H->I,e->f,l->m,l->m,o->p,space->!,W->X,o->p,r->s,l->m,d->e = "Ifmmp!Xpsme"
    #   Insert Y at 5: "IfmmpY!Xpsme". YES!
    # Check "0123456789": shift +1 ASCII: 0->1,1->2,...,9->: = "123456789:". Insert Y at 5: "12345Y6789:". YES!
    # Check "aA0 zZ!": shift +1: a->b,A->B,0->1,space->!,z->{,Z->[,!->" = "bB1!{[\"". Insert Y at 3: "bB1Y!{[\"". YES!
    # Check "bananaUPPER": shift: b->c,a->b,n->o,a->b,n->o,a->b,U->V,P->Q,P->Q,E->F,R->S = "cboboVQQFS". 
    #   Insert Y at 5: "cboboYVQQFS". But observed "cboboYbVQQFS"! Extra 'b'.
    #   Hmm observed: c,b,o,b,o,Y,b,V,Q,Q,F,S. So "cbobo" + "Y" + "bVQQFS". 
    #   Shifted "bananaUPPER" = c,b,o,b,o,b,V,Q,Q,F,S = "cbobobVQQFS" (11 chars). 
    #   Insert Y at 5: "cboboYbVQQFS". YES! I miscounted n->o, a->b... "banana"->"cbobob". Right, 6 chars.
    # So rule: Caesar +1 on ALL characters (ASCII +1), then insert 'Y' at index floor(len/2).
    # Wait, but "Zebralower"->"![fcsYbmpxfs": Z->[? Z=90, [=91 +1 yes. e->f,b->c,r->s,a->b,l->m,o->p,w->x,e->f,r->s
    #   "Zebralower" shift: [fcsbmp xfs = "[fcsbmpxfs" (10 chars). Insert Y at 5: "[fcsbY mpxfs" = "[fcsbYmpxfs".
    #   Observed "![fcsYbmpxfs". Hmm leading '!' and Y at index 5.
    #   Wait " Zebralower" has leading space! Input was " Zebralower" (with space). space->! (+1). 
    #   So " Zebralower" shift: !, [, f, c, s, b, m, p, x, f, s = "![fcsbmpxfs" (11). Insert Y at 5: "![fcsYbmpxfs". YES!
    # Check "Hello World function lazy": shift each char +1: I,f,m,m,p,!X,p,s,m,e,!g,v,o,d,u,j,p,o,!m,b,z,{ 
    #   "Hello World function lazy" = H e l l o _ W o r l d _ f u n c t i o n _ l a z y
    #   shift: I f m m p ! X p s m e ! g v o d u j p o ! m b z {
    #   = "Ifmmp!Xpsme!gvodujpo!mbz{" (24 chars). Insert Y at 12: "Ifmmp!Xpsme!Ygvodujpo!mbz{"
    #   Observed: "Ifmmp!Xpsme!Ygvodujpo!mb{z". Close but "mb{z" vs "mbz{". 
    #   Hmm observed ends "mb{z" but shift gives "mbz{". Let me recheck: l->m,a->b,z->{,y->z. So "lazy"->"mb{z". 
    #   I made error: z->{ and y->z, so "lazy"->"mb{z". YES matches!
    # Check "Zebra"->"[fYcsb": shift Z->[,e->f,b->c,r->s,a->b = "[fcsb" (5). Insert Y at 2: "[fYcsb". YES!
    # Check "abc123"->"bcdY234": shift a->b,b->c,c->d,1->2,2->3,3->4 = "bcd234" (6). Insert Y at 3: "bcdY234". YES!
    # Great, rule confirmed: shift every char +1 (ord+1), then insert 'Y' at index floor(len/2).
    def shift(s):
        return ''.join(chr(ord(c)+1) for c in s)
    def transform(s):
        t = shift(s)
        i = len(s)//2
        return t[:i] + 'Y' + t[i:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
