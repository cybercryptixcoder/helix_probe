def predict(probe):
    # Observations from E1:
    # - "hello" -> "hello" (unchanged)
    # - "Hello" -> "ello" (leading uppercase H removed)
    # - "HELLO" -> "ELLO" (leading uppercase H removed)
    # - "hello world" -> "hello world" (unchanged)
    # - "Hello World" -> "ello World" (leading uppercase H removed)
    # - "two words" -> "two words" (unchanged)
    # - "123" -> "123" (unchanged)
    # - "A1!" -> "A1!" (unchanged)
    # - "abc123" -> "abc123" (unchanged)
    # - "  spaced  " -> "spaced" (leading/trailing spaces stripped)
    #
    # Hypothesis: strip whitespace, then if the first character is an
    # uppercase letter, remove it. Otherwise unchanged.
    # "A1!" stays because... wait, A is uppercase. But "A1!" -> "A1!".
    # So the rule isn't simply "remove leading uppercase".
    # Re-examine: "Hello"->"ello", "HELLO"->"ELLO", "Hello World"->"ello World"
    # but "A1!"->"A1!". Difference: "A1!" has a digit/symbol after A.
    # Maybe only remove leading uppercase if followed by a lowercase letter?
    # "HELLO": H followed by E (uppercase) -> removed. So no.
    # Maybe remove leading uppercase if the string has length > 1 and
    # the rest contains a lowercase letter? "HELLO" has no lowercase but
    # H was removed. Hmm.
    # Alternative: remove leading uppercase letter if followed by a letter.
    # "A1!" -> A followed by '1' (not letter) -> kept. Consistent!
    # "Hello" -> H followed by 'e' (letter) -> removed. Consistent.
    # "HELLO" -> H followed by 'E' (letter) -> removed. Consistent.
    # "Hello World" -> H followed by 'e' -> removed. Consistent.
    # "abc123" -> 'a' lowercase -> unchanged. Consistent.
    # "two words" -> 't' lowercase -> unchanged. Consistent.
    # "123" -> '1' not letter -> unchanged. Consistent.
    # "  spaced  " -> strip -> "spaced", 's' lowercase -> unchanged. Consistent.
    #
    # Rule: strip whitespace; if first char is uppercase letter AND
    # second char exists and is a letter, drop the first char.
    # (?) Uncertain about single-char uppercase like "A" or "H".
    # (?) Uncertain about leading uppercase followed by space, e.g. "H ello".
    import re
    out = []
    for s in probe.get("inputs", []):
        try:
            t = s.strip()
            if len(t) >= 2 and t[0].isupper() and t[0].isalpha() and t[1].isalpha():
                t = t[1:]
            out.append(t)
        except Exception:
            out.append(s)
    return {"outputs": out}
