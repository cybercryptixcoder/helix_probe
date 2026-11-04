def predict(probe):
    # Rule: keep first occurrence of each character (global dedupe), then append 'h' [E1, E2]
    # EXCEPT: if the deduped result already ends in 'h', do not append another 'h' [E2: "hello world hello" -> "helo wrd"]
    #   - "hello world hello" dedupes to "helo wrd" (already ends in 'd'... wait, ends in 'd')
    #   Re-check: "hello world hello" -> dedupe: h,e,l,o,space,w,r,d -> "helo wrd", ends in 'd', not 'h'.
    #   But observed is "helo wrd" with NO trailing 'h'. So the append rule is conditional somehow.
    #   Compare with "abc123" -> "abc123h" (appended). "level" -> "levh" (appended).
    #   "hello world hello" -> "helo wrd" (NOT appended).
    #   Difference: input contains 'h' already? "hello world hello" contains 'h'.
    #   "abc123" no 'h'. "level" no 'h'. "Zebra" no 'h'. "bananaUPPER" no 'h'.
    #   "Hello World function lazy" contains 'H' (uppercase). Output "Helo Wrdfunctiazyh" - has 'h' appended.
    #   Hmm, so uppercase 'H' doesn't count, but lowercase 'h' does?
    #   "hello world hello" has lowercase 'h' -> no append.
    #   "abcabcABC" -> "abcABCh" (appended, no lowercase 'h' in input). ✓
    #   "  double  space" -> " doublespach" (appended, no 'h' in input). ✓
    #   "!@#!@#" -> "!@#h" (appended). ✓
    #   "112233" -> "123h" (appended). ✓
    #   "mississippi" -> "misph" (appended, no 'h'). ✓
    #   "aA aA" -> "aA h" (appended, no 'h'). ✓
    #   "AaAa" -> "Aah" (appended, no 'h'). ✓
    #   "aabbaa" -> "abh" (appended). ✓
    #   "ababab" -> "abh" (appended). ✓
    #   " Zebralower" -> " Zebralowh" (appended, no 'h'). ✓
    #   "Zebra" -> "Zebrah" (appended). ✓
    #   "level" -> "levh" (appended). ✓
    #   "abc123" -> "abc123h" (appended). ✓
    #   "bananaUPPER" -> "banUPERh" (appended). ✓
    #   "Hello World function lazy" -> "Helo Wrdfunctiazyh" (appended; contains 'H' uppercase only). ✓
    #   "hello world hello" -> "helo wrd" (NOT appended; contains lowercase 'h'). ✓
    #
    # Hypothesis: append 'h' only if the deduped string does not already contain lowercase 'h'.
    #   Check: "hello world hello" dedupe = "helo wrd" contains 'h' -> no append. ✓
    #   All others don't contain lowercase 'h' -> append. ✓
    #   Edge: what if input has 'h' but dedupe drops it? Not possible—first occurrence kept.
    out = []
    for s in probe["inputs"]:
        seen = set()
        res = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                res.append(ch)
        r = "".join(res)
        if "h" not in r:
            r += "h"
        out.append(r)
    return {"outputs": out}
