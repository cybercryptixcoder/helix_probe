def predict(probe):
    # Rules inferred from evidence:
    # R1: Remove all 'm'/'M' characters [E3, E4].
    # R2: Capitalize the first letter of the whole string (only the very first alphabetic
    #     character), lowercase all other letters [E1, E2, E3].
    # R3: BUT if the first character of the ORIGINAL input is uppercase, do NOT lowercase
    #     the rest — preserve case as-is (after m-removal) [E4: "Mango"->"Mango", "MOM"->"Mom"].
    #     Wait: "MOM"->"Mom": M kept, O->o, M->m. So first char upper, rest lowercased.
    #     "Mango"->"Mango": M kept, 'ango' already lower. Consistent with R2 applied to
    #     original (before m-removal)? Let's check: original "Mango", first char 'M' upper,
    #     rest lowercased -> "Mango", then remove m -> "Mango" (no m left? 'M' is at index 0).
    #     Hmm "Mango" has 'M' at index 0 and no other m. Removing 'M' would give "ango".
    #     But observed "Mango" keeps the M! So m-removal does NOT apply to the first char?
    #     Or: capitalization happens AFTER removal, and 'M' at start is re-capitalized.
    #     "Mango": remove m/M -> "ango", capitalize first -> "Ango". But observed "Mango".
    #     So that's wrong. Let's reconsider.
    #     "Mango"->"Mango": M preserved. "MOM"->"Mom": first M preserved, second M->m.
    #     "mango"->"Ango": m removed, then 'a' capitalized.
    #     "mom"->"O": m removed -> "o", capitalize -> "O". Yes.
    #     "MOM": if we remove all m/M -> "O", capitalize -> "O". But observed "Mom".
    #     So removal is NOT applied to the first character when it's uppercase 'M'?
    #     Alternative: the rule is "capitalize first letter, lowercase rest" applied to the
    #     ORIGINAL, THEN remove 'm'/'M' EXCEPT the first character.
    #     "Mango": capitalize-first/lower-rest -> "Mango", remove m/M except pos0 -> "Mango". ✓
    #     "MOM": -> "Mom", remove m/M except pos0 -> "Mom". ✓
    #     "mango": -> "Mango", remove m/M except pos0: pos0 is 'M' (from capitalized m)...
    #        if we keep pos0 -> "Mango", but observed "Ango". ✗
    #     Hmm. So the "keep first char" only applies when original first char was uppercase M?
    #     Let's think differently: maybe removal happens first, but capitalization is applied
    #     to the ORIGINAL first character's case.
    #     Actually: "Mango"->"Mango". If we remove m/M first: "ango". Then capitalize first
    #     letter -> "Ango". Not matching. So the M in "Mango" is NOT removed.
    #     "MOM"->"Mom": first M not removed, second M removed (and lowercased to m? no, removed).
    #        Wait "MOM" -> "Mom": M, o, m. The last M became 'm', not removed!
    #        So "MOM" -> "Mom" is just capitalize-first + lowercase-rest, NO removal at all!
    #     "Mango" -> "Mango": capitalize-first + lowercase-rest, no removal.
    #     "mango" -> "Ango": removal of m then capitalize.
    #     "mom" -> "O": removal of m then capitalize.
    #     "summer" -> "Suer": removal of m then capitalize.
    #     "m" -> "": removal.
    #     "am" -> "A": removal of m -> "a" -> "A".
    #     "ma" -> "A": removal of m -> "a" -> "A".
    #     "m m" -> " ": removal -> " ".
    #     "banana m banana" -> "Banana  banana": removal.
    #     "Example123" -> "Exaple123": removal.
    #     So: when does removal happen vs not?
    #     Inputs starting with uppercase 'M': "Mango"->"Mango", "MOM"->"Mom". NO removal.
    #     Inputs starting with lowercase 'm': removal happens.
    #     Inputs with m not at start: "summer"->"Suer" (removal), "Example123"->"Exaple123" (removal),
    #        "am"->"A" (removal), "banana m banana" (removal).
    #     So the ONLY exception is when the FIRST character is uppercase 'M'? 
    #     "MOM" first char M -> no removal anywhere? "MOM"->"Mom" has no removal (both M's: first kept, second lowercased to m). Yes no removal.
    #     "Mango" first char M -> no removal. Yes.
    #     Hypothesis: if the string starts with uppercase 'M', skip m-removal entirely;
    #        just capitalize-first + lowercase-rest.
    #     Otherwise: remove all m/M, then capitalize-first + lowercase-rest.
    #     Check "MOM": starts with M -> cap-first/lower-rest -> "Mom". ✓
    #     Check "Mango": -> "Mango". ✓
    #     Check "mango": not start M -> remove m -> "ango" -> "Ango". ✓
    #     Check "mom": remove m -> "o" -> "O". ✓
    #     Check "summer": remove m -> "suer" -> "Suer". ✓
    #     Check "Example123": remove m -> "Exaple123" -> cap-first -> "Exaple123". ✓
    #     Check "banana m banana": remove m -> "banana  banana" -> "Banana  banana". ✓
    #     Check "am": remove m -> "a" -> "A". ✓
    #     Check "ma": remove m -> "a" -> "A". ✓
    #     Check "m m": remove m -> " " -> " ". ✓
    #     Check "m": remove m -> "" -> "". ✓
    #     All consistent! But is "starts with uppercase M" the real boundary, or is it
    #     "starts with uppercase letter"? Only M-start uppercase tested. Mark with ?.
    #     Actually maybe simpler: the removal is of lowercase 'm' only, and uppercase 'M' is
    #     never removed but gets lowercased by the cap-first rule... let's test:
    #     "MOM": remove lowercase m only -> "MOM" (no lowercase m) -> cap-first/lower-rest -> "Mom". ✓
    #     "Mango": remove lowercase m -> "Mango" (no lowercase m) -> "Mango". ✓
    #     "mango": remove lowercase m -> "ango" -> "Ango". ✓
    #     "mom": remove lowercase m -> "oo"? no: "mom" -> remove 'm' -> "oo"? wait "mom" letters m,o,m -> remove both m -> "o" -> "O". ✓
    #     "summer": s,u,m,m,e,r -> remove m -> "suer" -> "Suer". ✓
    #     "Example123": E,x,a,m,p,l,e -> remove m -> "Exaple123" -> "Exaple123". ✓
    #     "MOM": no lowercase m -> "MOM" -> "Mom". ✓
    #     This is simpler and consistent! Remove only lowercase 'm', not uppercase 'M'.
    #     But then "MOM" -> "Mom": the second M is lowercased to 'm' by cap-first rule, not removed.
    #     And "Mango" -> "Mango". 
    #     What about a string like "aM" -> remove lowercase m (none) -> "aM" -> cap-first/lower-rest -> "Am". 
    #     Untested but plausible.
    #     This "remove lowercase m only" rule fits ALL evidence. Let's go with it.
    # R4: Capitalize first alphabetic character, lowercase all subsequent alphabetic chars [E1,E2].
    #     Non-letters pass through unchanged, and don't count as "first letter" [E1: " Zebralower"->" zebralower",
    #     "123 hello"->"123 hello"].
    def transform(s):
        s = s.replace("m", "")  # remove lowercase m only
        out = []
        seen = False
        for ch in s:
            if ch.isalpha():
                if not seen:
                    out.append(ch.upper())
                    seen = True
                else:
                    out.append(ch.lower())
            else:
                out.append(ch)
        return "".join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
