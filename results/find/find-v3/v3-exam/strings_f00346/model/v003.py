def predict(probe):
    # Rule: remove all spaces [E1, E2, E3]
    # Rule: shift the first character by +2 in ASCII, wrapping within letters [E1, E3, E4]
    #   - "abc123"->"cbc123", "level"->"nevel", "Zebra"->"Bebra" [E1]
    #   - "yell"->"aell", "zebra"->"bebra", "Zoo"->"Boo", "yy"->"ay", "zz"->"bz" [E4]
    # Rule: if the first character is a digit, leave it unchanged [E2]
    #   - "1abc"->"1abc", "123 abc"->"123abc", "9lives"->"9lives" [E2, E4]
    # Rule: if the first character is a symbol/punctuation, leave it unchanged [E4]
    #   - "!hello"->"!hello", "!abc"->"!abc", "~test"->"~test", "  !hi"->"!hi" [E4]
    # So: shift only if first char is a letter; wrap 'y'->'a', 'z'->'b' within alphabet.
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        if t and t[0].isalpha():
            c = t[0]
            if c.islower():
                c = chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
            else:
                c = chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
            t = c + t[1:]
        out.append(t)
    return {"outputs": out}
