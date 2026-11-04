def predict(probe):
    # Observations from E1:
    # - "abc123" -> "abcZ123": Z inserted before first digit
    # - "level" -> "leZvel": Z inserted in middle (len 5 -> pos 2)
    # - " Zebralower" -> "ZebraZlower": leading space removed, Z inserted at middle of remaining? "Zebralower"(10) -> "ZebraZlower" Z at pos 5
    # - "Hello World function lazy" -> "HelloWorldfZunctionlazy": spaces removed, Z inserted in middle of "HelloWorldfunctionlazy"(23) -> pos 11? "HelloWorldf" is 11 chars, then Z. yes pos 11
    # - "bananaUPPER" -> "bananZaUPPER": Z at pos 5 (len 11 -> middle 5)
    # - "Zebra" -> "ZeZbra": Z at pos 2 (len 5 -> middle 2)
    # Rule: remove spaces, then insert 'Z' at index len//2.
    # Check: "abc123" len 6 -> 3? but Z at pos 3 -> "abcZ123" yes pos 3 = 6//2.
    # "level" len5 -> 2 -> "leZvel" yes.
    # " Zebralower" remove space -> "Zebralower" len10 -> 5 -> "ZebraZlower" yes.
    # "Hello World function lazy" remove spaces -> "HelloWorldfunctionlazy" len23 -> 11 -> "HelloWorldf"+"Z"+"unctionlazy" yes.
    # "bananaUPPER" len11 -> 5 -> "banan"+"Z"+"aUPPER" yes.
    # "Zebra" len5 -> 2 -> "Ze"+"Z"+"bra" yes.
    def f(s):
        s = s.replace(" ", "")
        i = len(s) // 2
        return s[:i] + "Z" + s[i:]
    return {"outputs": [f(x) for x in probe["inputs"]]}
