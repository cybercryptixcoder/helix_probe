def predict(probe):
    # Observations from E1:
    # "abc123" -> "Abc123": first letter capitalized, rest unchanged
    # "level" -> "Level": first letter capitalized
    # " Zebralower" -> "zebralower": leading space removed, then lowercased? 
    #   Actually " Zebralower" -> "zebralower" - space removed AND lowercased
    # "Hello World function lazy" -> "Helloworldfunctionlazy": spaces removed, and... 
    #   "Hello World function lazy" -> "Helloworldfunctionlazy"
    #   H-e-l-l-o W-o-r-l-d f-u-n-c-t-i-o-n l-a-z-y
    #   "Hello" stays "Hello", "World"->"world", "function"->"function", "lazy"->"lazy"
    #   So first word keeps case, subsequent words lowercased, spaces removed
    # "bananaUPPER" -> "Bananaupper": first letter cap, rest lowercased
    # "Zebra" -> "Zebra": first letter cap, rest unchanged (already)
    #
    # Hypothesis: 
    # 1. Remove all spaces
    # 2. Capitalize first letter of result, lowercase the rest? 
    #    But "Hello World function lazy" -> "Helloworldfunctionlazy" has "Hello" with capital H, 
    #    then "worldfunctionlazy" all lowercase. That's consistent with capitalize() on whole string!
    #    "abc123".capitalize() = "Abc123" ✓
    #    "level".capitalize() = "Level" ✓
    #    " Zebralower".capitalize() = " zebralower" - no, capitalize doesn't strip space
    #    But if we remove spaces first: "Zebralower".capitalize() = "Zebralower", not "zebralower"
    #    Hmm. " Zebralower" -> "zebralower". 
    #    Maybe: strip, then... no, "Zebralower".capitalize()="Zebralower"
    #    Wait - maybe lowercase everything first, then capitalize first char?
    #    " Zebralower" -> remove space -> "Zebralower" -> lower -> "zebralower" -> cap first -> "Zebralower"
    #    But observed is "zebralower" (lowercase z). So NOT capitalizing.
    #    
    #    Let me reconsider. Maybe: remove spaces, then capitalize() only if... no.
    #    "Hello World function lazy" -> "Helloworldfunctionlazy"
    #    If we remove spaces: "HelloWorldfunctionlazy", then .capitalize() -> "Helloworldfunctionlazy" ✓
    #    "bananaUPPER" -> remove spaces -> "bananaUPPER" -> .capitalize() -> "Bananaupper" ✓
    #    "Zebra" -> "Zebra" -> .capitalize() -> "Zebra" ✓
    #    "abc123" -> "abc123" -> .capitalize() -> "Abc123" ✓
    #    "level" -> "level" -> .capitalize() -> "Level" ✓
    #    " Zebralower" -> remove spaces -> "Zebralower" -> .capitalize() -> "Zebralower" 
    #    But observed "zebralower"! Contradiction.
    #
    #    Unless leading space matters differently. Maybe strip() then... no.
    #    What if spaces are removed but leading space causes something?
    #    " Zebralower" -> "zebralower". If we .lower() then .capitalize()? -> "Zebralower". No.
    #    What if it's: remove spaces, then if original had leading space, lowercase all?
    #    That seems arbitrary. Let me think differently.
    #
    #    Maybe: .strip() first, then remove internal spaces, then .capitalize()?
    #    " Zebralower".strip() = "Zebralower", .capitalize() = "Zebralower". Still not "zebralower".
    #
    #    Hmm what if the operation is: remove spaces, then lowercase, then capitalize ONLY first char 
    #    if the first char was originally uppercase? No...
    #
    #    Actually wait: maybe it's .title() related? No.
    #    Let me reconsider: maybe spaces are removed AND the string is lowercased, 
    #    EXCEPT the very first character is uppercased only if... 
    #    "abc123"->"Abc123" (A upper)
    #    "level"->"Level" (L upper)
    #    " Zebralower"->"zebralower" (z lower!)
    #    "Hello World function lazy"->"Helloworldfunctionlazy" (H upper)
    #    "bananaUPPER"->"Bananaupper" (B upper)
    #    "Zebra"->"Zebra" (Z upper)
    #
    #    The only lowercase-first is the one with leading space. 
    #    Maybe: if string starts with space, the "first char" after removing spaces is not capitalized?
    #    Like capitalize() applied to the string WITH space: " zebralower".capitalize() = " zebralower"
    #    then remove spaces: "zebralower" ✓!!!
    #    Let's test: "Hello World function lazy".capitalize() = "Hello world function lazy"
    #    then remove spaces: "Helloworldfunctionlazy" ✓
    #    "bananaUPPER".capitalize() = "Bananaupper", remove spaces -> "Bananaupper" ✓
    #    "abc123".capitalize() = "Abc123" ✓
    #    "level".capitalize() = "Level" ✓
    #    "Zebra".capitalize() = "Zebra" ✓
    #    " Zebralower".capitalize() = " zebralower", remove spaces -> "zebralower" ✓
    #
    #    So: capitalize() first, then remove all spaces!
    #    capitalize() makes first char upper, rest lower. Then remove spaces.
    #    That fits all 6!
    #
    # Rule: result = input.capitalize().replace(" ", "")
    # (?) Not sure about other whitespace like tabs/newlines - assume only spaces removed.
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s.capitalize().replace(" ", ""))
        except Exception:
            out.append("")
    return {"outputs": out}
