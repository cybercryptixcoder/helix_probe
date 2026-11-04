def predict(probe):
    # Split on runs of spaces; empty words dropped [E2, E4]
    # Reverse each word's letters [E1, E2]
    # Single word: "lmKA" + reversed word [E1]
    # Multi-word: reversed words joined by space, then " lmKA" + last reversed word [E1]
    # Trailing space matters: "racecar " -> "racecar lmKA" (treated as two words: "racecar" and empty) [E5]
    #   i.e. a trailing space creates an empty final word, which becomes the "last word" (empty),
    #   so output = reversed prior words + " lmKA" + "" = "racecar lmKA"
    # Leading spaces: dropped, no empty word [E2, E4, E5]
    # Empty / all spaces: "lmKA" [E2, E4]
    out = []
    for s in probe["inputs"]:
        # Split on single spaces, then drop leading empties but keep a trailing empty
        parts = s.split(" ")
        # Remove leading empty strings (from leading spaces)
        while parts and parts[0] == "":
            parts.pop(0)
        # Remove internal empty strings (runs of spaces collapse) but keep trailing empty
        cleaned = []
        for i, p in enumerate(parts):
            if p == "":
                if i == len(parts) - 1:
                    cleaned.append(p)  # keep trailing empty
                # else drop internal empty
            else:
                cleaned.append(p)
        rev = [w[::-1] for w in cleaned]
        if len(rev) == 0:
            out.append("lmKA")
        elif len(rev) == 1:
            out.append("lmKA" + rev[0])
        else:
            out.append(" ".join(rev[:-1]) + " lmKA" + rev[-1])
    return {"outputs": out}
