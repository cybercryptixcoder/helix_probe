def predict(probe):
    # Hypothesis: capitalize the FIRST alphabetic character of the string,
    # lowercase everything else? No — check evidence.
    # E1: "abc123"->"Abc123" (first char upper, rest lower)
    #     "level"->"Level"
    #     " Zebralower"->" zebralower" (leading space kept; 'Z' already upper, rest lower)
    #     "Hello World function lazy"->"Hello world function lazy"
    #       -> only FIRST letter of whole string is uppercased, rest lowercased.
    #     "bananaUPPER"->"Bananaupper"
    #     "Zebra"->"Zebra"
    # E2: "hello, world"->"Hello, world" (only first char of string)
    #     "foo-bar baz"->"Foo-bar baz"
    #     "a  b"->"A  b"
    #     "don't stop"->"Don't stop"
    #     "x1y2 z3"->"X1y2 z3"
    #     "  lead"->"  lead"  (first non-space? 'l' stays lower! so NOT first alpha)
    #     "trail  "->"Trail  "
    #     "multi   space"->"Ulti   space"  (!! 'm' dropped, 'u'->'U'? odd)
    #     "a.b.c"->"A.b.c"
    #     "CAPS lower"->"Caps lower"
    #
    # Reconcile: it looks like str.capitalize() on the whole string:
    #   capitalize: first char upper, rest lower.
    #   "  lead".capitalize() = "  lead"  ✓ (first char is space, rest lower)
    #   "multi   space".capitalize() = "Multi   space" ✗ (observed "Ulti   space")
    #   Hmm "Ulti   space" — the 'm' is gone and 'u' capitalized.
    #   That's weird. Maybe a bug in the box: it uppercases s[0] and lowercases s[1:],
    #   but for "multi   space" gives "Ulti   space"?? That drops 'm'.
    #   Actually maybe the box does: s[0].upper() + s[1:].lower() but with an off-by-one
    #   when... no. Let's just treat "multi   space" as an anomaly? Can't memorize.
    #   Best guess: str.capitalize() (first char upper, rest lower).
    #   The "Ulti   space" is likely a typo/edge in the box we can't generalize.
    out = []
    for s in probe["inputs"]:
        out.append(s.capitalize())
    return {"outputs": out}
