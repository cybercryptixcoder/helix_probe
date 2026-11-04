def predict(probe):
    # Capitalize first letter, lowercase the rest [E1: abc123->Abc123, level->Level,
    #   " Zebralower"->" zebralower", "Hello World function lazy"->"Hello world function lazy",
    #   bananaUPPER->Bananaupper, Zebra->Zebra]
    # Leading space preserved; only first char of whole string is capitalized.
    # E2: "Example123"->"Exaple123" — the second 'm' is dropped, so a character is deleted.
    #   Hypothesis (?): the box deletes the second character of the string, then
    #   capitalizes first letter and lowercases the rest.
    #   Check: "test case"->"Test case" (would delete 'e' -> "tst case"->"Tst case"? no).
    #   So deletion is not universal. "Example123" has 'x' at index 1... deleting index 1
    #   gives "Eample123" not "Exaple123". Deleting index 2 ('a') gives "Exmple123" no.
    #   "Exaple123" = "Example123" with the 'm' (index 2) removed? E-x-a-m-p-l-e -> E-x-a-p-l-e
    #   yes: remove index 3 ('m'). Hmm "Exaple" = E x a p l e, original E x a m p l e, so 'm' removed.
    #   Only "Example123" shows this; other inputs unchanged. Likely a special word rule (?).
    #   Best guess: the word "Example" is transformed to "Exaple" (a typo rule), then
    #   capitalize-first/lowercase-rest applies. Marked uncertain.
    out = []
    for s in probe["inputs"]:
        t = s.replace("Example", "Exaple").replace("example", "exaple")
        out.append(t[:1].upper() + t[1:].lower())
    return {"outputs": out}
