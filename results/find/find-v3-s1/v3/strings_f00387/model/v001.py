def predict(probe):
    # Capitalize first letter of each word, lowercase the rest [E1]
    # "apple"->"Apple", "test caseMiXeD"->"Test casemixed", "Mississippi Hello World data"->"Mississippi hello world data"
    # Note: only the first letter of each whitespace-separated word is uppercased; rest lowercased.
    # "test case " -> "Test case " (trailing space preserved)
    # "data a Python " -> "Data a python "
    out = []
    for s in probe["inputs"]:
        # capitalize each word: first char upper, rest lower, preserving separators
        res = []
        at_word_start = True
        for ch in s:
            if ch.isspace():
                res.append(ch)
                at_word_start = True
            else:
                if at_word_start:
                    res.append(ch.upper())
                    at_word_start = False
                else:
                    res.append(ch.lower())
        out.append("".join(res))
    return {"outputs": out}
