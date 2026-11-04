def predict(probe):
    # Model beliefs:
    # 1. The box removes every uppercase 'H' character from the input string [E2, E4, E6].
    #    - "H" -> "", "Hello" -> "ello", "HHHello" -> "ello", "aH bH c" -> "a b c"
    # 2. Lowercase 'h' is left untouched [E6: "hello"->"hello", "hH"->"h", "h"->"h"].
    # 3. Other uppercase letters are untouched [E1 "Zebra"->"Zebra", E5 "World" stays].
    # 4. Spaces are preserved except those that were adjacent to removed H's [E2 "H H"->" ",
    #    E4 "H Hello"->" ello", " H"->""], i.e. simply delete 'H' chars.
    # 5. Trailing spaces are stripped from the final result [E3 "banana data banana "->"banana data banana",
    #    E5 "banana a data "->"banana a data", "Example "->"Example"].
    #    Leading spaces are NOT stripped [E1 " Zebralower"->"Zebralower"? wait].
    #    Check E1: " Zebralower" -> "Zebralower": leading space removed too.
    #    E4 "  Hello"->"ello", "   Hello"->"ello", "  lead"->"lead": leading spaces removed.
    #    So the result is stripped of leading and trailing whitespace after deleting H's.
    #    But E2 " Hello"->"ello", " He"->"e", "  two spaces"->"two spaces": consistent with strip.
    #    E4 " Hello "->"ello": consistent.
    #    E6 "H H"->" ": after deleting H's we get " " which strips to ""? But output is " ".
    #    Wait E6 "H H" output is " " (a single space). Hmm.
    #    Let's recheck: E2 "H H" -> " ". E6 "H H" -> " ". So a lone space survives.
    #    But " Hello" -> "ello" (leading space gone). "  two spaces"->"two spaces".
    #    So stripping removes leading/trailing spaces only if there is non-space content?
    #    Actually "H H" delete H -> " " (one space). If we strip, we'd get "". But output is " ".
    #    Maybe the rule is: strip leading and trailing whitespace, but if the result is empty and
    #    original after deletion was all spaces, keep one space? Check E4 "H H"? not present.
    #    E4 "HH" -> "". "HHH" -> "". Those delete to "".
    #    E2 "H H" -> " ". So deletion of H's gives " ", then strip would give "". Contradiction.
    #    Alternative: maybe the box removes H's, then strips leading/trailing spaces, but the
    #    strip happens BEFORE H removal? Let's test: "H H" strip -> "H H" (no change), remove H -> " ".
    #    " Hello" strip -> "Hello", remove H -> "ello". Good.
    #    "  two spaces" strip -> "two spaces", remove H -> "two spaces". Good.
    #    " Hello " strip -> "Hello", remove H -> "ello". Good.
    #    "  lead" strip -> "lead", remove H -> "lead". Good.
    #    " Zebralower" strip -> "Zebralower", remove H -> "Zebralower". Good.
    #    "banana data banana " strip -> "banana data banana", remove H -> same. Good.
    #    "H H" strip -> "H H", remove H -> " ". Good!
    #    "HH" strip -> "HH", remove H -> "". Good.
    #    " H" strip -> "H", remove H -> "". Good.
    #    "H Hello" strip -> "H Hello", remove H -> " ello". Output E4 "H Hello"->" ello". Good.
    #    " Hello " strip -> "Hello", remove H -> "ello". Good.
    #    So order: strip whitespace first, then delete all 'H' characters.
    #    Check E1 "Hello World function lazy" -> strip same -> delete H -> "ello World function lazy". Good.
    #    E5 "function Hello World" -> delete H -> "function ello World". Good.
    #    E6 "shHello" -> delete H -> "shello". Good.
    # 6. Only uppercase H is removed; lowercase h remains.
    s = probe["inputs"]
    outs = []
    for x in s:
        t = x.strip()
        t = t.replace("H", "")
        outs.append(t)
    return {"outputs": outs}
