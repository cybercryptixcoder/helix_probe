def predict(probe):
    # f inserts "10" into the string at a position determined by the input.
    # Evidence:
    # "" -> "10"                  [E1] empty: insert at start
    # "a" -> "10a"                [E1] insert before 'a'
    # "A" -> "10a"                [E1] uppercase lowered, insert before
    # "1" -> "101"                [E1] insert before digit
    # "!" -> "10!"                [E1] insert before symbol
    # " " -> "10 "                [E1] insert before space
    # "ab" -> "A10b"              [E1] 'a'->'A', insert after first char
    # "a b" -> "A10 b"            [E1] 'a'->'A', insert after first char
    # "Hello, World!" -> "Hello,10 world!" [E1] insert after "Hello,"
    # "123" -> "11023"            [E1] insert after first char
    #
    # Hypothesis (?): the box finds a "split point" and inserts "10" there.
    # For single-char inputs the split point is 0 (before the char).
    # For multi-char inputs the split point is 1 (after first char).
    # Additionally, the first character is uppercased if it is a letter,
    # and the rest of the string is lowercased if it is a letter.
    # "Hello, World!" -> "Hello,10 world!" : first char already upper,
    #   rest lowercased ("World" -> "world"), insert after position 6.
    # That contradicts a fixed split point of 1. So the split point varies.
    #
    # Re-examine: "Hello, World!" -> "Hello,10 world!". Insert position 6,
    # which is right after "Hello,". Hmm, that's after the first word+comma.
    # Maybe split after first "word boundary"? "ab"->"A10b": after 'a'.
    # "a b"->"A10 b": after 'a'. "123"->"11023": after '1'.
    # So for short strings split=1; for "Hello, World!" split=6.
    #
    # Alternative: insert "10" after the first "token" where a token is
    # a run of same-class characters? "Hello," is letters then comma...
    # Actually "Hello, World!" split at 6 = after "Hello,". That's the
    # first word plus following punctuation. "ab" split at 1 = after "a".
    # "a b" split at 1 = after "a" (space not included).
    # "123" split at 1 = after "1".
    #
    # Simplest consistent rule (?): split after the first character,
    # EXCEPT when there is a comma, split after the comma.
    # This is a guess; only one comma case exists.
    #
    # Case rule: first letter uppercased, subsequent letters lowercased.
    # "A"->"10a": first char 'A' became 'a'?? Output "10a" lowercase.
    # Wait "A"->"10a" but "a"->"10a" too. So single 'A' lowercased.
    # "ab"->"A10b": 'a'->'A' uppercased. Contradiction with "A"->"a".
    # Hmm. "A"->"10a" (lower), "ab"->"A10b" (upper first).
    # Maybe: the char right before "10" ... no.
    # Perhaps case: the character at split boundary? Unclear.
    #
    # Given uncertainty, best guess: lowercase everything except uppercase
    # the first letter of multi-char strings. For single char, lowercase.
    # Mark heavily with ?.

    def transform(s):
        if s == "":
            return "10"
        # determine split point
        if "," in s:
            idx = s.index(",") + 1
        else:
            idx = 1
        left = s[:idx]
        right = s[idx:]
        # case handling (?)
        if len(s) == 1:
            left = left.lower()
        else:
            if left and left[0].isalpha():
                left = left[0].upper() + left[1:].lower()
            else:
                left = left.lower()
        right = right.lower()
        return left + "10" + right

    return {"outputs": [transform(x) for x in probe["inputs"]]}
