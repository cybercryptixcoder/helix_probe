import re

def predict(probe):
    # Observations from E1:
    # - "abc123" -> "abc123h": appended 'h'
    # - "level" -> "levh": 'el' removed? Actually "level" -> "lev" + "h". Looks like remove 'e'? No: l-e-v-e-l -> l-e-v (drop "el"?) 
    #   Wait: "level" -> "levh". That's "level" with last two chars "el" removed, then 'h' appended.
    # - " Zebralower" -> " Zebralowh": "Zebralower" -> "Zebralow" + "h": drop "er", append 'h'.
    # - "Hello World function lazy" -> "Helo Wrdfunctiazyh": many letters removed, 'h' appended.
    # - "bananaUPPER" -> "banUPERh": "banana" -> "ban", then "UPPER" kept, append 'h'.
    # - "Zebra" -> "Zebrah": append 'h'.
    #
    # Hypothesis: remove all occurrences of letters in some set, then append 'h'.
    # Let's check which letters are removed:
    # "abc123" -> "abc123": nothing removed (no a,b,c removed). So a,b,c kept.
    # "level" -> "lev": removed 'e','l'? But 'l' appears in "level" twice; result "lev" has one 'l'. So removed one 'e' and one 'l'? 
    #   Actually "level" = l e v e l. Result "lev" = l e v. Removed positions: second 'e' and last 'l'? Or removed all 'e' and last 'l'?
    #   If remove all 'e': "lvl" -> not "lev". So not all 'e'.
    #   Maybe remove letters that appear more than once? "level": l(2), e(2), v(1). Remove duplicates beyond first? 
    #   l e v e l -> keep first occurrences: l e v -> "lev". Yes! That matches.
    # " Zebralower": Z e b r a l o w e r. Duplicates: e(2), r(2). Keep first occurrences: Z e b r a l o w r? 
    #   Wait order: Z,e,b,r,a,l,o,w,e,r. First occurrences: Z,e,b,r,a,l,o,w -> "Zebralow". Matches!
    # "Hello World function lazy": H e l l o   W o r l d   f u n c t i o n   l a z y
    #   Duplicates: l(3 in Hello? H,e,l,l,o -> l twice), o(Hello, World, function -> 3), space(3), W(1), r(World, function? no r in function? f-u-n-c-t-i-o-n no r. World has r. So r once), 
    #   Let's compute first occurrences in order:
    #   H(1), e(1), l(1), l(dup skip), o(1), space(1), W(1), o(dup), r(1), l(dup), d(1), space(dup), f(1), u(1), n(1), c(1), t(1), i(1), o(dup), n(dup), space(dup), l(dup), a(1), z(1), y(1)
    #   Result: H e l o space W r d space f u n c t i a z y -> "Helo Wrd functiazy"? 
    #   Expected: "Helo Wrdfunctiazyh" (before h). Let's see: "Helo Wrd" then "functiazy"? 
    #   My sequence: H,e,l,o,space,W,r,d,space,f,u,n,c,t,i,a,z,y -> "Helo Wrd functiazy". 
    #   Expected "Helo Wrdfunctiazy": missing space between Wrd and functiazy. Hmm.
    #   Wait expected: "Helo Wrdfunctiazyh". So "Helo Wrd" + "functiazy" + "h". No space after Wrd.
    #   But there were two spaces in input? "Hello World function lazy" has spaces: after Hello, after World, after function. Three spaces.
    #   First space kept (after Helo). Second space (after World) - in my sequence it's kept. But expected drops it?
    #   Let's recount: H e l l o _ W o r l d _ f u n c t i o n _ l a z y
    #   First occurrences: H,e,l,o,_,W,r,d,_,f,u,n,c,t,i,a,z,y -> "Helo_Wrd_functiazy" with underscores as spaces.
    #   Expected: "Helo Wrdfunctiazy" - only one space. So second space removed?
    #   Maybe spaces are also deduplicated: first space kept, subsequent spaces removed. That gives "Helo Wrd" + "functiazy" = "Helo Wrdfunctiazy". Yes!
    #   So rule: keep first occurrence of each character (including space), remove later duplicates, then append 'h'.
    # Check "bananaUPPER": b,a,n,a,n,a,U,P,P,E,R. First occurrences: b,a,n,U,P,E,R -> "banUPER". Matches "banUPER" + h!
    # Check "Zebra": all unique -> "Zebra" + h. Matches.
    # Check "abc123": all unique -> "abc123" + h. Matches.
    # Check " Zebralower": space,Z,e,b,r,a,l,o,w,e(dup),r(dup) -> space,Z,e,b,r,a,l,o,w -> " Zebralow" + h. Matches.
    #
    # So: deduplicate characters keeping first occurrence, then append 'h'.
    # Case sensitivity: 'l' and 'L'? Not tested. Assume case-sensitive (distinct chars).
    # 'h' appended always? All outputs end with 'h'. Yes.
    # What if input already ends with 'h'? Unknown; assume still append 'h'.
    # What about empty string? Unknown; assume "" -> "h".
    # What about 'h' in input? It would be kept as first occurrence, then 'h' appended.

    def transform(s):
        seen = set()
        out = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
        return ''.join(out) + 'h'

    return {"outputs": [transform(x) for x in probe["inputs"]]}
