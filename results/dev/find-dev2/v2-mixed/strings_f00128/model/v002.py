def predict(probe):
    # Rules (evidence):
    # - Lowercase everything, then uppercase the first character [E1,E2,E3,E4]
    # - Insert "10" at position floor(len/2) of the transformed string [E1,E2,E3,E4]
    # - For empty string: unknown; guess "10" [?]
    # - For single char "a": "10a" means pos 0, but floor(1/2)=0, so insert at 0 [E4]
    #   Wait: "a" -> "10a": transformed "A", pos floor(1/2)=0 -> "10"+"A" = "10A". But observed "10a"!
    #   So first char is NOT uppercased when insertion happens before it? Or lowercase applied after insert?
    #   "a"->"10a": if we insert "10" at pos 0 into "a", then capitalize first char of result -> "10a" (first char '1' not a letter). Yes!
    #   So order: lowercase all, insert "10" at floor(len/2), THEN uppercase first character of the result.
    #   Check "ab"->"A10b": lowercase "ab", pos1 -> "a10b", capitalize first -> "A10b". Yes.
    #   Check "abcd"->"Ab10cd": "abcd" pos2 -> "ab10cd", cap -> "Ab10cd". Yes.
    #   Check "ABC"->"A10bc": "abc" pos1 -> "a10bc", cap -> "A10bc". Yes.
    #   Check "a"->"10a": "a" pos0 -> "10a", cap first char '1' stays -> "10a". Yes!
    #   Check "123"->"11023": "123" pos1 -> "11023", cap '1' -> "11023". Yes.
    #   Check "42"->"4102": pos1 -> "4102". Yes.
    #   Check "MiXeD"->"Mi10xed": "mixed" pos2 -> "mi10xed", cap -> "Mi10xed". Yes.
    #   Check "a b c d"->"A b10 c d": "a b c d" len7 pos3 -> "a b10 c d", cap -> "A b10 c d". Yes.
    def transform(s):
        t = s.lower()
        pos = len(t) // 2
        t = t[:pos] + "10" + t[pos:]
        if t:
            t = t[0].upper() + t[1:]
        return t
    return {"outputs": [transform(x) for x in probe["inputs"]]}
