def predict(probe):
    # Every character's code point is increased by 1 [E1: a->B, 1->2, !->", space->!]
    # But the RESULT is then uppercased? No — check: 'hello world'->'Ifmmp!xpsme' preserves case of shifted chars.
    # Actually: lowercase letters become UPPERCASE of (char+1). E4: b->C, m->N, x->Y, bmx->Cny, bMx->Cny.
    # Uppercase letters: B->C, M->N, X->Y, BMX->Cny (all uppercase!). Hello World->Ifmmp!xpsme.
    # So: shift by +1, then uppercase the whole result? Check E1: 'Hello'->'Ifmmp' (H->I upper, e->f lower...).
    # 'hello world'->'Ifmmp!xpsme': h->I (upper!), e->f (lower), l->m, l->m, o->p, space->!, w->x, o->p, r->s, l->m, d->e.
    # Only first char uppercased? 'hello world' -> 'Ifmmp!xpsme' yes only h->I is upper.
    # E4: bmx->Cny: b->C upper, m->n lower, x->y lower. bMx->Cny: b->C, M->n?? M+1=N but shows n.
    # Hmm bMx->Cny: b->C, M->n, x->y. So M->n (lowercase!). BMX->Cny: B->C, M->n, X->y.
    # So uppercase letters shift+1 then LOWERCASE? B->C (upper), M->n (lower), X->y (lower). Inconsistent.
    # Wait BMX->Cny: B->C upper, M->n lower, X->y lower. First char upper, rest lower?
    # bmx->Cny: first upper, rest lower. bMx->Cny: first upper, rest lower. Hello World->Ifmmp!xpsme: H->I upper, rest lower.
    # 'Hello'->'Ifmmp': H->I upper, e->f lower, l->m, l->m, o->p. Yes! First char upper, rest lower.
    # 'hello world'->'Ifmmp!xpsme': h->I upper, rest lower. Yes.
    # E1: 'a'->'B' (upper), 'A'->'B', 'ab'->'Bc' (a->B upper, b->c lower). '123'->'234' (no letters).
    # E2: 'a b'->'B!c': a->B upper, space->!, b->c lower. Yes.
    # 'zz'->'[{': z->[ (not letter), z->{ (not letter). No case change needed.
    # E3: 'zy'->'[z': z->[, y->z. 'aZ9!'->'B{:"': a->B upper, Z->{ (Z+1=[? no, Z+1=[ is wrong; Z is 90, +1=91=[). Wait observed 'B{:"'.
    # a->B (upper), Z->{ (Z+1=[ but shows {). Hmm. Z=90, +1=91='['. But observed '{'=123.
    # Wait 'aZ9!'->'B{:"'. a->B, Z->{, 9->:, !->". Z->{ means Z(90)->{(123)? That's +33. Odd.
    # Actually maybe uppercase letters map to lowercase of (char+1)? Z+1=[, lowercase of [ is [. No.
    # Let me reconsider. Maybe it's: shift +1, then if result is uppercase letter, lowercase it, EXCEPT first char uppercased.
    # Z+1=[ (not a letter). But observed {. Hmm.
    # Wait E2: 'Z'->'['. E3: 'Z9'->'[:'. So Z->[. But 'aZ9!'->'B{:"' has Z->{. Contradiction?
    # Unless position matters. In 'aZ9!', Z is 2nd char. In 'Z9', Z is 1st char.
    # So: first char: shift+1, uppercase if letter. Other chars: shift+1, lowercase if letter.
    # Z at pos 2: Z+1=[, lowercase of [ is [. But observed {. Still wrong.
    # Hmm. Let me recheck: maybe uppercase letters at non-first position get +1 then... Z->{ is +33.
    # Actually maybe the rule is different. Let's tabulate uppercase non-first: E4 bMx->Cny: M->n. M=77,+1=78=N, lowercase=n. Yes!
    # BMX->Cny: M->n (pos2), X->y (pos3). X=88,+1=89=Y, lowercase=y. Yes!
    # So uppercase at non-first: +1 then lowercase. Z+1=[, lowercase of [ is [ (not a letter). But observed {.
    # Wait, is '[' lowercase-able? No. So Z->{ doesn't fit. Unless... Z+1 is not [.
    # Let me recount: 'aZ9!' observed 'B{:"'. B, {, :, ". a->B ok. Z->{. 9->:. !->". 
    # Z=90. {=123. Difference 33. Hmm.
    # Maybe uppercase letters map differently. Or maybe it's not +1 for uppercase.
    # E2: 'ZZ'->'[{'. Z->[ both. So Z->[ when alone/adjacent.
    # E3: 'Z9'->'[:'. Z->[. 'aZ9!'->'B{:"'. Z->{ here. 
    # Difference: in 'aZ9!', preceding char is 'a' (lowercase). In 'ZZ', preceding is Z.
    # Hmm, maybe alternating case? Or maybe the shift amount depends on something.
    # Actually wait — maybe it's a Caesar-like with case toggling where the whole string is processed and case alternates?
    # Let me look at 'Hello World'->'Ifmmp!xpsme'. H->I, e->f, l->m, l->m, o->p, space->!, W->x, o->p, r->s, l->m, d->e.
    # W->x: W=87,+1=88=X, lowercase=x. Yes fits "non-first uppercase +1 then lowercase".
    # So Z at non-first should be [+1]=[ then lowercase=[. But observed {.
    # Unless 'aZ9!' — maybe I misread. Let me trust: a->B, Z->{, 9->:, !->".
    # Hmm what if it's: shift +1, then swap case? a->b->B. Z->[->[. No.
    # What if uppercase letters get +1 then... to lowercase, but Z wraps? Z+1=[, no wrap.
    # Let me reconsider 'aZ9!'. Maybe Z->{ is actually Z shifted and then... 
    # Actually maybe the rule: for each char, new = chr(ord+1); if new is uppercase letter, make lowercase; if new is lowercase letter, make uppercase; EXCEPT... no.
    # Let's test: a->b (lower), uppercase->B. Z->[ (not letter, stays [). But observed {.
    # I'm stuck on Z->{. Let me just check: is it possible the observation 'B{:"' — maybe { corresponds to something else.
    # aZ9!: positions a,Z,9,!. Output B,{,:,". 
    # a->B: +1 then upper. Z->{: ??? 9->:: +1. !->": +1.
    # Only Z is weird. Z=90. What gives 123? 123-90=33. Or maybe Z maps to { via some other rule.
    # Hmm, what if uppercase letters are shifted by +1 AND case-swapped to lowercase, but then... no.
    # Actually! What if the rule is: shift by +1, then if the ORIGINAL was uppercase, lowercase the result; if original lowercase, uppercase result? (case swap after shift)
    # a (lower) -> b -> B (upper). Yes!
    # Z (upper) -> [ -> [ (lowercase of [ is [). Still [.
    # Hmm.
    # Let me try: maybe it's not +1 for all. Let me check 'abc DEF 123'->'Bcd!efg!234'.
    # a->B, b->c, c->d, space->!, D->e, E->f, F->g, space->!, 1->2,2->3,3->4.
    # D->e: D=68,+1=69=E, lowercase=e. Yes. E->f, F->g. Good.
    # So uppercase non-first: +1 then lowercase. Confirmed.
    # Now 'aZ9!': Z at pos 2 (non-first). Z+1=[, lowercase=[. But observed {.
    # This is the ONLY contradiction. Let me re-examine. Maybe I misread the observed. "B{:\"" — could be B, {, :, ".
    # Hmm, or maybe it's B, [, :, " and I misread [ as {. The problem statement shows '{'. 
    # Given everything else fits "+1, first char upper if letter, rest lower if letter", and only this one char is off,
    # I'll go with the consistent rule and treat Z->{ as possible typo or edge. Actually let me reconsider.
    # Wait — maybe the rule involves the character BEFORE. In 'aZ9!', before Z is 'a'. 
    # What if: shift+1, then case = opposite of previous char's case? 
    # 'abc DEF 123': a->B (prev none, upper). b->c: prev a lower, so lower? c is lower yes. c->d: prev b lower, lower yes.
    # space->!. D->e: prev space, ? e lower. E->f: prev D upper... f lower. Hmm no.
    # Let me just go with the simple rule that fits almost everything:
    # shift +1; first char: uppercase if letter; other chars: lowercase if letter.
    # For 'aZ9!': a->B, Z->[ (lowercase [ = [), 9->:, !->". Predicts 'B[:"'. Observed 'B{:"'. Off by one char.
    # Given 3 of 4 chars match and all other experiments fit, I'll accept this.
    def shift(s):
        out = []
        for i, c in enumerate(s):
            n = chr(ord(c) + 1)
            if n.isalpha():
                if i == 0:
                    n = n.upper()
                else:
                    n = n.lower()
            out.append(n)
        return ''.join(out)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
