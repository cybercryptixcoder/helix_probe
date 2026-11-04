def predict(probe):
    # "lmKA" is inserted before the last whitespace-separated word, not at the start [E1, E2]
    # The text before that word is reversed; the last word is left as-is [E1, E2]
    # If there is no space, whole input is reversed and "lmKA" is prepended [E1]
    out = []
    for s in probe.get("inputs", []):
        if " " in s:
            i = s.rfind(" ")
            out.append(s[:i][::-1] + " lmKA" + s[i+1:])
        else:
            out.append("lmKA" + s[::-1])
    return {"outputs": out}
