def predict(probe):
    # Words are whitespace-split; each word is reversed individually [E1,E2,E3]
    # Split point: all-but-last word before lmKA, last word after [E2,E3,E6]
    # If input ends in whitespace, ALL words go before lmKA [E2,E4,E6]
    # Multiple/leading spaces normalized to single spaces between words [E4,E6]
    # lmKA sits between halves; no leading space if no "before" words [E1,E5]
    # All-whitespace input yields just "lmKA" [E2]
    outputs = []
    for s in probe["inputs"]:
        words = s.split()  # handles any whitespace runs, strips ends
        trailing = len(s) > 0 and s[-1].isspace()

        if trailing:
            before, after = words, []
        elif words:
            before, after = words[:-1], words[-1:]
        else:
            before, after = [], []

        left = " ".join(w[::-1] for w in before)
        right = " ".join(w[::-1] for w in after)

        if left:
            res = left + " lmKA" + right
        else:
            res = "lmKA" + right
        outputs.append(res)

    return {"outputs": outputs}
