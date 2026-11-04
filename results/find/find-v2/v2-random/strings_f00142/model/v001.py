def predict(probe):
    # Rule: shift every character's ASCII code by +5, then append 'W' [E1]
    # Verified on letters, digits, spaces, upper/lowercase, symbols [E1]
    out = []
    for s in probe["inputs"]:
        try:
            out.append(''.join(chr(ord(c) + 5) for c in s) + 'W')
        except Exception:
            out.append('')
    return {"outputs": out}
