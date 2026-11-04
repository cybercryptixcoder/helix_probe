def predict(probe):
    # Observations from E1:
    # "hello" -> "he2llq": insert '2' after 2 chars, last char shifted +1 (o->q? no, o->q is +2)
    # Let's analyze carefully:
    # hello -> he2llq : h,e,2,l,l,q  (o->q is +2)
    # Hello -> He2llq : H,e,2,l,l,q
    # two words -> two 2wordu : t,w,o,space,2,w,o,r,d,u  (s->u is +2)
    # abc123 -> abc2123 : a,b,c,2,1,2,3  (insert 2 after 3 chars)
    # a b c -> a 2b e : a,space,2,b,space,e  (c->e is +2)
    # test -> te2sv : t,e,2,s,v  (t->v is +2)
    # WORLD -> WO2RLF : W,O,2,R,L,F  (D->F is +2)
    # x -> 2z : 2,z  (x->z is +2)
    # hello world -> hello2 worlf : hello,2,space,w,o,r,l,f  (d->f is +2)
    # A1! -> A21! : A,2,1,!  (insert 2 after 1 char)
    #
    # Pattern: insert '2' at position len//2 (floor), and shift last char +2.
    # Check: hello len5, 5//2=2 -> insert at 2: he|2|llo -> he2llo, last o+2=q -> he2llq ✓
    # Hello len5 -> He2llo -> He2llq ✓
    # two words len9, 9//2=4 -> two |2|words -> two 2words, last s+2=u -> two 2wordu ✓
    # abc123 len6, 6//2=3 -> abc|2|123 -> abc2123, last 3+2=5? but output is abc2123, last is 3.
    #   Wait abc2123: a,b,c,2,1,2,3. Last char is 3, unchanged? 3+2=5 not 3.
    #   Hmm. Maybe last char shifted only if letter? digit 3->5 would be abc2125. But it's abc2123.
    #   So digit last char not shifted? Let's check A1!: A,2,1,! last is ! unchanged.
    #   a b c len5, 5//2=2 -> a |2|b c -> a 2b c, last c+2=e -> a 2b e ✓
    #   test len4, 4//2=2 -> te|2|st -> te2st, last t+2=v -> te2sv ✓
    #   WORLD len5 -> WO2RLD, last D+2=F -> WO2RLF ✓
    #   x len1, 1//2=0 -> 2|x -> 2x, last x+2=z -> 2z ✓
    #   hello world len11, 11//2=5 -> hello|2| world -> hello2 world, last d+2=f -> hello2 worlf ✓
    #   A1! len3, 3//2=1 -> A|2|1! -> A21!, last ! not letter -> unchanged ✓
    #   abc123: last char '3' is digit, not shifted. So only letters shift +2.
    #   Check: does digit shift? abc123 last 3 stays 3. Yes only letters.
    #   What about '!' stays. So: shift last char +2 only if it's a letter.
    #   Also check: does the shift wrap? z+2 -> b? unknown, assume wrap within case.
    #   Case preserved: lowercase stays lowercase, uppercase stays uppercase.
    #   'o'->'q', 's'->'u', 't'->'v', 'd'->'f', 'x'->'z', 'D'->'F'. All +2 same case.
    #   Wrap: 'y'+2='a', 'z'+2='b'? assume wrap.
    # Insert position: len//2 (floor). For len1 -> 0 (before). For len0 -> 0.
    # Edge: empty string -> "2"? len0//2=0 insert at 0 -> "2", no last char. Guess "2".
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+2)%26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+2)%26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        n = len(s)
        p = n // 2
        t = s[:p] + "2" + s[p:]
        if n > 0:
            t = t[:-1] + shift(t[-1])
        out.append(t)
    return {"outputs": out}
