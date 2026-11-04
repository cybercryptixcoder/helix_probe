def predict(probe):
    # Only the LAST character is transformed [E1,E2,E3,E4]
    #   "abc123"->"abc123", "level"->"levem", "Zebra"->"Zebrb" [E1]
    #   "a"->"b", "z"->"a", "A"->"B", "Z"->"A" [E2]
    #   digits, space, symbols unchanged: "0","9"," ","!" [E2]
    #   "ab"->"ac", "a!"->"a!" [E2]
    #   "test case"->"test casf", "lazy"->"lazz", "banana"->"bananb" [E3]
    #   "abc"->"abd", "ABC"->"ABD", "aBc"->"aBd", "ZebraX"->"ZebraY" [E4]
    #   "hello!"->"hello!", "hello?"->"hello?" (last char symbol) [E4]
    #   "xyz"->"xya", "XYZ"->"XYA" (wrap) [E4]
    #   "a1b2c3"->"a1b2c3" (last char digit) [E4]
    # Lowercase a-y -> next; z -> a [E2,E4]
    # Uppercase A-Y -> next; Z -> A [E2,E4]
    # Non-letters unchanged [E2,E4]
    # "midUPPERend"->"midUPPEene": last char 'd'->'e' (+1). The 'R' in middle
    #   is NOT shifted, but the output shows "midUPPEene" vs input "midUPPERend":
    #   m-i-d-U-P-P-E-R-e-n-d -> m-i-d-U-P-P-E-e-n-e
    #   Wait: input "midUPPERend" = m,i,d,U,P,P,E,R,e,n,d (11)
    #   output "midUPPEene" = m,i,d,U,P,P,E,e,n,e (10)
    #   So 'R' at position 8 removed, and last 'd'->'e'. Hmm.
    #   Compare with "bananaUPPER"->"bananaUPPF": 'R' removed, 'E'->'F'.
    #   Pattern: when string ends with uppercase letters, the last uppercase
    #   letter 'R' is dropped and the preceding letter is shifted? 
    #   "bananaUPPER": ...U P P E R -> ...U P P F  (E->F, R dropped)
    #   "midUPPERend": ...U P P E R e n d -> ...U P P E e n e
    #     Here R dropped, and 'd'->'e' (last char shifted). E stays E.
    #   Hmm inconsistent. Let me look again.
    #   "midUPPERend" -> "midUPPEene": 
    #     m i d U P P E R e n d
    #     m i d U P P E e n e
    #   Positions: 1-7 same (m,i,d,U,P,P,E). Then R removed. Then e,n,d -> e,n,e.
    #   So 'd'->'e' (last char +1), and 'R' removed.
    #   "bananaUPPER" -> "bananaUPPF":
    #     b a n a n a U P P E R
    #     b a n a n a U P P F
    #   Positions 1-9 same. Then E->F, R removed.
    #   So here E->F (the char before R shifted), R removed.
    #   In midUPPERend, char before R is E, but E stayed E, and last char d->e.
    #   Difference: in bananaUPPER, R is the LAST char. In midUPPERend, R is not last.
    #   So rule: if last char is 'R'? No...
    #   Let's think: maybe rule is: shift last char +1. If last char is uppercase
    #   letter, and it's 'R'... no.
    #   Alternative: the box removes any 'R' that is immediately preceded by 'E'
    #   and followed by end-or-lowercase? "ER" -> ""? 
    #   bananaUPPER: "ER" at end -> removed, leaving "bananaUPP", then last char P->? 
    #     No, output is "bananaUPPF" which has F.
    #   Hmm. Let me reconsider: maybe "ER" -> "F". E+1=F, R dropped.
    #   midUPPERend: "ER" -> "E"? then "end"->"ene"? 
    #     "midUPP" + "ER" + "end" -> "midUPP" + "E" + "ene" = "midUPPEene". Yes!
    #   So "ER" -> "E" when followed by more text? And "ER" at end -> "F"?
    #   Wait bananaUPPER: "bananaUPP" + "ER" -> "bananaUPP" + "F" = "bananaUPPF". Yes.
    #   So "ER" at end -> "F" (E->F, R dropped). "ER" mid -> "E" (R dropped, E kept)?
    #   But then last char of whole string still gets +1: "end"->"ene" (d->e).
    #   Hmm, but in midUPPERend the "ER" is mid, R dropped, E kept, then "end"->"ene".
    #   Actually simpler: maybe the rule is just "remove 'R' when preceded by 'E'"
    #   AND "shift last char +1". Let's test:
    #   bananaUPPER: remove R -> "bananaUPPE", then shift last char E->F -> "bananaUPPF". Yes!
    #   midUPPERend: remove R -> "midUPPEend", then shift last char d->e -> "midUPPEene". Yes!
    #   Check others: "level" no ER, shift l->m = "levem". Yes.
    #   "Zebra" no ER, shift a->b = "Zebrb". Yes.
    #   "abc123" shift 3->3 (digit) = same. Yes.
    #   "ZebraX" shift X->Y = "ZebraY". Yes.
    #   "hello!" shift !->! = same. Yes.
    #   "xyz" shift z->a = "xya". Yes.
    #   "XYZ" shift Z->A = "XYA". Yes.
    #   "a1b2c3" shift 3->3 = same. Yes.
    #   "test case" shift e->f = "test casf". Yes.
    #   "banana data banana " shift space->space = same. Yes.
    #   "lazy" shift y->z = "lazz". Yes.
    #   "banana" shift a->b = "bananb". Yes.
    #   "a"->"b", "z"->"a", "A"->"B", "Z"->"A". Yes.
    #   "ab"->"ac", "a!"->"a!". Yes.
    #   "Example123" shift 3->3 = same. Yes.
    # So rule: remove all occurrences of "ER"? Or just "R" preceded by "E"?
    #   Only evidence is "ER". Could be "remove R when preceded by E".
    #   Or could be "remove R" generally? No other R evidence without E.
    #   "Zebra" has 'r' lowercase, not removed. So uppercase R specifically?
    #   "ZebraX" has no R. 
    #   Let's go with: remove uppercase 'R' when immediately preceded by uppercase 'E'.
    #   Actually could be "ER" -> "" (both removed)? 
    #     bananaUPPER: remove ER -> "bananaUPP", shift P->Q = "bananaUPPQ". Not F. No.
    #   So only R removed, E kept. Then shift last char.
    #   But wait: in bananaUPPER, after removing R we get "bananaUPPE", last char E->F. 
    #   That matches. Good.
    #   What about "ER" where E is not uppercase? "Zebra" has 'e' then 'b', no.
    #   I'll assume uppercase "ER" -> "E" (drop R). Mark uncertain.
    # Also need to check: does removal happen before or after shift? 
    #   If shift first: bananaUPPER -> shift R->S = "bananaUPPES", then remove ER? 
    #   "ES" no. So removal first.
    #   Actually maybe rule is: drop 'R' if preceded by 'E' (case-insensitive?).
    #   "Zebra" has 'e','b' no. "level" no. 
    #   I'll do uppercase ER only, since evidence is uppercase.
    #   Hmm but "Zebralower" has 'r' at end, lowercase, not dropped. Good.
    #   "Hello World function lazy" no ER.
    #   Let me also consider: maybe it's "remove R when preceded by E" regardless of case.
    #   No evidence for lowercase er. Keep uppercase only? Or both?
    #   "Zebralower" has "er"? Z-e-b-r-a-l-o-w-e-r. No "er". 
    #   "level" no. "test case" no. "banana data banana" no.
    #   I'll do uppercase ER only, mark uncertain.
    
    def shift(c):
        if 'a' <= c <= 'z':
            return 'a' if c == 'z' else chr(ord(c)+1)
        if 'A' <= c <= 'Z':
            return 'A' if c == 'Z' else chr(ord(c)+1)
        return c
    
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append(s)
            continue
        # Remove uppercase 'R' preceded by uppercase 'E' [E1,E4]
        t = s.replace("ER", "E")
        if not t:
            out.append(t)
            continue
        out.append(t[:-1] + shift(t[-1]))
    return {"outputs": out}
