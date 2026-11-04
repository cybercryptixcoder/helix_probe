def predict(probe):
    # Observations [E1]:
    # - "abc123" -> "abc123h"        (append 'h')
    # - "level" -> "levh"            (remove consecutive duplicate chars, then append 'h')
    # - " Zebralower" -> " Zebralowh" (remove consecutive duplicate chars, append 'h')
    # - "Hello World function lazy" -> "Helo Wrdfunctiazyh"
    #     (remove consecutive duplicates: "Hello"->"Helo", "World"->"World",
    #      "function"->"functin"? actually "function" has no consecutive dup,
    #      but output shows "functi" + "azy"... let's re-derive)
    # - "bananaUPPER" -> "banUPERh"  (remove consecutive duplicates, append 'h')
    # - "Zebra" -> "Zebrah"          (append 'h')
    #
    # Re-check "Hello World function lazy" -> "Helo Wrdfunctiazyh":
    #   "Hello" -> "Helo" (drop one 'l')
    #   "World" -> "World" (no dup)
    #   "function" -> "functin"? observed "functi" ... hmm
    #   observed: "Helo Wrdfunctiazyh"
    #   Let's split: "Helo Wr" + "dfuncti" + "azy" + "h"
    #   Original: "Hello World function lazy"
    #   Removing consecutive duplicates gives:
    #     "Helo World function lazy"
    #   That's not it. Observed has "Wr" then "dfuncti" - 'o','l','d' missing?
    #   Actually "World" -> "Wr" suggests removing 'o','l','d'? No...
    #   Wait: "World function" -> "Wrdfuncti"? Let's see: W-o-r-l-d-space-f-u-n-c-t-i-o-n
    #   Removing consecutive duplicates: W o r l d space f u n c t i o n -> same
    #   Observed "Wrdfuncti": W r d f u n c t i
    #   Hmm, that drops 'o','l' from World, and 'o','n' from function?
    #   Maybe it removes vowels? "Hello"->"Hllo"? No, "Helo" keeps 'e'.
    #   Let's try: remove consecutive duplicates AND something else.
    #   "Hello World function lazy"
    #   Remove consecutive dups: "Helo World function lazy"
    #   Now remove... 'o' after W? "Wrld function lazy" -> no.
    #   Observed: "Helo Wrdfunctiazyh"
    #   Compare "Helo World function lazy" vs "Helo Wrdfunctiazyh"
    #   "Helo W" matches. Then "orld function lazy" vs "rdfunctiazy"
    #   "orld" -> "rd" (drop 'o','l')
    #   " function lazy" -> "functiazy" (drop 'n','o','n',' ','l')
    #   Hmm inconsistent.
    #
    #   Alternative: maybe it's removing every other character in some pattern?
    #   Let me try: remove consecutive duplicates, then remove all 'o' and 'l' and 'n'?
    #   "Helo World function lazy" remove o,l,n:
    #     "He Wrd fucti azy" - no.
    #
    #   Let me try: the box removes consecutive duplicate letters, then removes
    #   letters that appear more than once in the string? 
    #   "Hello World function lazy":
    #     counts: H1 e1 l3 o3 space2 W1 r1 d1 f1 u1 n2 c1 t1 i1 a1 z1 y1
    #     remove letters with count>1 (l,o,space,n):
    #     "HeWrdfuctiazy" - close but observed "Helo Wrdfunctiazyh"
    #     Not quite.
    #
    #   Let me reconsider. Maybe it's a "remove consecutive duplicates" applied
    #   but the observed is "Helo Wrdfunctiazyh". 
    #   "Hello World function lazy"
    #   positions: H e l l o _ W o r l d _ f u n c t i o n _ l a z y
    #   Remove consecutive dups: H e l o _ W o r l d _ f u n c t i o n _ l a z y
    #   = "Helo World function lazy"
    #   Observed: "Helo Wrdfunctiazyh"
    #   Difference: "World function lazy" -> "Wrdfunctiazy"
    #   "World" -> "Wrd" (drop o,l)
    #   " function" -> "functi" (drop space, n, o, n)
    #   " lazy" -> "azy" (drop space, l)
    #   So dropped: o,l (from World), space,n,o,n (from function), space,l (from lazy)
    #   Hmm, dropped letters: o,l,space,n,o,n,space,l
    #   These are: o,l,n,space... and o,n,space,l
    #   Maybe drop letters that appeared before? Like dedupe globally?
    #   "Helo World function lazy" - global first occurrence:
    #     H e l o _ W r d f u n c t i a z y
    #   = "HeloWrdfunctiazy" - but observed has spaces: "Helo Wrdfunctiazyh"
    #   Close! Observed: "Helo Wrdfunctiazyh" - has space after Helo, and trailing h.
    #   Hmm but global dedupe would remove the space after Helo too (space appeared once before? no, first space is after Helo).
    #   Wait "Helo World..." first space is after Helo. Global dedupe keeps first space.
    #   Then "World" -> W (new), o (seen), r (new), l (seen), d (new) -> "Wrd"
    #   space (seen) -> drop
    #   "function" -> f,u,n,c,t,i,o(seen),n(seen) -> "functi"
    #   space (seen) -> drop
    #   "lazy" -> l(seen),a,z,y -> "azy"
    #   Result: "Helo" + " " + "Wrd" + "functi" + "azy" = "Helo Wrdfunctiazy"
    #   Observed: "Helo Wrdfunctiazyh" - matches except trailing 'h'!
    #
    #   So the rule might be: remove consecutive duplicates, then remove any
    #   character that has already appeared earlier (keep first occurrence),
    #   then append 'h'.
    #   Check "level": consecutive dups -> "level" (no consecutive dups).
    #     Global dedupe: l,e,v,l(seen),e(seen) -> "lev". Append h -> "levh". ✓
    #   Check "abc123": no dups, no repeats -> "abc123h". ✓
    #   Check " Zebralower": consecutive dups none. Global dedupe:
    #     space,Z,e,b,r,a,l,o,w,e(seen),r(seen) -> " Zebralow". Append h -> " Zebralowh". ✓
    #   Check "bananaUPPER": consecutive dups none. Global dedupe:
    #     b,a,n,a(seen),n(seen),a(seen),U,P,P(seen),E,R -> "banUPER". Append h -> "banUPERh". ✓
    #   Check "Zebra": no dups -> "Zebrah". ✓
    #
    #   But wait, does the consecutive-duplicate removal matter separately?
    #   Global dedupe already removes all repeats including consecutive ones.
    #   "Hello" global dedupe: H,e,l,l(seen),o -> "Helo". ✓ (same as consecutive removal)
    #   So maybe just: global dedupe (keep first occurrence) then append 'h'.
    #   Check "Hello World function lazy" with pure global dedupe:
    #     H,e,l,o,space,W,r,d,f,u,n,c,t,i,a,z,y -> "Helo Wrdfunctiazy" + h ✓
    #   Yes! Pure global dedupe works.
    #
    #   So: f(s) = (keep first occurrence of each character in s) + "h"
    def predict(probe):
        out = []
        for s in probe["inputs"]:
            seen = set()
            res = []
            for ch in s:
                if ch not in seen:
                    seen.add(ch)
                    res.append(ch)
            out.append("".join(res) + "h")
        return {"outputs": out}
    return predict(probe)
