def predict(probe):
    # Observations:
    # "Hello World function lazy" -> "ello World function lazy" (H removed)
    # " Zebralower" -> "Zebralower" (leading space removed)
    # "banana data banana " -> "banana data banana" (trailing space removed)
    # "test case" -> "test case" (unchanged! has space, first char kept)
    # "Example123" -> "Example123" (unchanged)
    # "abc123","level","bananaUPPER","Zebra","lazy","banana" -> unchanged
    #
    # Hypothesis: strip leading/trailing whitespace, then remove first char
    #   only if... hmm. "Hello World..." -> H removed. "test case" -> unchanged.
    #   Difference: "Hello World function lazy" starts uppercase H, "test case" starts lowercase t.
    #   " Zebralower" -> after strip = "Zebralower", starts uppercase Z, but NOT removed!
    #   So that fails too.
    #
    # Reconsider: maybe it's strip() only, plus something else for "Hello World...".
    #   "Hello World function lazy" -> "ello World function lazy": only H removed, no strip needed.
    #   "test case" -> "test case": unchanged.
    #   "banana data banana " -> trailing space removed (strip).
    #   " Zebralower" -> leading space removed (strip).
    #   So: strip whitespace. Then why H removed from "Hello World..."?
    #   Maybe: if the string starts with uppercase AND contains a space, remove first char?
    #   "Hello World..." yes. "test case" no (lowercase). " Zebralower" after strip = "Zebralower" no space -> no removal. Good.
    #   "Example123" no space -> unchanged. Good.
    #   "bananaUPPER" no space -> unchanged. Good.
    #   "Zebra" no space -> unchanged. Good.
    #   "banana data banana " -> strip -> "banana data banana", starts lowercase -> unchanged. Good.
    #   "abc123","level","lazy","banana" -> unchanged. Good.
    # Rule: s = s.strip(); if s and s[0].isupper() and ' ' in s: s = s[1:]
    out = []
    for s in probe["inputs"]:
        s = s.strip()
        if s and s[0].isupper() and " " in s:
            s = s[1:]
        out.append(s)
    return {"outputs": out}
