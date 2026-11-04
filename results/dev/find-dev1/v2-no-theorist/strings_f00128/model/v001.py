def predict(probe):
    # Observations from E1:
    # "" -> "10"
    # "a" -> "10a", "A" -> "10a" (case-insensitive? both give "10a")
    # "1" -> "101"
    # " " -> "10 "
    # "!" -> "10!"
    # "ab" -> "A10b", "a b" -> "A10 b"
    # "Hello" -> "He10llo", "hello" -> "He10llo"
    #
    # Pattern hypothesis: insert "10" at a position, and capitalize first letter?
    # "" -> "10": insert "10" at position 0.
    # "a" -> "10a": insert "10" at position 0.
    # "A" -> "10a": insert "10" at 0 and lowercase? Or capitalize... "A"->"10a" means first char lowercased.
    # "1" -> "101": insert "10" at 0 -> "101". Yes.
    # " " -> "10 ": insert "10" at 0.
    # "!" -> "10!": insert "10" at 0.
    # "ab" -> "A10b": hmm. If insert "10" at position 1: "a10b", then capitalize first -> "A10b". Yes!
    # "a b" -> "A10 b": insert "10" at position 1 -> "a10 b", capitalize -> "A10 b". Yes.
    # "Hello" -> "He10llo": insert "10" at position 2 -> "He10llo". Capitalize first (already H). Yes.
    # "hello" -> "He10llo": insert "10" at position 2 -> "he10llo", capitalize -> "He10llo". Yes.
    #
    # So: insert "10" at position len//2 (integer division), then capitalize first letter.
    # Check: "" len 0 -> pos 0 -> "10". ok.
    # "a" len 1 -> pos 0 -> "10a", capitalize -> "10a" (first char '1' unaffected). ok.
    # "A" len 1 -> pos 0 -> "10A", capitalize -> "10A"? But observed "10a". Hmm, lowercase.
    # Wait "A" -> "10a". So maybe lowercase the whole thing then capitalize first? "A" -> "a" -> "10a" -> capitalize first char '1' -> "10a". ok.
    # "ab" -> lowercase "ab", insert at 1 -> "a10b", capitalize -> "A10b". ok.
    # "Hello" -> lowercase "hello", insert at 2 -> "he10llo", capitalize -> "He10llo". ok.
    # "hello" -> "he10llo" -> "He10llo". ok.
    # "1" -> "1" -> insert at 0 -> "101" -> capitalize -> "101". ok.
    # " " -> " " -> "10 " -> capitalize -> "10 ". ok.
    # "!" -> "10!" -> capitalize -> "10!". ok.
    #
    # So rule: s2 = s.lower(); pos = len(s)//2; s3 = s2[:pos] + "10" + s2[pos:]; return s3.capitalize()
    # Note capitalize() lowercases rest too, but s2 already lowercase.
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            s2 = s.lower()
            pos = len(s) // 2
            s3 = s2[:pos] + "10" + s2[pos:]
            outputs.append(s3.capitalize())
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
