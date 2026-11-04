def predict(probe):
    # Observations from E1:
    # "abc123" -> "Abc123": first letter capitalized, rest unchanged
    # "level" -> "Level": first letter capitalized
    # " Zebralower" -> "zebralower": leading space removed, first letter lowercased?
    #   Actually " Zebralower" -> "zebralower" - space stripped, then first char lowercased
    # "Hello World function lazy" -> "Helloworldfunctionlazy": spaces removed, case preserved
    # "bananaUPPER" -> "Bananaupper": first letter capitalized, rest lowercased
    # "Zebra" -> "Zebra": unchanged
    #
    # Hypothesis: remove all spaces, then capitalize first letter and lowercase rest?
    # Check: "abc123" -> "abc123" -> "Abc123" ✓
    # "level" -> "level" -> "Level" ✓
    # " Zebralower" -> "Zebralower" -> "Zebralower" ✗ (observed "zebralower")
    #
    # Hmm. " Zebralower" -> "zebralower". If we strip leading space first, "Zebralower",
    # then lowercase first? That gives "zebralower" ✓ but conflicts with "Zebra"->"Zebra".
    #
    # Alternative: maybe it's title-case-ish but only first word? Let's reconsider.
    # "Hello World function lazy" -> "Helloworldfunctionlazy" - spaces removed, NO case change
    #   (H stays H, W stays W, f stays f, l stays l)
    # "bananaUPPER" -> "Bananaupper" - B upper, rest lower
    # "abc123" -> "Abc123" - A upper, rest lower
    # "level" -> "Level" - L upper, rest lower
    # "Zebra" -> "Zebra" - Z upper, rest lower (already)
    # " Zebralower" -> "zebralower" - z lower, rest lower
    #
    # So for single-word (no internal space) inputs: capitalize first letter, lowercase rest.
    # But " Zebralower" has leading space. After removing spaces: "Zebralower" -> should be "Zebralower".
    # Observed "zebralower". So leading space matters differently.
    #
    # Maybe: if input starts with space, lowercase everything and strip spaces?
    # Or: the rule operates on original string: capitalize first char, lowercase rest, then remove spaces?
    # " Zebralower": first char is space -> capitalize(space)=space, rest lowercased = "zebralower", 
    #   remove spaces -> "zebralower" ✓
    # "Hello World function lazy": first char H, rest lowercased -> "Hello world function lazy",
    #   remove spaces -> "Helloworldfunctionlazy" ✓
    # "bananaUPPER": first b->B, rest lower -> "Bananaupper" ✓
    # "abc123": "Abc123" ✓
    # "level": "Level" ✓
    # "Zebra": "Zebra" ✓
    #
    # So: capitalize first character, lowercase the rest, then remove all spaces.
    # Check "Hello World function lazy": H + "ello world function lazy" lowercased = 
    #   "Hello world function lazy", remove spaces = "Helloworldfunctionlazy" ✓
    # 
    # Rule: s[0].upper() + s[1:].lower(), then remove spaces.
    # Edge: empty string -> "".
    def f(s):
        if not s:
            return ""
        t = s[0].upper() + s[1:].lower()
        return t.replace(" ", "")
    return {"outputs": [f(x) for x in probe["inputs"]]}
