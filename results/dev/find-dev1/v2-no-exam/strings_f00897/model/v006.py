def predict(probe):
    # Mechanism: each character's code point is shifted by +2 or +4.
    # Which shift applies depends on the character's code point, NOT its position.
    #
    # Evidence for a code-point-based rule (not position-based):
    #  - 'a'->'c' (+2) [E1], 'b'->'f' (+4) in "ab"->"cf" [E1]
    #    So 'a' gets +2 and 'b' gets +4 regardless of position.
    #  - "aa"->"ce": first a +2, second a +4 [E6] — but E6 shows a->c on first
    #    position; the second a->e is +4. Hmm, that suggests position matters...
    #    BUT E7: "oa"->"qe": o->q (+2), a->e (+4). And "pa"->"re": p->r(+2), a->e(+4).
    #    So 'o','p','q','r','s','t','u','v' all get +2 at position 0.
    #  - E7 "Oa"->"Qe": O->Q (+2). "Za"->"^e": Z->^ (+4).
    #
    # Reconcile: the +2 set at position 0 is a-n, o-v, A-N, O-V, @? Let's check.
    # E7 shows o-v get +2 at position 0. E4 showed w,x get +4 at position 0.
    # E2 showed z,y get +4. E3 showed n,m,l get +2, N,M,L get +2.
    # E1 showed a,A get +2; b in "ab" (position 1) got +4.
    # E6 showed a-j at position 0 all get +2.
    #
    # So at position 0: a-v, A-V get +2; w-z, W-Z get +4.
    # At position >0: everything gets +4 (a->e in "aa", b->f in "ab", etc.)
    #
    # Wait — is it really position-based, or is it "first char of string"?
    # All evidence is consistent with: index 0 uses the +2 set {a-v, A-V, @?},
    # index >=1 always +4.
    #
    # Check @: E3 "@"->"B" (+2), E5 "@a"->"Be" (@->B +2). So @ is in the +2 set.
    # Check digits: 0->4(+4), 9->=(+4), 1->5(+4). Not in +2 set.
    # Check space, !: +4. {, ~, \x80: +4.
    #
    # So +2 set at position 0: '@', 'A'-'V', 'a'-'v'.
    # Let me verify boundaries: E7 gives o-v (+2) and Z (+4). E4 gives w,x,W,X,Y (+4).
    # So lowercase cutoff is v (v->x +2, w->{ +4). Uppercase cutoff is V (V->X +2, W->[ +4).
    # E7 "Oa"->"Qe" confirms O->Q (+2). Good.
    #
    # What about chars between 'V' and 'a' (W-Z, [, \, ], ^, _, `)? E4 W,X,Y +4; E7 Z +4.
    # So those are +4. What about '[' '\\' ']' '^' '_' '`'? Unknown, assume +4 (not in set).
    #
    # What about '@'? It's +2. What about chars just below '@' ('?','>','=','<',';',':','9'...)?
    # 9->=(+4) [E3]. So digits are +4. Assume only '@' is +2 in that region.
    #
    # Final rule:
    #   if index == 0 and c in "@" or "A"<=c<="V" or "a"<=c<="v": shift +2
    #   else: shift +4

    def shift_char(c, is_first):
        o = ord(c)
        if is_first and (c == '@' or ('A' <= c <= 'V') or ('a' <= c <= 'v')):
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
