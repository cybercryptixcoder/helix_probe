def predict(probe):
    # Most chars shift +8 [E1, E2]
    # BUT: 't' -> 'm' (-7), 'e' -> 'm' (+8? no: 'test'->'m{(k' means t->m, e->{, s->k, t->m)
    #   'test case' -> 'm{(ki{m': t->m, e->{, s->k, t->m, space->(, c->k, a->i, s->k, e->{
    #   So t->m is -7, e->{ is +8, s->k is +8, c->k is +8, a->i is +8
    # 'data' -> 'lii(': d->l(+8), a->i(+8), t->i(-11?), a->(??)
    #   wait 'banana data banana ' -> 'jivivi(lii(jivivi('
    #   b->j(+8) a->i(+8) n->v(+8) a->i(+8) n->v(+8) a->i(+8) space->( d->l(+8) a->i(+8) t->i a->( 
    #   Hmm 'data' -> 'lii(' : d->l(+8), a->i(+8), t->i, a->(
    #   But 'banana'->'jivivi' has a->i consistently. In 'data', second a -> '(' which is +8 from 'i'? no.
    # Let's reconsider: maybe it's not per-char shift but something else.
    # 'level'->'tm~mt': l->t(+8), e->m(+8), v->~(+8), e->m(+8), l->t(+8). Consistent +8.
    # 'Zebra'->'bmjzi': Z->b(+8), e->m(+8), b->j(+8), r->z(+8), a->i(+8). Consistent +8.
    # 'abc123'->'ijk9:;': +8 all.
    # 'Example123'->'M\x80iuxtm9:;': E->M(+8), x->\x80(+8), a->i, m->u, p->x, l->t, e->m, 1->9,2->:,3->;. +8 all.
    # 'lazy'->'ti\x82\x81': l->t, a->i, z->\x82, y->\x81. +8 all.
    # 'bananaUPPER'->'jivivi]XXMZ': b->j,a->i,n->v,a->i,n->v,a->i,U->],P->X,P->X,E->M,R->Z. +8 all.
    # 'Hello World function lazy'->'Pmttw(_wztl(n}vkqwv(ti\x82\x81': +8 all.
    # ' Zebralower'->'(bmjzitw\x7fmz': +8 all.
    # So where does E2 fail? 'test case'->'m{(ki{m'
    #   t+8 = |, but observed m. e+8=m ok. s+8={ ok. t+8=| but observed m. space+8=( ok. c+8=k ok. a+8=i ok. s+8={ ok. e+8=m ok.
    #   So 't' -> 'm' instead of '|'. That's -7.
    # 'banana data banana '->'jivivi(lii(jivivi('
    #   b->j,a->i,n->v,a->i,n->v,a->i,space->(,d->l,a->i,t->i,a->(,space->(,b->j,a->i,n->v,a->i,n->v,a->i,space->(
    #   t->i here (t+8=|, but observed i). a->( (a+8=i, observed (). 
    #   Hmm 'data'->'lii(': d->l(+8), a->i(+8), t->i, a->(
    #   So t->i and a->( . That's weird. t->i is -11, a->( is -25.
    # Wait, maybe it's not char-by-char. Maybe 'ta' -> 'i(' ? 
    # Let's look: 'data' -> 'lii('. If we shift +8: 'li(i'? d+8=l, a+8=i, t+8=|, a+8=i => 'li|i'. Observed 'lii('.
    # Hmm. What if the box does something like: shift +8, but then... no.
    # Let's check 'test case' with +8: '|m{|(ki{m'. Observed 'm{(ki{m'. 
    #   Position 0: | vs m. Position 3: | vs m. Both are 't'->'m'.
    # 'banana data banana ': +8 gives 'jivivi(li|i(jivivi('. Observed 'jivivi(lii(jivivi('.
    #   Position 9: t->i (expected |). Position 11: a->( (expected i).
    # Hmm wait let me recount 'banana data banana ':
    #   b a n a n a _ d a t a _ b a n a n a _
    #   0 1 2 3 4 5 6 7 8 9 10 11 12...
    #   +8: j i v i v i ( l i | i ( j i v i v i (
    #   obs: j i v i v i ( l i i ( j i v i v i (
    #   So pos 9: t->i, pos 10: a->( . 
    # Wait pos 10 is 'a', +8 = i, but observed '('. And pos 11 is space, +8=(, observed '('.
    #   Hmm so 'a ' -> '((' ? No: pos 10 a->(, pos 11 space->(. 
    #   Actually maybe 'ta' -> 'i('? t->i, a->(. 
    # Let me reconsider. In 'test', t->m. In 'data', t->i. Different! So t's output depends on context.
    # Hmm. What if it's a Caesar shift but the shift amount varies? 
    # Or maybe it's: shift +8, but 't' is special? No, t->m in 'test' (-7), t->i in 'data' (-11).
    # Wait, maybe I'm miscounting. Let me carefully redo 'test case':
    #   t e s t _ c a s e
    #   +8: | m { | ( k i { m
    #   obs: m { ( k i { m  -- that's only 8 chars? No, 'test case' is 9 chars.
    #   obs 'm{(ki{m' is 7 chars! Wait: m { ( k i { m = 7 chars.
    #   But 'test case' is 9 chars. So output is SHORTER. 
    #   Hmm! 'test case' -> 'm{(ki{m' (7 chars). 
    #   Let's see: t e s t _ c a s e. Output m { ( k i { m.
    #   Maybe 'te' -> 'm'? 'st' -> '{'? No...
    #   Actually: 'test case' has 9 chars, output 7. Two chars removed.
    #   'banana data banana ' has 19 chars, output 'jivivi(lii(jivivi(' = 18 chars. One removed.
    #   'Example123' 10 chars -> 'M\x80iuxtm9:;' 10 chars. Same.
    #   'lazy' 4 -> 4. 'banana' 6->6. 'level' 5->5.
    #   So some chars get dropped/merged.
    # Let's look at 'banana data banana ' (19) -> 'jivivi(lii(jivivi(' (18). One char dropped.
    #   +8 of full: 'jivivi(li|i(jivivi(' (19). Observed 'jivivi(lii(jivivi(' (18).
    #   Compare: jivivi(li | i ( jivivi(  vs  jivivi(li i ( jivivi(
    #   So '|i' became 'i'? i.e., '|' dropped, leaving 'i'. But '|' is t+8. Hmm.
    #   Actually maybe 'ta' -> 'i(' : the 't' and 'a' combine? t+8=|, a+8=i. '|i' -> 'i('? 
    #   Hmm '|i' (2 chars) -> 'i(' (2 chars). So t->i, a->(. 
    #   Wait but then length same. Let me recount output: 'jivivi(lii(jivivi(' 
    #   j i v i v i ( l i i ( j i v i v i ( = 18 chars.
    #   Input 'banana data banana ' = b a n a n a _ d a t a _ b a n a n a _ = 19.
    #   So 19->18, one dropped.
    #   If 'ta'->'i(' that's 2->2, no drop. Then where's the drop?
    #   Let me align: 
    #   in:  b a n a n a _ d a t a _ b a n a n a _
    #   out: j i v i v i ( l i i ( j i v i v i (
    #   pos0 b->j, 1 a->i, 2 n->v, 3 a->i, 4 n->v, 5 a->i, 6 _->(, 7 d->l, 8 a->i, 9 t->i, 10 a->(, 11 _->j?? 
    #   No wait, out pos 11 is 'j' but in pos 11 is '_'. That doesn't work.
    #   Let me try: maybe the drop is at position 10 (the 'a' in 'data').
    #   in:  b a n a n a _ d a t a _ b a n a n a _
    #   out: j i v i v i ( l i i ( j i v i v i (
    #   If a at pos10 dropped: then in pos 11 '_' -> out pos 10 '('. Yes! _+8=(.
    #   Then in pos 12 b -> out pos 11 j. Yes.
    #   So the 'a' at position 10 (second a in 'data') is DROPPED.
    #   And t at pos 9 -> out pos 9 'i'. t+8=| but observed i. Hmm still t->i.
    #   Wait, unless t->i is because... hmm.
    # Let me redo 'test case' (9) -> 'm{(ki{m' (7). Two dropped.
    #   in:  t e s t _ c a s e
    #   out: m { ( k i { m
    #   pos0 t->m, 1 e->{, 2 s->(, 3 t->k?? no.
    #   Hmm. Let's try: t->m, e->{, s->(, then t dropped? 
    #   in: t e s t _ c a s e
    #   out: m { ( k i { m
    #   If t(pos0)->m, e->{, s->(, t(pos3) dropped, _->k?? no _+8=( not k.
    #   Hmm. Let me try different alignment.
    #   Maybe 'te'->'m'? No.
    #   What if s->( and t->k? s+8={, not (. 
    #   Let me think: maybe it's not +8 for all. Let me look at 'test case' output chars: m { ( k i { m
    #   m = t+? t=116, m=109, diff -7.
    #   { = e+? e=101, {=123, diff +22.
    #   ( = s+? s=115, (=40, diff -75.
    #   Hmm inconsistent. Maybe I'm misreading.
    # Let me reconsider entirely. Maybe the box does something like: reverse, or shift by position.
    # 'level'->'tm~mt'. l e v e l -> t m ~ m t. 
    #   l->t(+8), e->m(+8), v->~(+8), e->m(+8), l->t(+8). All +8. Palindrome preserved.
    # 'abc123'->'ijk9:;' all +8.
    # 'Zebra'->'bmjzi' all +8.
    # 'Example123'->'M\x80iuxtm9:;' all +8.
    # 'lazy'->'ti\x82\x81' all +8.
    # 'banana'->'jivivi' all +8.
    # 'bananaUPPER'->'jivivi]XXMZ' all +8.
    # 'Hello World function lazy'->'Pmttw(_wztl(n}vkqwv(ti\x82\x81' all +8.
    # ' Zebralower'->'(bmjzitw\x7fmz' all +8.
    # So most are pure +8. Only 'test case' and 'banana data banana ' differ.
    # What's special? Both contain 'ta'? 'test' has 'te', 'data' has 'ta'. 
    # 'test case': t e s t _ c a s e. Contains 'st' and 'te'.
    # 'banana data banana ': contains 'ta'.
    # Hmm 'Hello World function lazy' contains 't' in 'function' and 'World'? 
    #   'function' has 'ti' -> 'ti\x82\x81'? no wait 'lazy'->'ti\x82\x81'. 
    #   'function' -> 'n}vkqwv'. f->n(+8), u->}(+8), n->v, c->k, t->|? but observed... 
    #   'function' = f u n c t i o n. +8: n } v k | q w v. 
    #   In full output 'Pmttw(_wztl(n}vkqwv(ti\x82\x81': let's find 'function' part: 'n}vkqwv'? 
    #   Wait full: P m t t w ( _ w z t l ( n } v k q w v ( t i \x82 \x81
    #   'Hello World function lazy' = H e l l o _ W o r l d _ f u n c t i o n _ l a z y
    #   +8: P m t t w ( _ w z t l ( n } v k | q w v ( t i \x82 \x81
    #   Observed: P m t t w ( _ w z t l ( n } v k q w v ( t i \x82 \x81
    #   So 'function' -> 'n}vkqwv' but +8 gives 'n}vk|qwv'. The 't' (in function) -> 'q'? 
    #   Wait 'function': f u n c t i o n -> n } v k | q w v (+8). Observed 'n}vkqwv' (7 chars, one dropped).
    #   So 't' dropped? f->n, u->}, n->v, c->k, t dropped, i->q, o->w, n->v. Yes! 't' dropped.
    #   So in 'function', the 't' is dropped.
    # Hmm so 't' sometimes dropped, sometimes shifted.
    # 'test case': t e s t _ c a s e -> m { ( k i { m (7). 
    #   If t dropped: e s t _ c a s e -> { ( | ( k i { m? no.
    #   Let me try: maybe 't' followed by certain char?
    #   'function': 'ti' -> 'q'? t dropped, i->q. So 'ti'->'q'.
    #   'test': 'te'->'m'? t dropped, e->m. So 'te'->'m'.
    #   'data': 'ta'->'i'? t dropped, a->i. So 'ta'->'i'.
    #   'lazy': no t. 'banana': no t. 'level': no t. 'Zebra': no t. 'abc123': no t.
    #   'Example123': no t. 'bananaUPPER': no t. 'Hello World': no t? 'World' has no t. 
    #   'Hello World function lazy': 'function' has 't'. 'ti'->'q'. And 'lazy' no t.
    #   ' Zebralower': no t.
    # So hypothesis: 't' is dropped, and the following char is shifted +8.
    # Check 'test case': t e s t _ c a s e
    #   t dropped, e->m. s->{. t dropped, _->(. c->k. a->i. s->{. e->m.
    #   Result: m { ( k i { m. YES! matches 'm{(ki{m'.
    # Check 'banana data banana ': 
    #   b a n a n a _ d a t a _ b a n a n a _
    #   b->j a->i n->v a->i n->v a->i _->( d->l a->i t dropped a->i _->( b->j ...
    #   Result: j i v i v i ( l i i ( j i v i v i (. YES! matches.
    # Check 'Hello World function lazy':
    #   ... f u n c t i o n ... : t dropped, i->q. 
    #   Result: ... n } v k q w v ... YES!
    # So rule: shift every char +8, EXCEPT 't' which is deleted (and its following char still shifted +8).
    # Wait, but does 't' always get deleted? What about 't' at end of string?
    # 'test' -> t e s t. t dropped, e->m, s->{, t dropped (end). Result 'm{'. 
    # But observed 'test case' -> 'm{(ki{m'. 'test' part -> 'm{'. Then space->(, case->ki{m. So 'm{(ki{m'. Yes!
    # What if 't' is last char? Then just dropped, nothing follows. 
    # Let me double check 'test case' full: t e s t _ c a s e
    #   t dropped, e->m, s->{, t dropped, _->(, c->k, a->i, s->{, e->m => 'm{(ki{m'. 
    #   Wait that's m { ( k i { m = 7 chars. Yes!
    # Great. So the rule: for each char, if char == 't', skip it; else output chr(ord(c)+8).
    # But wait, does 't' deletion affect the following char's shift? No, following char just gets +8 normally.
    # Let me verify 'function': f u n c t i o n -> f->n u->} n->v c->k t dropped i->q o->w n->v = 'n}vkqwv'. Yes.
    # Verify 'data': d a t a -> d->l a->i t dropped a->i = 'lii'. Yes matches 'lii('? 
    #   Wait 'data' -> 'lii' (3 chars). But in 'banana data banana ' we had 'data'->'lii' then space->(. 
    #   'lii(' - yes 'lii' + '(' from space. Good.
    # So the model: delete 't', shift everything else +8.
    # But wait, what about 'T' uppercase? Not tested. Assume only lowercase 't' deleted? 
    #   'bananaUPPER' has no t. 'Hello World' no t. Hmm. Let's assume only 't' (lowercase) deleted. Mark with ?.
    # Also what about 't' in other contexts? All evidence consistent.
    return {"outputs": ["".join(chr(ord(c) + 8) for c in s if c != 't') for s in probe["inputs"]]}
