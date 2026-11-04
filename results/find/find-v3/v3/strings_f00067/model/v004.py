def predict(probe):
    # Reverse each whitespace-separated word, join with single spaces. [E1-E4]
    # Strip leading/trailing whitespace first. [E2, E3]
    # Then prepend the last character of the last word to the reversed last word
    #   (duplicating it), UNLESS that character is an uppercase letter. [E1-E4]
    # The "repeat word" suppression in v3 was wrong: E4 shows dup happens even
    #   when the last word repeats an earlier word. The E3 "banana data banana "
    #   case had a trailing space, so after strip the last word is "banana" and
    #   it DOES dup -> "aananab". v3 misread that. [E4]
    outs = []
    for s in probe.get("inputs", []):
        t = s.strip()
        if t == "":
            outs.append("")
            continue
        words = t.split()
        rev = [w[::-1] for w in words]
        last = words[-1]
        if last and not last[-1].isupper():
            rev[-1] = last[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
