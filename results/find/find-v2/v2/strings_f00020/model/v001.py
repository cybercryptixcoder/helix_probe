def predict(probe):
    # Observations from E1:
    # "abc123" -> "abc51233": insert "5" before the first digit? Actually "abc123" -> "abc" + "5" + "123" + "3"? Let's look.
    #   abc123 -> abc51233. Original: a b c 1 2 3. Output: a b c 5 1 2 3 3. So "5" inserted before "123", and extra "3" appended.
    # "level" -> "lev5ell": l e v e l -> l e v 5 e l l. "5" inserted before last two chars? "level" -> "lev" + "5" + "el" + "l"? Hmm.
    #   Actually: level = l e v e l. Output l e v 5 e l l. So insert 5 after position 3 (before "el"), then duplicate last char.
    # " Zebralower" -> " Zebra5lowerr": " Zebralower" -> " Zebra" + "5" + "lower" + "r". Insert 5 before "lower", duplicate last char.
    # "Hello World function lazy" -> "Hello World f5unction lazyy": insert 5 before "unction" (after f), duplicate last char.
    # "bananaUPPER" -> "banana5UPPERR": insert 5 before "UPPER", duplicate last char.
    # "Zebra" -> "Zeb5raa": insert 5 before "ra", duplicate last char.
    #
    # Pattern: insert "5" at some position, and duplicate the last character.
    # Where is 5 inserted? Let's find index.
    # abc123: output abc51233. Insert at index 3 (before '1'). len=6, insert at 3 = len/2.
    # level: len=5, insert at index 3. Hmm len/2=2.5 -> 3? ceil(5/2)=3. Yes.
    # " Zebralower": len=12, insert at index 6 (" Zebra" is 6 chars). ceil(12/2)=6. Yes.
    # "Hello World function lazy": len=25, insert at index 13? "Hello World f" is 13 chars. ceil(25/2)=13. Yes.
    # "bananaUPPER": len=11, insert at index 6 ("banana"). ceil(11/2)=6. Yes.
    # "Zebra": len=5, insert at index 3 ("Zeb"). ceil(5/2)=3. Yes.
    #
    # Rule: insert "5" at index ceil(len/2), then append a copy of the last character.
    # ? Not sure if it's ceil(len/2) or something else; only one experiment.
    def f(s):
        try:
            n = len(s)
            idx = (n + 1) // 2
            out = s[:idx] + "5" + s[idx:]
            if s:
                out = out + s[-1]
            return out
        except Exception:
            return s
    return {"outputs": [f(x) for x in probe.get("inputs", [])]}
