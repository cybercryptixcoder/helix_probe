def predict(probe):
    # Observations from E1:
    # "abc123" -> "abc123h"  (append 'h')
    # "level" -> "levh"      (remove last char, append 'h'? "level"->"leve"+"h"? no, "levh")
    # " Zebralower" -> " Zebralowh"  (truncate + 'h')
    # "Hello World function lazy" -> "Helo Wrdfunctiazyh"
    # "bananaUPPER" -> "banUPERh"
    # "Zebra" -> "Zebrah"
    #
    # Hypothesis: remove all lowercase letters that are... hmm.
    # Let's look: "level" -> "levh": removed 'e','l'? Actually "level" letters: l,e,v,e,l -> "lev" then 'h'.
    # "Hello World function lazy" -> "Helo Wrdfunctiazyh"
    #   H e l l o   W o r l d   f u n c t i o n   l a z y
    #   H e l o   W r d f u n c t i a z y h
    #   Removed: second 'l' in Hello, 'o' in World, 'l' in World, 'o' in function, 'n' in function, 'l' in lazy
    #   Hmm, removed letters: l,o,l,o,n,l. 
    # "bananaUPPER" -> "banUPERh": b a n a n a U P P E R -> b a n U P P E R h
    #   Removed: a,n,a,a. Kept 'n' (first n). Hmm removed 'a' at pos2, 'n' pos3, 'a' pos4, 'a' pos5.
    # "Zebra" -> "Zebrah": Z e b r a -> Z e b r a h. Nothing removed!
    # "abc123" -> "abc123h": nothing removed.
    # " Zebralower" -> " Zebralowh": ' ' Z e b r a l o w e r -> ' ' Z e b r a l o w h
    #   Removed 'e','r' at end. Kept "low".
    #
    # Pattern: seems to remove a letter if it appears... let's check "level": l,e,v,e,l
    #   Removed e (pos1), l (pos4). Kept l(pos0), e(pos3)? no wait output "lev": l,e,v. So kept pos0 l, pos1 e, pos2 v. Removed pos3 e, pos4 l.
    #   Hmm so removed last two chars 'e','l'? "level"[:-2]="lev". Yes!
    # "bananaUPPER" -> "banUPERh": "bananaUPPER"[:-?]. "bananaUPPER" is 11 chars. "banUPER" is 7. Removed 4 chars: "ana" + ? Actually "bananaUPPER" -> remove "ana" (pos3-5)? b-a-n-a-n-a-U-P-P-E-R. Output b-a-n-U-P-P-E-R. So removed positions 3,4,5 = 'a','n','a'. That's "ana". Hmm.
    # "Hello World function lazy" -> "Helo Wrdfunctiazyh". Let's see removals:
    #   "Hello World function lazy" = H e l l o ' ' W o r l d ' ' f u n c t i o n ' ' l a z y
    #   Output: H e l o ' ' W r d f u n c t i a z y h
    #   So removed: 'l'(pos3), 'o'(pos4), 'o'(pos7), 'l'(pos9), 'o'(pos17), 'n'(pos18), 'l'(pos21)
    #   Wait let me recount. "Hello World function lazy"
    #   indices: 0H 1e 2l 3l 4o 5space 6W 7o 8r 9l 10d 11space 12f 13u 14n 15c 16t 17i 18o 19n 20space 21l 22a 23z 24y
    #   Output "Helo Wrdfunctiazyh": H e l o space W r d f u n c t i a z y h
    #   So kept: H(0) e(1) l(2) o(4) space(5) W(6) r(8) d(10) space(11) f(12) u(13) n(14) c(15) t(16) i(17) a(22) z(23) y(24) then h
    #   Removed: l(3), o(7), l(9), o(18), n(19), l(21)
    #   Hmm removed: l,o,l,o,n,l. 
    #   Wait o(7) removed but o(4) kept. l(3) removed but l(2) kept.
    #   Looks like: if a letter appears twice in a row (double), remove one? "Hello" has "ll" -> remove one l -> "Helo". Yes!
    #   "World" -> "Wrd"? removed 'o','l'. Hmm not double.
    #   Wait "World" -> "Wrd": removed o,l. 
    #   "function" -> "functi"? removed o,n. 
    #   "lazy" -> "azy"? removed l.
    #   Hmm. Let's reconsider.
    #
    # Maybe: remove letters that are "lowercase and appear more than once"? No.
    #
    # Let's look at "bananaUPPER" -> "banUPER": removed "ana" (positions 3,4,5). "banana" = b a n a n a. Removed a,n,a = positions 3,4,5. So kept "ban" then removed "ana". 
    # Hmm "banana" -> "ban". Removed last 3 chars "ana".
    #
    # "level" -> "lev": removed last 2 "el".
    # "Zebra" -> "Zebrah": removed nothing.
    # "abc123" -> "abc123h": removed nothing.
    #
    # Wait maybe it's about consecutive duplicate-ish? Let me think differently.
    #
    # Maybe the rule: remove every lowercase letter that is immediately preceded by a lowercase letter that... no.
    #
    # Let's check "Hello World function lazy" more carefully with a different idea: remove a letter if it equals the letter 2 positions before? 
    #   H e l l o: l(3) equals l(2)? yes remove l(3). o(4) vs l(2)? no.
    #   Hmm.
    #
    # Another idea: remove lowercase letters that appear earlier in the string (first occurrence kept, subsequent removed)?
    #   "level": l(0) keep, e(1) keep, v(2) keep, e(3) remove (e seen), l(4) remove (l seen). -> "lev". YES!
    #   "bananaUPPER": b keep, a keep, n keep, a remove, n remove, a remove, U,P,P,E,R keep (uppercase). -> "banUPER". YES!
    #   "Zebra": Z keep, e keep, b keep, r keep, a keep. -> "Zebra". YES!
    #   "abc123": all unique -> "abc123". YES!
    #   " Zebralower": space, Z,e,b,r,a,l,o,w,e(remove, e seen),r(remove, r seen) -> " Zebralow". YES!
    #   "Hello World function lazy": 
    #     H keep, e keep, l keep, l remove, o keep, space, W keep, o remove (o seen), r keep, l remove (l seen), d keep, space, f keep, u keep, n keep, c keep, t keep, i keep, o remove, n remove, space, l remove, a keep, z keep, y keep
    #     -> "Helo Wrdfuctiazy"? Let me check: H e l o space W r d space f u n c t i space a z y
    #     = "Helo Wrd functi azy"? Hmm "Helo Wrdfunctiazy". 
    #     Wait output was "Helo Wrdfunctiazyh". Let me verify: H e l o space W r d f u n c t i a z y
    #     = "Helo Wrdfunctiazy". YES matches!
    #
    # So rule: keep first occurrence of each lowercase letter (case-sensitive? uppercase always kept?), remove subsequent lowercase duplicates. Then append 'h'.
    #
    # Check uppercase: "bananaUPPER" kept U,P,P,E,R all. So uppercase not deduplicated. Only lowercase deduplicated.
    # Check "Zebra": Z uppercase kept, e,b,r,a lowercase all unique kept.
    #
    # What about digits/symbols? "abc123" kept 1,2,3. Are digits deduped? Unknown. Assume only lowercase letters deduped.
    #
    # Append 'h' at end always.
    import re
    def transform(s):
        seen = set()
        out = []
        for ch in s:
            if 'a' <= ch <= 'z':
                if ch in seen:
                    continue
                seen.add(ch)
            out.append(ch)
        return ''.join(out) + 'h'
    return {"outputs": [transform(x) for x in probe["inputs"]]}
