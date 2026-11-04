def predict(probe):
    # Observations from E1:
    # - "abc123" -> "Abc123": first letter capitalized, rest unchanged
    # - "level" -> "Level": first letter capitalized
    # - " Zebralower" -> "zebralower": leading space stripped, then... "Z" became "z"?
    #   Wait: " Zebralower" -> "zebralower". Leading space removed, and Z lowercased.
    # - "Hello World function lazy" -> "Helloworldfunctionlazy": spaces removed, case preserved
    # - "bananaUPPER" -> "Bananaupper": first letter capitalized, rest lowercased
    # - "Zebra" -> "Zebra": unchanged (already capitalized)
    #
    # Hypothesis: 
    # 1. Strip all whitespace (spaces removed).
    # 2. Then capitalize first letter and lowercase the rest? 
    #   Check "abc123" -> "Abc123": capitalize first, lowercase rest -> "Abc123" ✓
    #   "level" -> "Level" ✓
    #   "bananaUPPER" -> "Bananaupper" ✓ (capitalize first, lowercase rest)
    #   "Hello World function lazy" -> remove spaces -> "HelloWorldfunctionlazy" -> capitalize first, lowercase rest -> "Helloworldfunctionlazy" ✓
    #   "Zebra" -> "Zebra" ✓
    #   " Zebralower" -> remove spaces -> "Zebralower" -> capitalize first, lowercase rest -> "Zebralower" 
    #     But observed "zebralower" (lowercase z!). Contradiction.
    #
    # Hmm. " Zebralower" -> "zebralower". If we strip spaces first, we get "Zebralower",
    # capitalize -> "Zebralower". But observed is "zebralower".
    # Maybe leading space means something? Or maybe the rule is: capitalize first char of
    # original string, then lowercase rest, then remove spaces?
    #   " Zebralower": first char is space. capitalize(space)=space, rest lowercased -> " zebralower", 
    #     then remove spaces -> "zebralower" ✓
    #   "Hello World function lazy": first char 'H' -> "H", rest lowercased -> "hello world function lazy",
    #     remove spaces -> "helloworldfunctionlazy". But observed "Helloworldfunctionlazy" (capital H!).
    #     Contradiction.
    #
    # Let me reconsider. Maybe: capitalize first letter (skip non-letters?), lowercase the rest,
    # then remove spaces.
    #   "Hello World function lazy": capitalize first letter 'H', lowercase rest -> "Hello world function lazy",
    #     remove spaces -> "Helloworldfunctionlazy" ✓
    #   " Zebralower": first letter is 'Z' (skip space). capitalize 'Z' -> 'Z', lowercase rest -> "Zebralower",
    #     remove spaces -> "Zebralower". But observed "zebralower". Contradiction.
    #
    # Alternative: maybe the rule is capitalize() applied to the whole string after removing spaces?
    #   " Zebralower" -> remove spaces -> "Zebralower" -> capitalize -> "Zebralower". Still capital Z.
    #
    # What if leading whitespace causes lowercasing? Or what if the rule is:
    #   title-case-ish but only first word? 
    #   "bananaUPPER" -> "Bananaupper": looks like .capitalize() (first upper, rest lower)
    #   "abc123" -> "Abc123": .capitalize() ✓
    #   "level" -> "Level": .capitalize() ✓
    #   "Zebra" -> "Zebra": .capitalize() ✓
    #   "Hello World function lazy": .capitalize() -> "Hello world function lazy", then remove spaces -> "Helloworldfunctionlazy" ✓
    #   " Zebralower": .capitalize() -> " zebralower" (capitalize lowercases rest, first char space stays),
    #     then remove spaces -> "zebralower" ✓ !!
    #
    # Yes! .capitalize() on the original string, then remove all spaces.
    #   " Zebralower".capitalize() = " zebralower" (first char space, rest lowercased)
    #   remove spaces -> "zebralower" ✓
    #
    # So rule: s.capitalize() then remove all spaces.
    # But wait, does it remove only spaces or all whitespace? Unknown. Assume spaces only for now.
    # Also "abc123".capitalize() = "Abc123" ✓
    # "bananaUPPER".capitalize() = "Bananaupper" ✓
    # "Hello World function lazy".capitalize() = "Hello world function lazy" -> remove spaces -> "Helloworldfunctionlazy" ✓
    # "Zebra".capitalize() = "Zebra" ✓
    # "level".capitalize() = "Level" ✓
    #
    # All consistent! Rule: remove spaces after capitalize().
    # Actually order matters: capitalize first (on original), then remove spaces.
    # Equivalent: capitalize() then replace(" ", "").
    #
    # What about other whitespace like tabs/newlines? Unknown, guess remove all whitespace? 
    # But capitalize on " hello" gives " hello" -> strip spaces -> "hello". 
    # I'll remove spaces only (safer given evidence), mark with ?.
    
    out = []
    for s in probe.get("inputs", []):
        try:
            t = s.capitalize()
            t = t.replace(" ", "")
            out.append(t)
        except Exception:
            out.append("")
    return {"outputs": out}
