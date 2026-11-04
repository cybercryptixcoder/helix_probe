def predict(probe):
    # Every character's ASCII code is incremented by 1, no wrapping [E1, E2]
    # 'z'->'[' , 'Z'->'[' , '~'->DEL, '!'->'"' all consistent with +1 on ord [E2]
    # Letters, digits, spaces, punctuation all shift equally [E1, E2]
    out = []
    for s in probe.get("inputs", []):
        r = []
        for c in s:
            r.append(chr(ord(c) + 1))
        out.append(''.join(r))
    return {"outputs": out}
