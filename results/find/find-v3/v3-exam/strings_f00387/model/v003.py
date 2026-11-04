def predict(probe):
    # Observations:
    # - First char of string uppercased, rest lowercased [E1, E2].
    # - "multi   space" -> "Ulti   space": 'm' dropped, 'u' uppercased [E2].
    # - "Example123" -> "Exaple123": 'm' dropped, 'a'... wait 'a' stays [E3].
    #   "Example123" -> "Exaple123": the 'm' (index 2) is deleted.
    # - "multi   space" -> "Ulti   space": the 'm' (index 0) is deleted.
    # Hypothesis: the box deletes the first occurrence of 'm' (lowercase m),
    # then applies capitalize() to the result.
    #   "multi   space": remove 'm' -> "ulti   space" -> "Ulti   space" ✓
    #   "Example123": remove 'm' -> "Exaple123" -> "Exaple123" ✓
    #   "banana data banana ": no 'm' -> capitalize -> "Banana data banana " ✓
    #   "Hello World function lazy": no 'm' -> "Hello world function lazy" ✓
    #   "bananaUPPER": no 'm' -> "Bananaupper" ✓
    #   "  lead": no 'm' -> "  lead" ✓
    #   "don't stop": no 'm' -> "Don't stop" ✓
    #   "x1y2 z3": no 'm' -> "X1y2 z3" ✓
    #   "a.b.c": no 'm' -> "A.b.c" ✓
    #   "CAPS lower": no 'm' -> "Caps lower" ✓
    #   "Zebralower": no 'm' -> "Zebralower" ✓
    #   "abc123": no 'm' -> "Abc123" ✓
    #   "level": no 'm' -> "Level" ✓
    #   "Zebra": no 'm' -> "Zebra" ✓
    #   "foo-bar baz": no 'm' -> "Foo-bar baz" ✓
    #   "a  b": no 'm' -> "A  b" ✓
    #   "trail  ": no 'm' -> "Trail  " ✓
    #   "test case": no 'm' -> "Test case" ✓
    #   "lazy": no 'm' -> "Lazy" ✓
    #   "banana": no 'm' -> "Banana" ✓
    # Rule: delete first 'm' (if any), then str.capitalize().
    out = []
    for s in probe["inputs"]:
        i = s.find("m")
        if i != -1:
            s = s[:i] + s[i+1:]
        out.append(s.capitalize())
    return {"outputs": out}
