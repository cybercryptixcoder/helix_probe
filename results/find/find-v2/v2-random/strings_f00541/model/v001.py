def predict(probe):
    # Hypothesis: f removes a leading space if present? No — " Zebralower" -> "Zebralower" (leading space stripped)
    # But "Hello World function lazy" -> "ello World function lazy" (leading 'H' removed, not a space)
    # So: remove the first character if it is uppercase? "Hello..." -> "ello..." (H removed)
    # " Zebralower" -> "Zebralower": first char is space, removed. So: remove first character unconditionally?
    # Check others: "abc123" -> "abc123" (unchanged, first char 'a' lowercase kept)
    # "level" -> "level" (unchanged)
    # "bananaUPPER" -> "bananaUPPER" (unchanged)
    # "Zebra" -> "Zebra" (unchanged, first char 'Z' uppercase kept!)
    # So not "remove first char unconditionally", and not "remove uppercase first char" (Zebra kept).
    # "Hello World function lazy" -> "ello World function lazy": H removed.
    # " Zebralower" -> "Zebralower": space removed.
    # What distinguishes "Hello..." and " Zebralower" from "Zebra", "abc123", "level", "bananaUPPER"?
    # Maybe: remove leading char if the string contains a space? "Hello World..." has spaces -> removed H.
    # " Zebralower" has a space -> removed leading space.
    # "abc123","level","bananaUPPER","Zebra" have no spaces -> unchanged.
    # That fits all evidence. Rule: if ' ' in s, drop first character; else unchanged.
    out = []
    for s in probe["inputs"]:
        if " " in s and len(s) > 0:
            out.append(s[1:])
        else:
            out.append(s)
    return {"outputs": out}
