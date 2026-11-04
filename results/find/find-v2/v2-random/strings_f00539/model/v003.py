def predict(probe):
    # Keep only first occurrence of each character (case-sensitive) [E1-E4]
    # Append 'h' at the end [E1-E4]
    # EXCEPTION: if the input starts with a space, do NOT append 'h' [E5]
    #   " hello" -> " helo" (no h); "world  " -> "world h" (has h)
    #   " Example" -> " Exampleh" (has h, starts with space!) -- wait, E4 contradicts?
    #   E4: " Example" -> " Exampleh" (starts with space, HAS h)
    #   E5: " hello" -> " helo" (starts with space, NO h)
    #   Difference? " Example" has uppercase E after space; " hello" lowercase.
    #   Hmm. Let's look: " hello" -> " helo" (5 chars in, 5 out, no h)
    #   " Example" -> " Exampleh" (8 in, 9 out, h added)
    #   Maybe: if result already ends in a char that... no.
    #   Alternative: maybe 'h' is only appended if 'h' not already in string? No, "abc123h" has no h in input.
    #   Check: " hello" contains 'h'! " Example" does not contain 'h'.
    #   Rule: append 'h' only if 'h' not already present in input [E5]
    #   Verify: "world  " no h -> "world h" ✓; "apple data apple" no h -> "aple dth" ✓
    #   "racecar" no h -> "raceh" ✓; "Zebra Example OpenAI" no h -> "...OnAIh" ✓
    #   "a!@#" no h -> "a!@#h" ✓
    #   E1-E4: none of those inputs contain 'h'? "Hello World function lazy" has 'H' (capital, not 'h')... 
    #     wait it has lowercase? "Hello World function lazy" - H,e,l,l,o... no lowercase h. ✓
    #   "function Hello World" - no lowercase h ✓
    #   " functionend." - no h ✓
    #   "test case apple" - no h ✓
    #   So rule: append 'h' unless 'h' already in input.
    def f(s):
        seen = set()
        out = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
        r = "".join(out)
        if 'h' not in s:
            r += 'h'
        return r
    return {"outputs": [f(x) for x in probe["inputs"]]}
