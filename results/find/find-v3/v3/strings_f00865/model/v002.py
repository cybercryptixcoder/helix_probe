def predict(probe):
    # First char shifted back 2 in alphabet (wrap), rest unchanged [E1-E6]
    # Only if first char is a letter [E4,E6: digits/symbols/space unchanged]
    outs = []
    for s in probe["inputs"]:
        if s and s[0].isalpha() and s[0].isascii():
            c = s[0]
            if c.islower():
                c = chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
            else:
                c = chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
            outs.append(c + s[1:])
        else:
            outs.append(s)
    return {"outputs": outs}
