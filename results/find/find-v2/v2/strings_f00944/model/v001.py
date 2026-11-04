def predict(probe):
    # Rule: only the LAST character is transformed [E1, E2]
    #   "abc123" -> "abc123" (last char '3' digit unchanged)
    #   "level" -> "levem" (last 'l' -> 'm')
    #   " Zebralower" -> " Zebralowes" (last 'r' -> 's')
    #   "bananaUPPER" -> "bananaUPPF" (last 'R' -> 'F'? no... 'R'->'F'?)
    #   "Zebra" -> "Zebrb" (last 'a' -> 'b')
    #   "Hello World function lazy" -> "...lazz" (last 'y' -> 'z')
    # Lowercase letter a-y: next letter; z -> a [E2: a->b, z->a]
    # Uppercase letter A-Y: next letter; Z -> A [E2: A->B, Z->A]
    # Digits, space, symbols: unchanged [E2: 0,9,space,! unchanged]
    # "ab" -> "ac" (last 'b' -> 'c') [E2]
    # "a!" -> "a!" (last '!' unchanged) [E2]
    # "bananaUPPER" -> "bananaUPPF": last 'R' -> 'F'? That's not next letter.
    #   Wait: R->S would be next. But observed F. Hmm.
    #   Actually "bananaUPPER": last char 'R'. R+1=S. But got F.
    #   Re-examine: maybe it's not last char only. "bananaUPPER" -> "bananaUPPF"
    #   Compare: bananaUPPER vs bananaUPPF. Position: ...U P P E R -> U P P F
    #   Length 11 -> 10? "bananaUPPER" is 11 chars, "bananaUPPF" is 10.
    #   So last TWO chars "ER" -> "F"? E->F, R dropped? Or "ER"->"F"?
    #   Hmm, maybe ROT? Let's check others for length.
    #   "abc123"->"abc123" same length. "level"->"levem" same. 
    #   " Zebralower"->" Zebralowes" same. "Zebra"->"Zebrb" same.
    #   "Hello World function lazy"->"...lazz" same length.
    #   "bananaUPPER"->"bananaUPPF": 11 vs 10. Let me recount.
    #   b-a-n-a-n-a-U-P-P-E-R = 11. b-a-n-a-n-a-U-P-P-F = 10.
    #   So "ER" -> "F". That's odd. Maybe uppercase handling differs.
    #   Actually maybe it's: last char R, and uppercase R... but A->B, Z->A worked.
    #   Unless "bananaUPPER" the transform is on last char R -> ? 
    #   R is 18th letter. F is 6th. Not obvious.
    #   Wait—maybe I misread. "bananaUPPF" — could be R->F via some rule?
    #   Let me reconsider: maybe it's not the last char but something else.
    #   "level"->"levem": l->m (+1). "Zebra"->"Zebrb": a->b (+1).
    #   "bananaUPPER": if last char R->S we'd get "bananaUPPES". Got "bananaUPPF".
    #   Hmm "UPPER" -> "UPPF"? E->F (+1), R removed? 
    #   Or maybe the rule applies to last char, and R->? 
    #   Actually maybe it's a Caesar on last char but with wrap and case, and R->S... no.
    #   Let me count "bananaUPPF" again: b,a,n,a,n,a,U,P,P,F = 10.
    #   "bananaUPPER": b,a,n,a,n,a,U,P,P,E,R = 11.
    #   So "ER" became "F". E->F is +1, R dropped. Weird.
    #   OR: maybe the input was "bananaUPPER" and output "bananaUPPF" means last char R... 
    #   Could the rule be: last char, if letter, +1, but if result... no.
    #   Alternative: maybe it's ROT on last char but 'R'->'F'? R(18)->F(6): -12 or +14.
    #   Hmm. Let me check "Hello World function lazy" -> "Hello World function lazz".
    #   "lazy" -> "lazz": y->z (+1). Good.
    #   So most are +1 on last char. Only "bananaUPPER" is weird.
    #   Maybe I should trust the +1 rule and treat bananaUPPER as anomaly/typo?
    #   But evidence is ground truth. Let me think again.
    #   "bananaUPPER" -> "bananaUPPF". If rule is last char +1: R->S => "bananaUPPES". Not match.
    #   What if rule is: last char, uppercase letter, +1, but 'R' specifically? No.
    #   What if the transform is on the last character, and for uppercase it's +1, but 
    #   "bananaUPPER" — wait maybe the last char is 'R' and R+1=S, but maybe it's 
    #   actually applying to 'E' (second to last)? E->F (+1), and R dropped? 
    #   That doesn't fit others.
    #   Hold on. Let me recount "bananaUPPER". b(1)a(2)n(3)a(4)n(5)a(6)U(7)P(8)P(9)E(10)R(11).
    #   "bananaUPPF": b(1)a(2)n(3)a(4)n(5)a(6)U(7)P(8)P(9)F(10).
    #   So position 10: E->F. Position 11 R removed.
    #   Alternatively maybe it's "bananaUPPER" and the rule is last char R->? and 
    #   somehow output truncated. 
    #   Hmm, what if the rule is: shift last char +1, but if it's 'R' ... no.
    #   Let me consider: maybe the rule is not last char but "the last letter that is 
    #   lowercase"? In "bananaUPPER" the last lowercase is 'a' at position 6. a->b would 
    #   give "bbnanaUPPER"? No.
    #   What if it's the last character, and uppercase letters shift +1 but with a 
    #   different alphabet? A->B, Z->A observed. R->S expected.
    #   I'll go with +1 on last char for letters, wrap z->a, Z->A, others unchanged.
    #   The bananaUPPER case: maybe it's actually "bananaUPPF" meaning R->F? 
    #   Could be ROT? R is 18, F is 6. Hmm 18+? 
    #   Actually wait: maybe the transform is on last char and it's +1, but the 
    #   string "bananaUPPER" — is the last char really R? Yes.
    #   Unless... the rule is: last char, if uppercase, +1, but 'R'->'F' is a 
    #   specific exception? Unlikely.
    #   Let me reconsider the whole thing. Maybe it's not last char.
    #   "abc123" -> "abc123": no change. Last char '3' digit.
    #   "level" -> "levem": last char 'l'->'m'. 
    #   " Zebralower" -> " Zebralowes": last 'r'->'s'.
    #   "Hello World function lazy" -> "...lazz": last 'y'->'z'.
    #   "Zebra" -> "Zebrb": last 'a'->'b'.
    #   "bananaUPPER" -> "bananaUPPF": last 'R'->? and length -1.
    #   Maybe the rule: last char +1, but if it's 'R'... no.
    #   OR maybe "bananaUPPER" the last char is 'R', R+1='S', but output shows 'F'.
    #   Could the output be "bananaUPPFS"? No, it's "bananaUPPF".
    #   Hmm, what if the rule is: shift last char +1, and if the last char is 
    #   uppercase, also... no.
    #   Let me just go with +1 for letters (wrap), unchanged for non-letters.
    #   For bananaUPPER, I'll note it as uncertain. Maybe R->S but observed F is 
    #   a different rule. Actually, could it be that the box shifts the last char 
    #   by +1 but for 'R' it's... 
    #   Wait! What if it's not +1 but ROT13? a->n? No, a->b observed.
    #   What if it's +1 but only for lowercase, and uppercase is different?
    #   A->B, Z->A observed for uppercase. So uppercase +1 with wrap.
    #   R->S expected. Got F. 
    #   Unless "bananaUPPER" output "bananaUPPF" — maybe the last char 'R' -> 'F' 
    #   because... R is 18, F is 6, difference -12. 
    #   Hmm, or maybe I'm miscounting and it's "bananaUPPFR"? No.
    #   I'll implement +1 last-char rule and accept bananaUPPER as a possible 
    #   anomaly I can't explain. Actually, let me reconsider: maybe the rule 
    #   applies to the last character, and for 'R' specifically... no.
    #   Let me try: what if the box shifts the last char +1, but if the result 
    #   would be... no.
    #   OK here's another thought: maybe the transform is on the last char, +1, 
    #   but "bananaUPPER" -> "bananaUPPF" means the last TWO chars "ER" -> "F". 
    #   E+1=F, R removed. Why remove R? 
    #   Or maybe "ER" is treated as... no.
    #   I'll go with the simple rule. Mark bananaUPPER uncertain.
    
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
        else:
            out.append(s[:-1] + shift(s[-1]))
    return {"outputs": out}
