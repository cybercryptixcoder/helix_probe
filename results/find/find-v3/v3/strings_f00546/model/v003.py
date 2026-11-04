def predict(probe):
    # "lmKA" is inserted before the last whitespace-separated word [E1, E2, E3]
    # The text before that last word is reversed; the last word is reversed too [E3]
    #   E3 "test case" -> "tset lmKAesac": "test" reversed = "tset", "case" reversed = "esac"
    #   E2 "a b" -> "a lmKAb": "a" reversed = "a", "b" reversed = "b"
    #   E2 "ab cd" -> "ba lmKAdc": "ab"->"ba", "cd"->"dc"
    # So: reverse everything, but insert "lmKA" at the position of the last space
    #   (i.e. between the reversed last word and the reversed preceding text).
    # If there is no space, whole input is reversed and "lmKA" is prepended [E1, E3]
    out = []
    for s in probe.get("inputs", []):
        if " " in s:
            i = s.rfind(" ")
            # reverse the last word and the prefix separately, join with " lmKA"
            out.append(s[:i][::-1] + " lmKA" + s[i+1:][::-1])
        else:
            out.append("lmKA" + s[::-1])
    return {"outputs": out}
